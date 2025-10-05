# UpShiftRx 🚀

_AI-Powered Drug Repurposing for Better, Faster, Smarter Treatments_

---

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](CHANGELOG.md)
[![API Status](https://img.shields.io/badge/API-Live-green.svg)](https://idyllic-salmiakki-7b5539.netlify.app/.netlify/functions/health)
[![PubMed Integration](https://img.shields.io/badge/PubMed-Live%20Data-brightgreen.svg)]()
[![Python](https://img.shields.io/badge/python-3.9%20%7C%203.10-blue.svg)]()
[![Status](https://img.shields.io/badge/status-production-green)]()

## 🌟 Mission

UpShiftRx is building AI-driven tools to discover **new uses for existing drugs**.  
Our goal is to accelerate healthcare innovation by mining medical literature, clinical trial data, and drug databases to uncover **repurposing opportunities** that can improve patient outcomes.

---

## 📖 Project Overview

This repository is the **R&D workspace** for our core AI platform.  
It contains:

- Scripts + pipelines for ingesting biomedical data (PubMed, DrugBank, ClinicalTrials.gov).
- Machine learning experiments for drug-disease relationship prediction.
- Jupyter notebooks documenting early proof-of-concepts.
- Results, visualizations, and supporting documentation.

---

## 🔬 First Prototype

- **Input**: A disease (e.g., _colon cancer_)
- **Output**: Candidate drugs with supporting references (e.g., _aspirin_ → known studies + confidence ranking).

Our first goal is a simple **literature-mining pipeline** to rediscover known drug repurposing cases.  
If the system can re-find what humans already know, it’s a strong signal we’re on the right track.

---

## 🏗️ Repo Structure

```
upshiftrx-ai/                    # 👁️ Public Repository
├── src/                         # Core Python scripts
│   ├── build_map.py            # PubMed mining pipeline
│   ├── graph_results.py        # Interactive visualization
│   ├── hello_pubmed.py         # PubMed API utilities
│   └── combine_results.py      # Data aggregation
├── config/                      # Configuration files
│   ├── drugs.json              # Drug lists for batch processing
│   ├── diseases.json           # Disease lists for batch processing
│   └── config.yaml             # Main configuration
├── results/examples/            # 📊 Sample datasets (small)
│   └── sample_results.csv      # Demo data for testing
├── data/                        # 📥 Data fetching scripts
├── notebooks/                   # 📓 Jupyter exploration (public)
├── docs/                        # 📚 Documentation
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```

### 🔒 Private Repository (Collaborators Only)
```
upshiftrx-ai-private/           # 🔐 Private Repository
├── results/full_pubmed/        # Complete PubMed datasets
├── results/drugbank/           # DrugBank/ChEMBL data
├── models/                     # Trained ML models
├── notebooks/                  # Analysis with full datasets
└── src/                        # Proprietary processing scripts
```

## ⚡ Quickstart

Get up and running in minutes.

1. **Clone the repo**
   ```bash
   git clone https://github.com/YOUR_USERNAME/upshiftrx-ai.git
   cd upshiftrx-ai
   ```
2. Create a virtual environment
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
4. Try a minimal example dataset
   - We include a few small CSVs under `results/examples/` so you can test the pipeline without hitting PubMed.
   ```bash
   python src/graph_results.py --input results/examples/sample_results.csv
   ```
   --> Opens an interactive graph in
   `results/drug_disease_graph.html`
5. Run a live query against PubMed

   ```bash
   # Single drug-disease pair
   python src/build_map.py --drug "aspirin" --disease "colon cancer"

   # Or run batch processing with config files
   python src/build_map.py

   # Generate interactive graph
   python src/graph_results.py
   ```

   --> Fetches PubMed papers, saves results under `results/`, and builds a knowledge graph.

6. View results

---

## ⚡ Public Demo vs Full Datasets

This repository contains the **public prototype** of UpShiftRx AI:

- All scripts needed to run the **PubMed mining pipeline**.
- A **minimal example dataset** (`results/examples/sample_results.csv`) so you can try the visualization out-of-the-box.
- Documentation and roadmap to understand our vision.

**Full datasets and advanced pipelines** are **kept private** for compliance and IP protection.  
If you are a collaborator, partner, or interested researcher, you can request access via `info@upshiftrx.ai`.

This way contributors and testers have **two clear paths**:

- ✅ Play instantly with the **sample dataset** (fast, offline, no API calls).
- 🔥 Run the **live PubMed query** when they’re ready.

---

## 📊 Data & Results

This repo generates CSVs and graphs of drug–disease links from PubMed.

- **Small sample files** are included under `results/examples/` for quick testing.
- **Large datasets** (thousands of PubMed results) are **not stored in GitHub** to keep the repo lightweight.
- To regenerate them:

  ```bash
  # Single query
  python src/build_map.py --drug "aspirin" --disease "colon cancer"

  # Batch processing (uses config/drugs.json and config/diseases.json)
  python src/build_map.py

  # Custom rate limiting for large batches
  python src/build_map.py --sleep 3.0 --max-results 25
  ```

---

## 🛠️ Advanced Usage

**Command Line Options:**

```bash
# Single drug-disease pair
python src/build_map.py --drug "metformin" --disease "alzheimer's"

# Batch processing with custom settings
python src/build_map.py --max-results 100 --sleep 2.5

# Use custom config files
python src/build_map.py --drugs-config my_drugs.json --diseases-config my_diseases.json
```

**Configuration Files:**

- Edit `config/drugs.json` and `config/diseases.json` to customize your search lists
- Smaller lists = faster testing, larger lists = comprehensive analysis

---

## 📚 Documentation

- [Vision](docs/VISION.md) – Why UpShiftRx exists
- [Roadmap](docs/ROADMAP.md) – Milestones + strategy
- [Developer Guide](docs/DEVELOPER.md) – Technical notes

---

This way, a new visitor **instantly knows how to clone, run, and explore**, and also sees the deeper docs if they want to dive in 🚀.

## 🤝 Contributing

We welcome collaborators! See CONTRIBUTING.md for guidelines.
**coming soon**

---

## 📜 License

MIT License (flexible for open innovation).

## 🌍 About UpShiftRx LLC

Founded in Maryland, USA — 2025.
We are committed to using AI to accelerate medical breakthroughs and help physicians discover better treatments for their patients.

**Current Phase**: MVP Development (Phase 1 of 4)
**Website**: https://upshiftrx.ai (in development)
**Contact**: info@upshiftrx.ai (coming soon)

### Development Ecosystem
- **upshiftrx-ai** (this repo): Core R&D and public API
- **upshiftrx-website**: User interface and search functionality
- **upshiftrx-ai-private**: Proprietary models and full datasets

## 🚀 Phase 1 Progress (MVP Development)

**Current Status**: 60% Complete | [View Detailed Criteria](docs/PHASE_COMPLETION_CRITERIA.md)

### ✅ Completed
- PubMed mining pipeline
- Interactive visualization system
- API infrastructure
- Sample datasets

### 🔄 In Progress
- Core AI models (drug-target interactions)
- Dataset expansion (targeting 10M+ compounds)
- Web interface development
- Validation with known repurposing cases

### 🎯 Phase 1 Goals
- **Accuracy**: >85% on validation set
- **Coverage**: 10M+ compounds analyzed
- **Performance**: <2s API response time
- **Validation**: 3 confirmed repurposing cases

## 🔮 Future Work

- Expand beyond PubMed → integrate DrugBank + ClinicalTrials.gov
- Add machine learning ranking of drug–disease links
- Build interactive web dashboard for researchers and clinicians
- Deploy serverless N-M search capabilities (drug↔diseases)

## 🔥 Slogan ideas for UpShiftRx

(short, memorable, forward-looking — tone: visionary, practical, or playful):
“Shifting tomorrow’s cures into today.”
“Revealing hidden treatments with AI.”
“Accelerating medicine through repurposing.”
“Every drug has another story — we find it.”
“UpShiftRx: Turning old pills into new hope.”
“Smarter paths to better treatments.”
“Discover more. Faster. Smarter.”
“Repurposing medicine, reimagining care.”
“AI-powered breakthroughs hiding in plain sight.”
“Shifting the future of medicine.”
-- finalizing soon.
