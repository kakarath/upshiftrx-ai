# UpShiftRx Examples

This directory contains interactive examples demonstrating UpShiftRx capabilities.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the demo
python demo_drug_repurposing.py
```

## 📊 Available Examples

### 1. Drug-Disease Network Visualization
**File**: `drug_disease_network.ipynb`  
**Description**: Interactive network showing drug-disease relationships discovered from PubMed literature.

### 2. Literature Mining Demo
**File**: `literature_mining_demo.py`  
**Description**: Command-line demo showing how we extract drug repurposing insights from research papers.

### 3. Aspirin Case Study
**File**: `aspirin_repurposing.ipynb`  
**Description**: Real example of how aspirin was repurposed for cardiovascular disease prevention.

## 🔬 Sample Datasets

All examples use anonymized, publicly available data:
- `data/sample_papers.csv` - PubMed abstracts (100 papers)
- `data/drug_targets.json` - Known drug-target interactions
- `data/disease_ontology.json` - Disease classification system

## 🎯 Use Cases Demonstrated

- **Literature Mining**: Extract drug mentions from research papers
- **Network Analysis**: Visualize drug-disease connections
- **Evidence Ranking**: Score repurposing opportunities by evidence strength
- **Interactive Exploration**: Browse results with filtering and search

## 📝 Running Examples

### Jupyter Notebooks
```bash
jupyter notebook examples/
```

### Python Scripts
```bash
cd examples/
python literature_mining_demo.py --drug "metformin" --disease "alzheimer"
```

## 🤝 Contributing Examples

Have an interesting use case? Submit a pull request with:
- Clear documentation
- Sample data (anonymized)
- Expected outputs
- Requirements.txt updates

## 📞 Support

Questions about examples? Open an issue or contact us at upshiftrx.ai/contact