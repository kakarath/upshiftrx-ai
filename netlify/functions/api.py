import json
import requests

def handler(event, context):
    """Netlify serverless function for UpShiftRx API"""
    
    # Handle CORS
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
    }
    
    # Handle preflight requests
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }
    
    path = event.get('path', '').replace('/.netlify/functions/api', '')
    method = event['httpMethod']
    
    try:
        if path == '/health' or path == '':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'status': 'healthy',
                    'service': 'upshiftrx-api',
                    'platform': 'netlify'
                })
            }
        
        elif path == '/drugs':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'drugs': ['aspirin', 'metformin', 'ibuprofen', 'acetaminophen', 'warfarin']
                })
            }
        
        elif path == '/diseases':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'diseases': ['cancer', 'diabetes', 'heart disease', 'alzheimer\'s', 'hypertension']
                })
            }
        
        elif path == '/analyze' and method == 'POST':
            body = json.loads(event.get('body', '{}'))
            drug = body.get('drug', '')
            disease = body.get('disease', '')
            
            if not drug or not disease:
                return {
                    'statusCode': 400,
                    'headers': headers,
                    'body': json.dumps({'error': 'Drug and disease required'})
                }
            
            # Simple PubMed search
            try:
                search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
                params = {
                    "db": "pubmed",
                    "term": f"{drug} AND {disease}",
                    "retmax": 10,
                    "retmode": "json"
                }
                
                response = requests.get(search_url, params=params, timeout=10)
                data = response.json()
                ids = data.get("esearchresult", {}).get("idlist", [])
                
                papers = []
                for i, pmid in enumerate(ids[:5]):
                    papers.append({
                        "pmid": pmid,
                        "title": f"Research on {drug} and {disease} - Paper {pmid}",
                        "journal": "Medical Journal",
                        "year": "2024"
                    })
                
                return {
                    'statusCode': 200,
                    'headers': headers,
                    'body': json.dumps({
                        'drug': drug,
                        'disease': disease,
                        'paper_count': len(papers),
                        'papers': papers
                    })
                }
            except Exception as e:
                return {
                    'statusCode': 500,
                    'headers': headers,
                    'body': json.dumps({'error': f'PubMed search failed: {str(e)}'})
                }
        
        else:
            return {
                'statusCode': 404,
                'headers': headers,
                'body': json.dumps({'error': 'Endpoint not found'})
            }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': str(e)})
        }