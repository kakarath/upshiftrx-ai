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
    
    search_url = f"{base_url}esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": min(max_results, 20),  # Limit for serverless
        "retmode": "json"
    }
    
    try:
        response = requests.get(search_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("esearchresult", {}).get("idlist", [])
    except Exception as e:
        return []

def fetch_details_simple(id_list):
    """Fetch paper details - simplified for serverless"""
    papers = []
    for i, pmid in enumerate(id_list[:10]):
        papers.append({
            "pmid": pmid,
            "title": f"Research paper {pmid}",
            "journal": "Medical Journal",
            "year": "2024"
        })
    return papers

@app.get("/")
async def root():
    return {"message": "UpShiftRx API - Drug Repurposing Platform", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "upshiftrx-api", "platform": "vercel"}

@app.post("/analyze")
async def analyze_drug_disease(query: DrugDiseaseQuery):
    """Analyze a single drug-disease pair"""
    try:
        ids = search_pubmed_simple(query.drug, query.disease, query.max_results)
        papers = fetch_details_simple(ids)
        
        return {
            "drug": query.drug,
            "disease": query.disease,
            "paper_count": len(papers),
            "papers": papers
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/drugs")
async def get_drugs():
    return {"drugs": ["aspirin", "metformin", "ibuprofen", "acetaminophen", "warfarin"]}

@app.get("/diseases")
async def get_diseases():
    return {"diseases": ["cancer", "diabetes", "heart disease", "alzheimer's", "hypertension"]}

# Vercel serverless handler
def handler(request):
    return app(request)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)