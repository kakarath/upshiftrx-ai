# src/build_map.py

from hello_pubmed import search_pubmed, fetch_details, save_results
import time
import sys
import json
import argparse
from pathlib import Path

def load_config(config_file):
    """Load drug or disease list from JSON config file."""
    try:
        with open(config_file, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Config file not found: {config_file}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON config: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description="Build drug-disease mapping from PubMed")
    parser.add_argument("--drug", help="Single drug to search")
    parser.add_argument("--disease", help="Single disease to search")
    parser.add_argument("--drugs-config", default="config/drugs.json", help="Path to drugs JSON config")
    parser.add_argument("--diseases-config", default="config/diseases.json", help="Path to diseases JSON config")
    parser.add_argument("--max-results", type=int, default=50, help="Max results per query")
    parser.add_argument("--sleep", type=float, default=2.0, help="Sleep time between requests")
    
    args = parser.parse_args()
    
    # Handle single drug-disease pair
    if args.drug and args.disease:
        drugs = [args.drug]
        diseases = [args.disease]
    else:
        # Load from config files
        drugs = load_config(args.drugs_config)
        diseases = load_config(args.diseases_config)
        
        if not drugs or not diseases:
            print("No drugs or diseases loaded. Check config files.")
            return

    # Process with error handling and better rate limiting
    processed = 0
    total = len(drugs) * len(diseases)
    
    for drug in drugs:
        for disease in diseases:
            processed += 1
            print(f"\n🔎 [{processed}/{total}] {drug} vs {disease}")
            
            try:
                ids = search_pubmed(drug, disease, max_results=args.max_results)
                if ids:
                    papers = fetch_details(ids)
                    save_results(papers, drug, disease)
                    print(f"✅ Found {len(papers)} papers")
                else:
                    print("No results found.")
            except Exception as e:
                print(f"❌ Error processing {drug} vs {disease}: {e}")
                continue
            
            # Respect NCBI rate limits
            time.sleep(args.sleep)

if __name__ == "__main__":
    main()
