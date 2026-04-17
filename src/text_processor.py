import spacy
import re
from typing import List, Set

class TextProcessor:
    def __init__(self):
        """Initialize spaCy model"""
        self.nlp = spacy.load("en_core_web_sm")
        
        # Common skill keywords database
        self.technical_skills = {
            'python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby', 'go',
            'sql', 'mongodb', 'postgresql', 'mysql', 'redis', 'elasticsearch',
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins',
            'react', 'vue', 'angular', 'node.js', 'express', 'django',
            'machine learning', 'deep learning', 'nlp', 'computer vision',
            'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy',
            'rest api', 'graphql', 'microservices', 'agile', 'scrum',
            'git', 'linux', 'unix', 'windows', 'macos'
        }
        
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Convert to lowercase
        text = text.lower()
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-z0-9\s\+\#\.]', ' ', text)
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def extract_entities(self, text: str) -> dict:
        """Extract named entities and important information"""
        doc = self.nlp(text)
        
        entities = {
            'PERSON': [],
            'ORG': [],
            'GPE': [],
            'SKILL': []
        }
        
        for ent in doc.ents:
            if ent.label_ in entities:
                entities[ent.label_].append(ent.text)
        
        return entities
    
    def extract_keywords(self, text: str) -> Set[str]:
        """Extract important keywords from text"""
        cleaned_text = self.clean_text(text)
        doc = self.nlp(cleaned_text)
        
        # Extract keywords: nouns, verbs, and technical terms
        keywords = set()
        
        for token in doc:
            # Include nouns, verbs, and adjectives
            if token.pos_ in ['NOUN', 'VERB', 'ADJ']:
                keywords.add(token.text)
            # Check if word is in technical skills
            elif any(skill in token.text for skill in self.technical_skills):
                keywords.add(token.text)
        
        # Add multi-word skills detection
        text_lower = text.lower()
        for skill in self.technical_skills:
            if skill in text_lower:
                keywords.add(skill)
        
        return keywords
    
    def extract_skills(self, text: str) -> Set[str]:
        """Extract technical and soft skills"""
        text_lower = text.lower()
        found_skills = set()
        
        for skill in self.technical_skills:
            if skill in text_lower:
                found_skills.add(skill)
        
        return found_skills
    
    def tokenize_sentences(self, text: str) -> List[str]:
        """Break text into sentences"""
        doc = self.nlp(text)
        return [sent.text for sent in doc.sents]


# Example usage
if __name__ == "__main__":
    processor = TextProcessor()
    
    sample_text = "I have 5 years of Python and JavaScript experience with React"
    print("Keywords:", processor.extract_keywords(sample_text))
    print("Skills:", processor.extract_skills(sample_text))