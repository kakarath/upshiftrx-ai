import json

def handler(event, context):
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Content-Type': 'application/json'
        },
        'body': json.dumps({
            'status': 'healthy',
            'service': 'upshiftrx-api',
            'platform': 'netlify'
        })
    }