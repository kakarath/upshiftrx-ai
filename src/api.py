from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import pandas as pd
import json
import os
from pathlib import Path
from hello_pubmed import search_pubmed, fetch_details
# from graph_results import build_graph  # Disabled for deployment
import asyncio
import uuid

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

class BatchQuery(BaseModel):
    drugs: List[str]
    diseases: List[str]
    max_results: int = 50

class AnalysisResult(BaseModel):
    drug: str
    disease: str
    paper_count: int
    papers: List[dict]

@app.get("/")
async def root():
    return {"message": "UpShiftRx API - Drug Repurposing Platform"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "upshiftrx-api"}

@app.post("/analyze", response_model=AnalysisResult)
async def analyze_drug_disease(query: DrugDiseaseQuery):
    """Analyze a single drug-disease pair"""
    try:
        ids = search_pubmed(query.drug, query.disease, max_results=query.max_results)
        if not ids:
            return AnalysisResult(
                drug=query.drug,
                disease=query.disease,
                paper_count=0,
                papers=[]
            )
        
        papers = fetch_details(ids)
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
    """Get available drugs from config"""
    try:
        with open("config/drugs.json", "r") as f:
            drugs = json.load(f)
        return {"drugs": drugs}
    except FileNotFoundError:
        return {"drugs": []}

@app.get("/diseases")
async def get_diseases():
    """Get available diseases from config"""
    try:
        with open("config/diseases.json", "r") as f:
            diseases = json.load(f)
        return {"diseases": diseases}
    except FileNotFoundError:
        return {"diseases": []}

@app.get("/results")
async def get_results():
    """Get existing analysis results"""
    results_dir = Path("results")
    if not results_dir.exists():
        return {"results": []}
    
    csv_files = list(results_dir.glob("*.csv"))
    results = []
    
    for csv_file in csv_files:
        if csv_file.name.startswith("pubmed_"):
            try:
                df = pd.read_csv(csv_file)
                if not df.empty and "drug" in df.columns and "disease" in df.columns:
                    drug = df["drug"].iloc[0]
                    disease = df["disease"].iloc[0]
                    results.append({
                        "drug": drug,
                        "disease": disease,
                        "paper_count": len(df),
                        "file": csv_file.name
                    })
            except Exception:
                continue
    
    return {"results": results}

@app.get("/graph")
async def generate_graph(input_file: str = "results/master_results.csv"):
    """Generate interactive graph from results"""
    return {
        "message": "Graph generation temporarily disabled in deployment",
        "note": "Use local development for graph visualization"
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)