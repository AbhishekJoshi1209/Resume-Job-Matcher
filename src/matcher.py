import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, Tuple, List
from src.text_processor import TextProcessor
from src.embeddings import EmbeddingGenerator

class ResumeMatcher:
    def __init__(self):
        """Initialize the matcher with processor and embeddings"""
        self.processor = TextProcessor()
        self.embeddings = EmbeddingGenerator()
    
    def calculate_skill_match(self, resume_skills: set, job_skills: set) -> Tuple[float, set]:
        """
        Calculate skill matching score
        
        Returns:
            - Match percentage (0-100)
            - Missing skills set
        """
        if not job_skills:
            return 100.0, set()
        
        matching_skills = resume_skills.intersection(job_skills)
        match_percentage = (len(matching_skills) / len(job_skills)) * 100
        missing_skills = job_skills - resume_skills
        
        return match_percentage, missing_skills
    
    def calculate_semantic_similarity(self, resume_text: str, job_text: str) -> float:
        """
        Calculate semantic similarity using embeddings
        Returns value between 0-100
        """
        # Generate embeddings
        resume_embedding = self.embeddings.generate_embedding(resume_text)
        job_embedding = self.embeddings.generate_embedding(job_text)
        
        # Reshape for cosine similarity
        resume_embedding = resume_embedding.reshape(1, -1)
        job_embedding = job_embedding.reshape(1, -1)
        
        # Calculate cosine similarity
        similarity = cosine_similarity(resume_embedding, job_embedding)[0][0]
        
        # Convert to percentage (0-100)
        return float(similarity * 100)
    
    def calculate_keyword_overlap(self, resume_keywords: set, job_keywords: set) -> Tuple[float, int]:
        """
        Calculate keyword overlap percentage
        
        Returns:
            - Overlap percentage (0-100)
            - Number of matching keywords
        """
        if not job_keywords:
            return 100.0, 0
        
        matching_keywords = resume_keywords.intersection(job_keywords)
        overlap_percentage = (len(matching_keywords) / len(job_keywords)) * 100
        
        return overlap_percentage, len(matching_keywords)
    
    def match_resume_to_job(self, resume_text: str, job_text: str) -> Dict:
        """
        Complete matching analysis
        
        Returns comprehensive matching report
        """
        # Extract skills
        resume_skills = self.processor.extract_skills(resume_text)
        job_skills = self.processor.extract_skills(job_text)
        
        # Extract keywords
        resume_keywords = self.processor.extract_keywords(resume_text)
        job_keywords = self.processor.extract_keywords(job_text)
        
        # Calculate different match scores
        skill_match, missing_skills = self.calculate_skill_match(resume_skills, job_skills)
        semantic_match = self.calculate_semantic_similarity(resume_text, job_text)
        keyword_match, matching_count = self.calculate_keyword_overlap(resume_keywords, job_keywords)
        
        # Weighted overall score
        # Skills: 40%, Semantic: 35%, Keywords: 25%
        overall_score = (
            skill_match * 0.40 +
            semantic_match * 0.35 +
            keyword_match * 0.25
        )
        
        result = {
            'overall_match_score': round(overall_score, 2),
            'skill_match_score': round(skill_match, 2),
            'semantic_match_score': round(semantic_match, 2),
            'keyword_match_score': round(keyword_match, 2),
            'resume_skills': list(resume_skills),
            'job_skills': list(job_skills),
            'matching_skills': list(resume_skills.intersection(job_skills)),
            'missing_skills': list(missing_skills),
            'matching_keywords_count': matching_count,
            'total_job_keywords': len(job_keywords),
            'match_percentage': round((matching_count / len(job_keywords) * 100) if job_keywords else 100, 2),
            'resume_skill_count': len(resume_skills),
            'job_requirement_count': len(job_skills)
        }
        
        return result


# Example usage
if __name__ == "__main__":
    matcher = ResumeMatcher()
    
    resume = """
    Senior Python Developer
    5 years of experience in Python, JavaScript, React
    Strong background in SQL, PostgreSQL, MongoDB
    AWS and Docker expertise
    Led multiple agile teams
    """
    
    job_desc = """
    Python Developer Required
    Requirements:
    - 3+ years Python experience
    - JavaScript and React knowledge
    - SQL and PostgreSQL
    - AWS deployment experience
    - Docker and Kubernetes
    - Machine Learning knowledge
    """
    
    result = matcher.match_resume_to_job(resume, job_desc)
    
    print("=== MATCH REPORT ===")
    print(f"Overall Match: {result['overall_match_score']}%")
    print(f"Missing Skills: {result['missing_skills']}")