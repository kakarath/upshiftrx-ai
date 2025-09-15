# UpShiftRx API Documentation

## Base URL
```
https://idyllic-salmiakki-7b5539.netlify.app/.netlify/functions/
```

## Authentication
No authentication required for public endpoints.

## Rate Limiting
- 100 requests per minute per IP
- Serverless functions have 15-second timeout

## Endpoints

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "upshiftrx-api",
  "platform": "netlify"
}
```

### Get Available Drugs
```http
GET /drugs
```

**Response:**
```json
{
  "drugs": ["aspirin", "metformin", "ibuprofen", "acetaminophen", "warfarin"]
}
```

### Get Available Diseases
```http
GET /diseases
```

**Response:**
```json
{
  "diseases": ["cancer", "diabetes", "heart disease", "alzheimer's", "hypertension"]
}
```

### Analyze Drug-Disease Pair
```http
POST /analyze
Content-Type: application/json

{
  "drug": "aspirin",
  "disease": "cancer"
}
```

**Response:**
```json
{
  "drug": "aspirin",
  "disease": "cancer",
  "paper_count": 15,
  "total_found": 1247,
  "papers": [
    {
      "pmid": "12345678",
      "title": "Aspirin and cancer prevention: a systematic review",
      "journal": "Journal of Clinical Oncology",
      "year": "2023"
    }
  ],
  "search_query": "aspirin AND cancer",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "error": "Valid drug and disease strings required"
}
```

### 405 Method Not Allowed
```json
{
  "error": "Method not allowed"
}
```

### 500 Internal Server Error
```json
{
  "error": "Analysis failed",
  "message": "Unable to process request at this time"
}
```

## Data Sources
- **PubMed**: Live medical literature search
- **NCBI E-utilities**: Real-time paper metadata
- **Curated Lists**: Pre-validated drug and disease names

## Usage Examples

### cURL
```bash
curl -X POST "https://idyllic-salmiakki-7b5539.netlify.app/.netlify/functions/analyze" \
  -H "Content-Type: application/json" \
  -d '{"drug": "metformin", "disease": "diabetes"}'
```

### JavaScript
```javascript
const response = await fetch('https://idyllic-salmiakki-7b5539.netlify.app/.netlify/functions/analyze', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ drug: 'aspirin', disease: 'heart disease' })
});
const data = await response.json();
```

### Python
```python
import requests

response = requests.post(
  'https://idyllic-salmiakki-7b5539.netlify.app/.netlify/functions/analyze',
  json={'drug': 'ibuprofen', 'disease': 'inflammation'}
)
data = response.json()
```