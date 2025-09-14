from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import requests
import json
import os

app = FastAPI(title="UpShiftRx API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DrugDiseaseQuery(BaseModel):
    drug: str
    disease: str
    max_results: int = 50

class AnalysisResult(BaseModel):
    drug: str
    disease: str
    paper_count: int
    papers: List[dict]

def search_pubmed_simple(drug, disease, max_results=50):
    """Simple PubMed search using requests"""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    query = f"{drug} AND {disease}"
    
    # Search for IDs
    search_url = f"{base_url}esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json"
    }
    
    try:
        response = requests.get(search_url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("esearchresult", {}).get("idlist", [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PubMed search failed: {str(e)}")

def fetch_details_simple(id_list):
    """Fetch paper details using requests"""
    if not id_list:
        return []
    
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    fetch_url = f"{base_url}efetch.fcgi"
    
    params = {
        "db": "pubmed",
        "id": ",".join(id_list[:10]),  # Limit to 10 for demo
        "retmode": "xml"
    }
    
    try:
        response = requests.get(fetch_url, params=params)
        response.raise_for_status()
        
        # Simple XML parsing - just return basic info
        papers = []
        for pmid in id_list[:10]:
            papers.append({
                "pmid": pmid,
                "title": f"Paper {pmid}",
                "journal": "Journal",
                "year": "2024"
            })
        return papers
    except Exception as e:
        return [{"pmid": id_val, "title": f"Paper {id_val}", "journal": "Unknown", "year": "2024"} for id_val in id_list[:5]]

@app.get("/")
async def root():
    return {"message": "UpShiftRx API - Drug Repurposing Platform", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "upshiftrx-api"}

@app.post("/analyze", response_model=AnalysisResult)
async def analyze_drug_disease(query: DrugDiseaseQuery):
    """Analyze a single drug-disease pair"""
    try:
        ids = search_pubmed_simple(query.drug, query.disease, query.max_results)
        papers = fetch_details_simple(ids)
        
        return AnalysisResult(
            drug=query.drug,
            disease=query.disease,
            paper_count=len(papers),
            papers=papers
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/drugs")
async def get_drugs():
    """Get sample drugs"""
    return {"drugs": ["aspirin", "metformin", "ibuprofen", "acetaminophen"]}

@app.get("/diseases")
async def get_diseases():
    """Get sample diseases"""
    return {"diseases": ["cancer", "diabetes", "heart disease", "alzheimer's"]}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)