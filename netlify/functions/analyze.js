exports.handler = async (event, context) => {
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers: { 'Access-Control-Allow-Origin': '*' },
      body: JSON.stringify({ error: 'Method not allowed' })
    }
  }

  let body;
  try {
    body = JSON.parse(event.body || '{}');
  } catch (error) {
    return {
      statusCode: 400,
      headers: { 'Access-Control-Allow-Origin': '*' },
      body: JSON.stringify({ error: 'Invalid JSON format' })
    }
  }
  
  const { drug, disease } = body;
  
  // Input validation
  if (!drug || !disease || typeof drug !== 'string' || typeof disease !== 'string') {
    return {
      statusCode: 400,
      headers: { 'Access-Control-Allow-Origin': '*' },
      body: JSON.stringify({ error: 'Valid drug and disease strings required' })
    }
  }

  // Sanitize inputs to prevent injection
  const sanitizedDrug = drug.replace(/[^a-zA-Z0-9\s-]/g, '').trim().substring(0, 100);
  const sanitizedDisease = disease.replace(/[^a-zA-Z0-9\s-]/g, '').trim().substring(0, 100);

  if (!sanitizedDrug || !sanitizedDisease) {
    return {
      statusCode: 400,
      headers: { 'Access-Control-Allow-Origin': '*' },
      body: JSON.stringify({ error: 'Invalid characters in drug or disease names' })
    }
  }

  return {
    statusCode: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      drug: sanitizedDrug,
      disease: sanitizedDisease,
      paper_count: 3,
      papers: [
        { pmid: '12345', title: `Research on ${sanitizedDrug} and ${sanitizedDisease}`, journal: 'Medical Journal', year: '2024' },
        { pmid: '12346', title: `Clinical study of ${sanitizedDrug}`, journal: 'Clinical Journal', year: '2024' },
        { pmid: '12347', title: `${sanitizedDisease} treatment options`, journal: 'Treatment Journal', year: '2024' }
      ]
    })
  }
}