exports.handler = async (event, context) => {
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Content-Type': 'application/json'
  };

  // Handle CORS preflight
  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  const path = event.path.replace('/.netlify/functions/api', '') || '/';
  
  try {
    // Health endpoint
    if (path === '/health' || path === '/') {
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          status: 'healthy',
          service: 'upshiftrx-api',
          platform: 'netlify',
          path: path
        })
      };
    }

    // Drugs endpoint
    if (path === '/drugs') {
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          drugs: ['aspirin', 'metformin', 'ibuprofen', 'acetaminophen']
        })
      };
    }

    // Diseases endpoint
    if (path === '/diseases') {
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          diseases: ['cancer', 'diabetes', 'heart disease', 'hypertension']
        })
      };
    }

    // Analyze endpoint (simplified for now)
    if (path === '/analyze' && event.httpMethod === 'POST') {
      const body = JSON.parse(event.body || '{}');
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          drug: body.drug || 'unknown',
          disease: body.disease || 'unknown',
          paper_count: 3,
          papers: [
            { pmid: '12345', title: 'Sample paper 1', journal: 'Test Journal', year: '2024' },
            { pmid: '12346', title: 'Sample paper 2', journal: 'Test Journal', year: '2024' },
            { pmid: '12347', title: 'Sample paper 3', journal: 'Test Journal', year: '2024' }
          ]
        })
      };
    }

    // 404 for unknown paths
    return {
      statusCode: 404,
      headers,
      body: JSON.stringify({ error: 'Endpoint not found', path: path })
    };

  } catch (error) {
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ error: error.message })
    };
  }
};