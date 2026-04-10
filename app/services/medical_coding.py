"""Medical coding service for ICD-10 code generation"""
from typing import Dict, List, Optional, Tuple
import re

class MedicalCoder:
    """Generate ICD-10 codes based on symptoms and conditions"""
    
    def __init__(self):
        self.icd10_mapping = {
            # Chest pain related
            "chest pain": {
                "codes": ["R07.9", "R07.8", "R07.1"],
                "descriptions": ["Chest pain, unspecified", "Other chest pain", "Chest pain on breathing"],
                "severity": "medium"
            },
            "heart attack": {
                "codes": ["I21.9", "I21.0", "I21.1"],
                "descriptions": ["Acute myocardial infarction, unspecified", "ST elevation myocardial infarction", "Non-ST elevation myocardial infarction"],
                "severity": "high"
            },
            "heart disease": {
                "codes": ["I25.1", "I25.9", "I50.9"],
                "descriptions": ["Atherosclerotic heart disease", "Chronic ischemic heart disease", "Heart failure, unspecified"],
                "severity": "high"
            },
            
            # Diabetes related
            "diabetes": {
                "codes": ["E11.9", "E11.8", "E10.9"],
                "descriptions": ["Type 2 diabetes mellitus", "Type 2 diabetes with complications", "Type 1 diabetes mellitus"],
                "severity": "medium"
            },
            "high blood sugar": {
                "codes": ["R73.9", "R73.0"],
                "descriptions": ["Hyperglycemia, unspecified", "Abnormal glucose"],
                "severity": "medium"
            },
            
            # Respiratory
            "difficulty breathing": {
                "codes": ["R06.02", "R06.09", "J45.909"],
                "descriptions": ["Shortness of breath", "Other dyspnea", "Unspecified asthma"],
                "severity": "high"
            },
            "cough": {
                "codes": ["R05", "R05.9", "J02.9"],
                "descriptions": ["Cough", "Cough, unspecified", "Acute pharyngitis"],
                "severity": "low"
            },
            
            # Neurological
            "headache": {
                "codes": ["R51", "G44.209"],
                "descriptions": ["Headache", "Tension-type headache, unspecified"],
                "severity": "low"
            },
            "dizziness": {
                "codes": ["R42", "H81.9"],
                "descriptions": ["Dizziness and giddiness", "Unspecified vertigo"],
                "severity": "medium"
            },
            
            # Abdominal
            "stomach pain": {
                "codes": ["R10.9", "R10.0", "K29.1"],
                "descriptions": ["Unspecified abdominal pain", "Acute abdominal pain", "Dyspepsia"],
                "severity": "medium"
            },
            "nausea": {
                "codes": ["R11.0", "R11.2"],
                "descriptions": ["Nausea", "Vomiting, unspecified"],
                "severity": "low"
            },
            
            # Fever
            "fever": {
                "codes": ["R50.9", "R50.0"],
                "descriptions": ["Fever, unspecified", "Fever with chills"],
                "severity": "medium"
            },
            
            # Mental health
            "anxiety": {
                "codes": ["F41.9", "F41.1"],
                "descriptions": ["Anxiety, unspecified", "Generalized anxiety disorder"],
                "severity": "medium"
            },
            "depression": {
                "codes": ["F32.9", "F33.9"],
                "descriptions": ["Major depressive disorder, unspecified", "Major depressive disorder, recurrent"],
                "severity": "high"
            }
        }
    
    def extract_symptoms(self, text: str) -> List[str]:
        """Extract symptoms from text using keyword matching"""
        symptoms = []
        text_lower = text.lower()
        
        for symptom in self.icd10_mapping.keys():
            if symptom in text_lower:
                symptoms.append(symptom)
        
        return symptoms
    
    def generate_codes(self, symptoms: List[str]) -> Dict:
        """Generate ICD-10 codes for extracted symptoms"""
        codes = []
        severity_levels = []
        descriptions = []
        
        for symptom in symptoms:
            if symptom in self.icd10_mapping:
                mapping = self.icd10_mapping[symptom]
                codes.extend(mapping["codes"])
                severity_levels.append(mapping["severity"])
                descriptions.extend(mapping["descriptions"])
        
        return {
            "symptoms": symptoms,
            "icd10_codes": list(set(codes)),  # Remove duplicates
            "descriptions": descriptions,
            "severity_levels": list(set(severity_levels)),
            "requires_medical_attention": any(level == "high" for level in severity_levels)
        }
    
    def assess_complexity(self, symptoms: List[str], sentiment: Dict) -> Dict:
        """Assess if case requires medical professional consultation"""
        high_severity_symptoms = []
        complex_conditions = []
        
        for symptom in symptoms:
            if symptom in self.icd10_mapping:
                mapping = self.icd10_mapping[symptom]
                if mapping["severity"] == "high":
                    high_severity_symptoms.append(symptom)
        
        # Check for multiple symptoms
        if len(symptoms) > 3:
            complex_conditions.append("multiple_symptoms")
        
        # Check for negative sentiment indicating distress
        high_negative_sentiment = sentiment.get("negative", 0) > 0.7
        
        requires_consultation = (
            len(high_severity_symptoms) > 0 or 
            len(complex_conditions) > 0 or 
            high_negative_sentiment
        )
        
        return {
            "requires_consultation": requires_consultation,
            "high_severity_symptoms": high_severity_symptoms,
            "complex_conditions": complex_conditions,
            "high_negative_sentiment": high_negative_sentiment,
            "recommendation": self._generate_recommendation(requires_consultation, high_severity_symptoms)
        }
    
    def _generate_recommendation(self, requires_consultation: bool, high_severity_symptoms: List[str]) -> str:
        """Generate appropriate recommendation based on assessment"""
        if requires_consultation:
            if high_severity_symptoms:
                return f"Based on your symptoms including {', '.join(high_severity_symptoms)}, I recommend speaking with a medical professional for proper evaluation."
            else:
                return "Based on your condition, I recommend consulting with a healthcare professional for personalized medical advice."
        else:
            return "Your symptoms appear to be manageable. Thank you for sharing this information with TeleMER."
    
    def extract_family_member(self, text: str) -> Tuple[str, str]:
        """Extract family member and their condition from text"""
        text_lower = text.lower()
        
        # Family member patterns
        family_patterns = {
            "self": ["i have", "i'm experiencing", "i feel", "i'm suffering from", "my"],
            "mother": ["my mother", "my mom", "mother has", "mom has"],
            "father": ["my father", "my dad", "father has", "dad has"],
            "spouse": ["my husband", "my wife", "my spouse", "husband has", "wife has"],
            "child": ["my son", "my daughter", "my child", "son has", "daughter has"],
            "sibling": ["my brother", "my sister", "my sibling", "brother has", "sister has"]
        }
        
        identified_member = "self"  # Default to self
        condition_text = text
        
        for member, patterns in family_patterns.items():
            for pattern in patterns:
                if pattern in text_lower:
                    identified_member = member
                    # Extract condition after the family member reference
                    if member != "self":
                        pattern_index = text_lower.find(pattern)
                        if pattern_index != -1:
                            # Get text after the pattern
                            condition_start = pattern_index + len(pattern)
                            condition_text = text[condition_start:].strip()
                            # Remove common prefixes
                            condition_text = re.sub(r'^(has|is|is suffering from|is experiencing)\s+', '', condition_text, flags=re.IGNORECASE)
                    break
            if identified_member != "self":
                break
        
        return identified_member, condition_text
    
    def should_end_call(self, text: str, intent: str, symptoms: List[str]) -> bool:
        """Determine if the call should end based on user input"""
        text_lower = text.lower().strip()
        
        # Call ending phrases
        ending_phrases = [
            "no", "nothing", "none", "no issues", "no problems",
            "thank you", "thanks", "that's all", "that's all for now",
            "i'm fine", "i'm good", "everything is fine", "everything is good",
            "no medical issues", "no health issues", "no symptoms",
            "nothing to report", "nothing else", "that's everything"
        ]
        
        # Check for ending phrases
        for phrase in ending_phrases:
            if phrase in text_lower:
                return True
        
        # Check for "no" combined with medical context
        if intent == "nil_disclosure" and not symptoms:
            return True
        
        # Check for gratitude expressions
        gratitude_phrases = ["thank you", "thanks", "appreciate it"]
        for phrase in gratitude_phrases:
            if phrase in text_lower and len(text_lower.split()) <= 5:
                return True
        
        return False
    
    def create_family_medical_record(self, text: str) -> Dict:
        """Create medical record for family member"""
        member, condition = self.extract_family_member(text)
        symptoms = self.extract_symptoms(condition)
        medical_codes = self.generate_codes(symptoms)
        
        return {
            "family_member": member,
            "condition_text": condition,
            "symptoms": symptoms,
            "medical_codes": medical_codes,
            "timestamp": "current_call"
        }

medical_coder = MedicalCoder()
