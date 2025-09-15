exports.handler = async (event, context) => {
  return {
    statusCode: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      status: 'healthy',
      service: 'upshiftrx-api',
      platform: 'netlify',
      version: '2.0.0',
      features: ['real-pubmed-integration', 'live-data', 'xml-parsing']
    })
  }
}