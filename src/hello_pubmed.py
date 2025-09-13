# Extracts Title, Journal, Year, PMID.
# Saves results to results/pubmed_results.csv.

from Bio import Entrez, Medline
import pandas as pd
import os
import time
import sys

# Always tell NCBI who you are
Entrez.email = os.getenv('PUBMED_EMAIL', 'contact@upshiftrx.ai')

def search_pubmed(drug, disease, max_results=100):
    """Search PubMed for articles mentioning both a drug and a disease."""
    query = f"{drug} AND {disease}"
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    handle.close()
    return record["IdList"]

def fetch_details(id_list, batch_size=50, max_retries=3):
    """Fetch article details with batching and retries."""
    all_papers = []

    # Break into smaller batches
    for start in range(0, len(id_list), batch_size):
        batch_ids = id_list[start:start+batch_size]
        ids_str = ",".join(batch_ids)

        for attempt in range(max_retries):
            try:
                handle = Entrez.efetch(db="pubmed", id=ids_str, rettype="medline", retmode="text")
                records = Medline.parse(handle)
                papers = []
                for record in records:
                    paper = {
                        "pmid": record.get("PMID", ""),
                        "title": record.get("TI", ""),
                        "journal": record.get("JT", ""),
                        "year": record.get("DP", "").split(" ")[0] if record.get("DP", "") else "",
                    }
                    papers.append(paper)
                handle.close()
                all_papers.extend(papers)
                break  # success, move to next batch
            except Exception as e:
                print(f"⚠️ Fetch attempt {attempt+1} failed for batch {start}-{start+batch_size}: {e}")
                time.sleep(3)  # wait before retry
        else:
            print(f"❌ Failed to fetch batch {start}-{start+batch_size} after {max_retries} retries")

        time.sleep(0.5)  # short pause between batches

    return all_papers

def save_results(papers, drug, disease):
    """Save papers to CSV including drug and disease columns."""
    if not papers:
        return
    
    # Ensure results directory exists
    os.makedirs("results", exist_ok=True)
    
    df = pd.DataFrame(papers)
    df["drug"] = drug
    df["disease"] = disease
    outfile = f"results/{drug}_{disease}.csv".replace(" ", "_")
    
    try:
        df.to_csv(outfile, index=False)
        print(f"Saved {len(papers)} papers to {outfile}")
    except Exception as e:
        print(f"Error saving to {outfile}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python src/hello_pubmed.py <drug> <disease>")
        sys.exit(1)

    drug = sys.argv[1]
    disease = sys.argv[2]

    print(f"\n🔎 Searching PubMed for '{drug}' AND '{disease}'...\n")
    ids = search_pubmed(drug, disease)
    if not ids:
        print("No results found.")
    else:
        papers = fetch_details(ids)
        save_results(papers, drug, disease)