exports.handler = async (event, context) => {
  return {
    statusCode: 200,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      drugs: ['aspirin', 'metformin', 'ibuprofen', 'acetaminophen', 'warfarin']
    })
  }
}