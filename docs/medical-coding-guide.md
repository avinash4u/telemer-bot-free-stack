# Medical Coding & AI Workflow Guide

## Overview

The TeleMER bot now includes advanced medical coding capabilities that automatically:
- Extract symptoms from patient descriptions
- Generates ICD-10 medical codes
- Assesses complexity and determines if medical consultation is needed
- Provides intelligent responses based on medical analysis

## Features

### 1. Symptom Extraction
The bot automatically identifies medical symptoms from patient text using keyword matching.

**Supported Symptoms:**
- **Chest Pain**: `chest pain`, `heart attack`, `heart disease`
- **Diabetes**: `diabetes`, `high blood sugar`
- **Respiratory**: `difficulty breathing`, `cough`
- **Neurological**: `headache`, `dizziness`
- **Abdominal**: `stomach pain`, `nausea`
- **Fever**: `fever`, `high temperature`
- **Mental Health**: `anxiety`, `depression`

### 2. ICD-10 Code Generation
For each identified symptom, the bot generates appropriate ICD-10 codes:

**Example:**
```
Input: "I have chest pain and diabetes"
ICD-10 Codes: [R07.9, R07.8, E11.9, E11.8, E10.9]
```

### 3. Complexity Assessment
The bot evaluates if the case requires medical professional consultation:

**Factors:**
- **High Severity Symptoms**: Difficulty breathing, heart attack, etc.
- **Multiple Symptoms**: More than 3 different symptoms
- **Negative Sentiment**: High distress levels (>70% negative)

### 4. Intelligent Workflow
Based on the assessment, the bot follows different workflows:

#### Simple Cases (No Consultation Needed)
- Generates medical codes
- Provides reassurance
- Ends conversation gracefully
- Completes without human intervention

#### Complex Cases (Consultation Required)
- Generates medical codes
- Recommends medical consultation
- Offers to connect with healthcare professional
- Escalates to human review

## Usage Examples

### Example 1: Simple Case
```
User: "I have chest pain and diabetes"
Bot: "I've analyzed your symptoms and generated medical codes. 
      Symptoms identified: chest pain, diabetes. 
      Medical codes (ICD-10): R07.9, E11.9. 
      Your symptoms appear to be manageable. Thank you for sharing this information with TeleMER."
```

### Example 2: Complex Case
```
User: "I have severe chest pain and difficulty breathing"
Bot: "I've analyzed your symptoms and generated medical codes. 
      Symptoms identified: chest pain, difficulty breathing. 
      Medical codes (ICD-10): R07.9, R06.02. 
      Based on your symptoms including difficulty breathing, I recommend speaking with a medical professional for proper evaluation. I can connect you with a healthcare professional."
```

### Example 3: No Medical Issues
```
User: "I have no health issues to report"
Bot: "Thank you for letting me know. Is there anything else I can help you with today?"
```

## Technical Implementation

### Medical Coding Service
Located at: `app/services/medical_coding.py`

**Key Classes:**
- `MedicalCoder`: Main class for symptom extraction and code generation
- `ICD-10 Mapping`: Comprehensive symptom-to-code mapping with severity levels

### API Response Structure
```json
{
  "status": "NEW",
  "nlu": {...},
  "sentiment": {...},
  "action": "route_imu",
  "medical_codes": {
    "symptoms": ["chest pain", "diabetes"],
    "icd10_codes": ["R07.9", "E11.9"],
    "descriptions": ["Chest pain, unspecified", "Type 2 diabetes mellitus"],
    "severity_levels": ["medium"],
    "requires_medical_attention": false
  },
  "symptoms": ["chest pain", "diabetes"],
  "complexity_assessment": {
    "requires_consultation": false,
    "high_severity_symptoms": [],
    "complex_conditions": [],
    "high_negative_sentiment": false,
    "recommendation": "Your symptoms appear to be manageable..."
  }
}
```

### WebRTC Interface Enhancements
The WebRTC client now displays:
- **Medical Analysis Panel**: Shows symptoms, ICD-10 codes, and descriptions
- **Intelligent Responses**: Context-aware responses based on medical analysis
- **Visual Indicators**: Color-coded severity levels

## ICD-10 Code Reference

### High Severity (Requires Consultation)
- **R06.02**: Shortness of breath
- **I21.9**: Acute myocardial infarction
- **I50.9**: Heart failure
- **F32.9**: Major depressive disorder

### Medium Severity
- **R07.9**: Chest pain, unspecified
- **E11.9**: Type 2 diabetes mellitus
- **R42**: Dizziness and giddiness
- **R10.9**: Unspecified abdominal pain

### Low Severity
- **R51**: Headache
- **R05**: Cough
- **R11.0**: Nausea
- **F41.9**: Anxiety, unspecified

## Integration with Existing Workflow

### State Machine Integration
The medical coding integrates seamlessly with the existing call flow state machine:

1. **Input Processing**: Patient utterance received
2. **NLU Analysis**: Intent and entities extracted
3. **Medical Coding**: Symptoms extracted and codes generated
4. **Complexity Assessment**: Consultation need determined
5. **Action Determination**: Route to appropriate workflow
6. **Response Generation**: Intelligent response created

### Queue Integration
- **Simple Cases**: Published to STP queue for completion
- **Complex Cases**: Published to IMU queue for medical review

## Configuration

### Adding New Symptoms
To add new symptoms, update the `icd10_mapping` in `MedicalCoder`:

```python
"new_symptom": {
    "codes": ["Xxx.x", "Yyy.y"],
    "descriptions": ["Description 1", "Description 2"],
    "severity": "medium"
}
```

### Customizing Complexity Rules
Modify the `assess_complexity` method to adjust consultation criteria:

```python
requires_consultation = (
    len(high_severity_symptoms) > 0 or 
    len(complex_conditions) > 0 or 
    high_negative_sentiment
)
```

## Testing

### Test Cases
1. **Simple Medical Disclosure**: "I have diabetes"
2. **Complex Medical Disclosure**: "I have chest pain and difficulty breathing"
3. **No Disclosure**: "I have no issues"
4. **Multiple Symptoms**: "I have headache, nausea, and anxiety"

### API Testing
```bash
curl -X POST http://localhost:8000/calls/{case_id}/utterance \
  -H "Content-Type: application/json" \
  -d '{"text": "I have chest pain and diabetes", "session_id": "test"}'
```

## Benefits

### For Patients
- **Immediate Medical Analysis**: Real-time symptom assessment
- **Clear Medical Codes**: Understandable ICD-10 codes
- **Appropriate Care**: Right level of medical attention
- **Reduced Wait Times**: Fast processing for simple cases

### For Healthcare Providers
- **Pre-screened Cases**: Medical codes already generated
- **Prioritized Reviews**: Complex cases flagged for attention
- **Efficient Workflow**: Simple cases handled automatically
- **Standardized Documentation**: Consistent ICD-10 coding

### For Healthcare Organizations
- **Cost Reduction**: Automated handling of routine cases
- **Improved Patient Experience**: Faster resolution
- **Better Resource Allocation**: Focus on complex cases
- **Compliance**: Standardized medical coding

## Future Enhancements

1. **Expanded Symptom Library**: More comprehensive symptom coverage
2. **Drug Interaction Checking**: Medication safety analysis
3. **Symptom Severity Scoring**: Quantitative severity assessment
4. **Integration with EMR**: Direct electronic medical record updates
5. **Multi-language Support**: Medical coding in multiple languages

## Troubleshooting

### Common Issues
1. **Missing Medical Codes**: Check symptom extraction logic
2. **Incorrect Severity**: Review ICD-10 mapping configuration
3. **Wrong Consultation Decision**: Adjust complexity assessment rules

### Debugging
```bash
# Test medical coding directly
docker exec orchestrator python -c "
from app.services.medical_coding import medical_coder
print(medical_coder.extract_symptoms('I have chest pain'))
print(medical_coder.generate_codes(['chest pain']))
"
```

## Conclusion

The enhanced TeleMER bot with medical coding provides:
- **Intelligent Medical Analysis**: Automated symptom extraction and coding
- **Appropriate Care Decisions**: Smart consultation recommendations
- **Seamless Integration**: Works with existing TeleMER infrastructure
- **Scalable Solution**: Handles both simple and complex medical cases

This system significantly improves the efficiency and accuracy of medical intake processing while ensuring patients receive appropriate care based on their medical needs.
