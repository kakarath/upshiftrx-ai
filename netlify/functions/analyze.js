exports.handler = async (event, context) => {
  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers: { 'Access-Control-Allow-Origin': '*' },
      body: JSON.stringify({ error: 'Method not allowed' })
    }
  }

  const body = JSON.parse(event.body || '{}');
  const { drug, disease } = body;

  return {
    statusCode: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      drug: drug || 'unknown',
      disease: disease || 'unknown',
      paper_count: 3,
      papers: [
        { pmid: '12345', title: `Research on ${drug} and ${disease}`, journal: 'Medical Journal', year: '2024' },
        { pmid: '12346', title: `Clinical study of ${drug}`, journal: 'Clinical Journal', year: '2024' },
        { pmid: '12347', title: `${disease} treatment options`, journal: 'Treatment Journal', year: '2024' }
      ]
    })
  }
}