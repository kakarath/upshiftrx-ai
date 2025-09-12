from Bio import Entrez
import sys

# Always tell NCBI who you are
Entrez.email = "pozogu@upshiftrx.ai"

def search_pubmed(drug, disease, max_results=10):
    """Search PubMed for articles mentioning both a drug and a disease."""
    query = f"{drug} AND {disease}"
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    handle.close()
    return record["IdList"]

def fetch_details(id_list):
    """Fetch article details (titles, journals) for given PubMed IDs."""
    ids = ",".join(id_list)
    handle = Entrez.efetch(db="pubmed", id=ids, rettype="medline", retmode="text")
    results = handle.read()
    handle.close()
    return results

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python src/hello_pubmed.py <drug> <disease>")
        sys.exit(1)

    drug = sys.argv[1]
    disease = sys.argv[2]

    print(f"\n🔎 Searching PubMed for articles about '{drug}' and '{disease}'...\n")
    ids = search_pubmed(drug, disease, max_results=5)

    if not ids:
        print("No results found.")
    else:
        print(f"Found {len(ids)} articles. Fetching details...\n")
        details = fetch_details(ids)
        print(details)
