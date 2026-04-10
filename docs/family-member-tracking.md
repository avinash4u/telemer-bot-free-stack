# Family Member Tracking & Call Ending Guide

## Overview

The TeleMER bot now supports advanced family member tracking and intelligent call ending capabilities. These features enhance the user experience by:

1. **Family Member Medical Tracking**: Records medical conditions for different family members
2. **Intelligent Call Ending**: Automatically ends calls when appropriate
3. **Contextual Responses**: Provides personalized responses based on who has the condition

## Features

### 1. Family Member Medical Tracking

The bot can identify and track medical conditions for different family members:

**Supported Family Members:**
- **Self**: "I have...", "I'm experiencing..."
- **Mother**: "My mother...", "My mom...", "Mother has..."
- **Father**: "My father...", "My dad...", "Father has..."
- **Spouse**: "My husband...", "My wife...", "My spouse..."
- **Child**: "My son...", "My daughter...", "My child..."
- **Sibling**: "My brother...", "My sister...", "My sibling..."

**Example Usage:**
```
User: "My mother has diabetes"
Bot: "I've analyzed your symptoms and generated medical codes. 
      Recorded for Mother: Symptoms identified: diabetes. 
      Medical codes (ICD-10): E11.9. 
      Your symptoms appear to be manageable. Thank you for sharing this information with TeleMER."
```

### 2. Intelligent Call Ending

The bot automatically detects when calls should end based on user input:

**Call Ending Triggers:**
- **No Issues**: "no", "nothing", "no issues", "no problems"
- **Gratitude**: "thank you", "thanks", "appreciate it"
- **Completion**: "that's all", "that's everything", "nothing else"
- **Well-being**: "I'm fine", "I'm good", "everything is fine"
- **Medical Context**: "no medical issues", "no symptoms"

**Example Scenarios:**

**Scenario 1: No Issues**
```
User: "no"
Bot: "Thank you for your time. I hope you have a wonderful day! Take care."
[Call automatically ends after 3 seconds]
```

**Scenario 2: Gratitude**
```
User: "thank you"
Bot: "Thank you for sharing this information. Your health records have been updated. Have a great day!"
[Call automatically ends after 3 seconds]
```

**Scenario 3: No Medical Issues**
```
User: "I have no health issues"
Bot: "Thank you for your time. I hope you have a wonderful day! Take care."
[Call automatically ends after 3 seconds]
```

## Technical Implementation

### Family Member Extraction

The system uses pattern matching to identify family members:

```python
def extract_family_member(self, text: str) -> Tuple[str, str]:
    family_patterns = {
        "self": ["i have", "i'm experiencing", "i feel"],
        "mother": ["my mother", "my mom", "mother has"],
        "father": ["my father", "my dad", "father has"],
        "spouse": ["my husband", "my wife", "my spouse"],
        "child": ["my son", "my daughter", "my child"],
        "sibling": ["my brother", "my sister", "my sibling"]
    }
```

### Call Ending Logic

The system determines when to end calls:

```python
def should_end_call(self, text: str, intent: str, symptoms: List[str]) -> bool:
    ending_phrases = [
        "no", "nothing", "none", "no issues", "no problems",
        "thank you", "thanks", "that's all", "that's everything",
        "i'm fine", "i'm good", "everything is fine",
        "no medical issues", "no health issues", "no symptoms"
    ]
    
    # Check for ending phrases
    for phrase in ending_phrases:
        if phrase in text.lower():
            return True
```

### Family Medical Record Structure

```json
{
  "family_member": "mother",
  "condition_text": "diabetes",
  "symptoms": ["diabetes"],
  "medical_codes": {
    "icd10_codes": ["E11.9", "E10.9", "E11.8"],
    "descriptions": ["Type 2 diabetes mellitus", "Type 1 diabetes mellitus"],
    "severity_levels": ["medium"]
  },
  "timestamp": "current_call"
}
```

## User Interface Enhancements

### WebRTC Interface Features

**1. Family Member Display**
- Blue-colored panel for family member information
- Shows member name, condition, symptoms, and ICD-10 codes
- Only displays for non-self family members

**2. Call Ending Indicators**
- Automatic call termination after appropriate responses
- Visual status updates: "Call ended - Thank you for using TeleMER!"
- 3-second delay before actual call ending

**3. Enhanced Medical Analysis**
- Green panel for medical analysis (self)
- Blue panel for family member records
- Clear visual distinction between different types of records

## API Response Structure

### Enhanced Response with Family Tracking

```json
{
  "status": "NEW",
  "nlu": {...},
  "sentiment": {...},
  "action": "route_imu",
  "medical_codes": {
    "symptoms": ["diabetes"],
    "icd10_codes": ["E11.9", "E10.9"],
    "descriptions": ["Type 2 diabetes mellitus"]
  },
  "family_record": {
    "family_member": "mother",
    "condition_text": "diabetes",
    "symptoms": ["diabetes"],
    "medical_codes": {...}
  },
  "should_end_call": false
}
```

### Call Ending Response

```json
{
  "status": "NEW",
  "action": "call_ended",
  "medical_codes": {...},
  "should_end_call": true,
  "family_record": null
}
```

## Usage Examples

### Example 1: Self Medical Condition
```
User: "I have chest pain"
Bot: "I've analyzed your symptoms and generated medical codes. 
      Symptoms identified: chest pain. 
      Medical codes (ICD-10): R07.9. 
      Your symptoms appear to be manageable. Thank you for sharing this information with TeleMER. 
      Is there anything else I can help you with today?"
```

### Example 2: Mother Medical Condition
```
User: "My mother has diabetes"
Bot: "I've analyzed your symptoms and generated medical codes. 
      Recorded for Mother: Symptoms identified: diabetes. 
      Medical codes (ICD-10): E11.9. 
      Your symptoms appear to be manageable. Thank you for sharing this information with TeleMER. 
      Is there anything else I can help you with today?"
```

### Example 3: Call Ending - No Issues
```
User: "no"
Bot: "Thank you for your time. I hope you have a wonderful day! Take care."
[Call ends automatically]
```

### Example 4: Call Ending - Gratitude
```
User: "thank you"
Bot: "Thank you for sharing this information. Your health records have been updated. Have a great day!"
[Call ends automatically]
```

## Configuration

### Adding New Family Members

To add new family member types, update the `family_patterns` dictionary:

```python
family_patterns = {
    "grandmother": ["my grandmother", "my grandma", "grandmother has"],
    "grandfather": ["my grandfather", "my grandpa", "grandfather has"]
}
```

### Customizing Call Ending Phrases

To modify call ending triggers, update the `ending_phrases` list:

```python
ending_phrases = [
    "no", "nothing", "none", "no issues",
    "thank you", "thanks", "appreciate it",
    "goodbye", "bye", "see you later"  # Add new phrases
]
```

## Testing

### Test Cases

**1. Family Member Tracking:**
- "My mother has diabetes" -> Should record for mother
- "My father has chest pain" -> Should record for father
- "I have headache" -> Should record for self (no family panel)

**2. Call Ending:**
- "no" -> Should end call
- "thank you" -> Should end call
- "I have no issues" -> Should end call
- "I have chest pain" -> Should NOT end call

**3. Combined Scenarios:**
- "My mother has diabetes" -> Record for mother, continue call
- "My mother has diabetes" then "thank you" -> Record for mother, then end call

### API Testing Commands

```bash
# Test family member tracking
curl -X POST http://localhost:8000/calls/{case_id}/utterance \
  -H "Content-Type: application/json" \
  -d '{"text": "My mother has diabetes", "session_id": "test"}'

# Test call ending
curl -X POST http://localhost:8000/calls/{case_id}/utterance \
  -H "Content-Type: application/json" \
  -d '{"text": "no", "session_id": "test"}'
```

## Benefits

### For Patients
- **Family Health Tracking**: Monitor health of entire family
- **Convenient Reporting**: Report conditions for family members easily
- **Natural Conversation**: Call ends naturally when appropriate

### For Healthcare Providers
- **Family Medical History**: Complete family health records
- **Contextual Information**: Know who has each condition
- **Efficient Consultations**: Pre-screened family medical data

### For Healthcare Organizations
- **Comprehensive Records**: Family-wide medical tracking
- **Improved Patient Experience**: Natural call flow
- **Reduced Call Times**: Automatic call ending when appropriate

## Troubleshooting

### Common Issues

**1. Family Member Not Detected**
- Check if the phrase pattern exists in `family_patterns`
- Verify the exact phrasing matches the patterns

**2. Call Not Ending**
- Ensure the phrase is in `ending_phrases` list
- Check if there are conflicting symptoms

**3. Wrong Family Member Identified**
- Review the pattern matching order
- Check for overlapping patterns

### Debug Information

Enable debug logging to see family member extraction:

```python
member, condition = medical_coder.extract_family_member(text)
print(f"Detected member: {member}, condition: {condition}")
```

## Future Enhancements

1. **Extended Family Support**: Grandparents, aunts, uncles, cousins
2. **Relationship Context**: Understanding complex family relationships
3. **Medical History Tracking**: Historical family medical records
4. **Multi-language Support**: Family member terms in different languages
5. **Voice Recognition**: Identify different speakers in family calls

## Conclusion

The enhanced TeleMER bot with family member tracking and intelligent call ending provides:

- **Comprehensive Family Health Monitoring**: Track conditions for all family members
- **Natural Call Flow**: Automatic call ending when appropriate
- **Enhanced User Experience**: Contextual, personalized interactions
- **Improved Efficiency**: Reduced call times and better data collection

These features make the TeleMER bot more user-friendly and efficient for both patients and healthcare providers.
