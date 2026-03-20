const https = require('https');
const querystring = require('querystring');

function makeRequest(url) {
  return new Promise((resolve, reject) => {
    const timeout = setTimeout(() => reject(new Error('Request timeout')), 15000);
    
    https.get(url, (res) => {
      clearTimeout(timeout);
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          resolve(data);
        }
      });
    }).on('error', (err) => {
      clearTimeout(timeout);
      reject(err);
    });
  });
}

async function searchStrokeTherapies(strokeType, recoveryPhase) {
  const strokeQueries = {
    'ischemic': [
      `${strokeType} stroke AND neuroprotection`,
      `${strokeType} stroke AND reperfusion`,
      `${strokeType} stroke AND thrombolysis`,
      `${strokeType} stroke AND rehabilitation`
    ],
    'hemorrhagic': [
      `${strokeType} stroke AND blood pressure`,
      `${strokeType} stroke AND neuroprotection`,
      `${strokeType} stroke AND rehabilitation`
    ],
    'rehabilitation': [
      `stroke rehabilitation AND ${recoveryPhase}`,
      `stroke recovery AND neuroplasticity`,
      `stroke therapy AND motor function`,
      `stroke AND cognitive rehabilitation`
    ]
  };

  const queries = strokeQueries[strokeType] || strokeQueries['rehabilitation'];
  const allResults = [];

  for (const query of queries) {
    try {
      const searchParams = querystring.stringify({
        db: 'pubmed',
        term: query,
        retmax: 10,
        retmode: 'json',
        sort: 'relevance'
      });
      
      const searchUrl = `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?${searchParams}`;
      const searchData = await makeRequest(searchUrl);
      const ids = searchData?.esearchresult?.idlist || [];
      
      if (ids.length > 0) {
        allResults.push({
          query: query,
          paper_count: ids.length,
          total_found: searchData?.esearchresult?.count || 0,
          pmids: ids.slice(0, 5)
        });
      }
    } catch (error) {
      console.error(`Error searching for ${query}:`, error);
    }
  }

  return allResults;
}

async function getStrokeRecoveryTimeline(strokeType) {
  const timelines = {
    'ischemic': {
      'acute': '0-24 hours: Thrombolysis window, neuroprotection critical',
      'subacute': '1-7 days: Prevent complications, early mobilization',
      'early_recovery': '1-3 months: Intensive rehabilitation, neuroplasticity',
      'late_recovery': '3-12 months: Continued therapy, adaptation strategies',
      'chronic': '12+ months: Long-term management, secondary prevention'
    },
    'hemorrhagic': {
      'acute': '0-24 hours: Blood pressure control, prevent rebleeding',
      'subacute': '1-7 days: Monitor for complications, gradual mobilization',
      'early_recovery': '1-3 months: Rehabilitation focus, motor recovery',
      'late_recovery': '3-12 months: Functional improvement, adaptive strategies',
      'chronic': '12+ months: Long-term care, quality of life focus'
    }
  };

  return timelines[strokeType] || timelines['ischemic'];
}

exports.handler = async (event, context) => {
  // CORS handling
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'POST, OPTIONS'
      },
      body: ''
    };
  }

  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers: { 'Access-Control-Allow-Origin': '*' },
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  let body;
  try {
    body = JSON.parse(event.body || '{}');
  } catch (error) {
    return {
      statusCode: 400,
      headers: { 'Access-Control-Allow-Origin': '*' },
      body: JSON.stringify({ error: 'Invalid JSON format' })
    };
  }
  
  const { stroke_type, recovery_phase, analysis_type } = body;
  
  // Input validation
  const validStrokeTypes = ['ischemic', 'hemorrhagic', 'rehabilitation'];
  const validPhases = ['acute', 'subacute', 'early_recovery', 'late_recovery', 'chronic'];
  const validAnalysis = ['drug_repurposing', 'recovery_timeline', 'therapy_options'];

  if (!stroke_type || !validStrokeTypes.includes(stroke_type)) {
    return {
      statusCode: 400,
      headers: { 'Access-Control-Allow-Origin': '*' },
      body: JSON.stringify({ 
        error: 'Valid stroke_type required',
        valid_types: validStrokeTypes
      })
    };
  }

  try {
    let results = {};

    // Drug repurposing analysis
    if (!analysis_type || analysis_type === 'drug_repurposing') {
      const therapies = await searchStrokeTherapies(stroke_type, recovery_phase);
      results.drug_repurposing = {
        stroke_type: stroke_type,
        therapy_categories: therapies,
        total_categories: therapies.length,
        recommended_drugs: [
          'Alteplase (tPA) - Thrombolytic therapy',
          'Aspirin - Antiplatelet therapy', 
          'Atorvastatin - Neuroprotection',
          'Citicoline - Cognitive enhancement',
          'Memantine - NMDA receptor antagonist'
        ]
      };
    }

    // Recovery timeline
    if (!analysis_type || analysis_type === 'recovery_timeline') {
      const timeline = await getStrokeRecoveryTimeline(stroke_type);
      results.recovery_timeline = {
        stroke_type: stroke_type,
        phases: timeline,
        current_phase: recovery_phase || 'not_specified',
        key_interventions: {
          'acute': ['Thrombolysis', 'Neuroprotection', 'Blood pressure management'],
          'subacute': ['Early mobilization', 'Swallow assessment', 'DVT prevention'],
          'early_recovery': ['Physical therapy', 'Speech therapy', 'Occupational therapy'],
          'late_recovery': ['Adaptive equipment', 'Community reintegration', 'Caregiver support'],
          'chronic': ['Secondary prevention', 'Long-term monitoring', 'Quality of life']
        }
      };
    }

    // Therapy options
    if (!analysis_type || analysis_type === 'therapy_options') {
      results.therapy_options = {
        stroke_type: stroke_type,
        rehabilitation_approaches: [
          'Constraint-induced movement therapy',
          'Robot-assisted therapy',
          'Virtual reality rehabilitation',
          'Transcranial magnetic stimulation',
          'Functional electrical stimulation'
        ],
        emerging_therapies: [
          'Stem cell therapy',
          'Brain-computer interfaces',
          'Exoskeleton training',
          'Pharmacological enhancement of plasticity'
        ]
      };
    }

    return {
      statusCode: 200,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        version: '2.1.1',
        analysis_type: 'stroke_specific',
        timestamp: new Date().toISOString(),
        data_sources: ['PubMed/MEDLINE', 'Clinical Guidelines', 'Rehabilitation Research'],
        ...results,
        disclaimer: 'This information is for research purposes only. Always consult healthcare professionals for medical decisions.'
      })
    };

  } catch (error) {
    console.error('Stroke analysis error:', error);
    return {
      statusCode: 500,
      headers: { 'Access-Control-Allow-Origin': '*' },
      body: JSON.stringify({ 
        error: 'Analysis failed',
        message: 'Unable to process stroke analysis request'
      })
    };
  }
};