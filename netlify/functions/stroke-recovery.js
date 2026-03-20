exports.handler = async (event, context) => {
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

  const { 
    age, 
    stroke_type, 
    severity_score, 
    time_to_treatment, 
    comorbidities,
    current_phase 
  } = body;

  // Input validation
  if (!age || !stroke_type || !severity_score) {
    return {
      statusCode: 400,
      headers: { 'Access-Control-Allow-Origin': '*' },
      body: JSON.stringify({ 
        error: 'Required fields: age, stroke_type, severity_score'
      })
    };
  }

  try {
    // Simple recovery prediction algorithm
    let recoveryScore = 100;
    
    // Age factor (younger = better recovery)
    if (age > 80) recoveryScore -= 30;
    else if (age > 65) recoveryScore -= 20;
    else if (age > 50) recoveryScore -= 10;
    
    // Severity factor (NIHSS-like scoring)
    if (severity_score > 20) recoveryScore -= 40;
    else if (severity_score > 15) recoveryScore -= 30;
    else if (severity_score > 10) recoveryScore -= 20;
    else if (severity_score > 5) recoveryScore -= 10;
    
    // Time to treatment factor
    if (time_to_treatment > 6) recoveryScore -= 25;
    else if (time_to_treatment > 4.5) recoveryScore -= 15;
    else if (time_to_treatment > 3) recoveryScore -= 10;
    
    // Comorbidities factor
    const comorbidityCount = (comorbidities || []).length;
    recoveryScore -= comorbidityCount * 5;
    
    // Ensure score stays within bounds
    recoveryScore = Math.max(10, Math.min(100, recoveryScore));
    
    // Generate recovery timeline
    const timeline = {
      '1_month': {
        'motor_function': Math.max(20, recoveryScore * 0.3),
        'cognitive_function': Math.max(30, recoveryScore * 0.4),
        'independence_level': Math.max(15, recoveryScore * 0.2)
      },
      '3_months': {
        'motor_function': Math.max(30, recoveryScore * 0.5),
        'cognitive_function': Math.max(40, recoveryScore * 0.6),
        'independence_level': Math.max(25, recoveryScore * 0.4)
      },
      '6_months': {
        'motor_function': Math.max(40, recoveryScore * 0.7),
        'cognitive_function': Math.max(50, recoveryScore * 0.8),
        'independence_level': Math.max(35, recoveryScore * 0.6)
      },
      '12_months': {
        'motor_function': Math.max(50, recoveryScore * 0.8),
        'cognitive_function': Math.max(60, recoveryScore * 0.9),
        'independence_level': Math.max(45, recoveryScore * 0.7)
      }
    };

    // Personalized recommendations
    const recommendations = [];
    
    if (recoveryScore > 70) {
      recommendations.push('Excellent recovery potential - intensive rehabilitation recommended');
      recommendations.push('Consider advanced therapies: robot-assisted training, VR rehabilitation');
    } else if (recoveryScore > 50) {
      recommendations.push('Good recovery potential - standard rehabilitation protocols');
      recommendations.push('Focus on motor and cognitive training');
    } else {
      recommendations.push('Moderate recovery potential - adaptive strategies important');
      recommendations.push('Emphasize quality of life and caregiver support');
    }

    if (age < 65) {
      recommendations.push('Age advantage - neuroplasticity enhancement therapies beneficial');
    }

    if (stroke_type === 'ischemic' && time_to_treatment <= 4.5) {
      recommendations.push('Timely treatment received - good prognostic indicator');
    }

    return {
      statusCode: 200,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        version: '2.1.1',
        analysis_type: 'recovery_prediction',
        patient_profile: {
          age,
          stroke_type,
          severity_score,
          time_to_treatment,
          comorbidities: comorbidities || []
        },
        recovery_prediction: {
          overall_score: Math.round(recoveryScore),
          confidence_level: 'Moderate', // Based on available data
          timeline: timeline,
          key_factors: {
            'age_impact': age > 65 ? 'Negative' : 'Positive',
            'severity_impact': severity_score > 15 ? 'High' : severity_score > 10 ? 'Moderate' : 'Low',
            'treatment_timing': time_to_treatment <= 4.5 ? 'Optimal' : 'Delayed'
          }
        },
        recommendations: recommendations,
        next_steps: [
          'Consult with stroke rehabilitation team',
          'Develop personalized therapy plan',
          'Regular progress monitoring',
          'Family/caregiver education'
        ],
        timestamp: new Date().toISOString(),
        disclaimer: 'Predictions are estimates based on general patterns. Individual outcomes may vary significantly. Always consult healthcare professionals.'
      })
    };

  } catch (error) {
    console.error('Recovery prediction error:', error);
    return {
      statusCode: 500,
      headers: { 'Access-Control-Allow-Origin': '*' },
      body: JSON.stringify({ 
        error: 'Prediction failed',
        message: 'Unable to generate recovery prediction'
      })
    };
  }
};