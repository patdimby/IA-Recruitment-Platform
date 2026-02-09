# ==========================================
# 2. Module B: CV Analysis (Parser & Extractor)
# ==========================================

import re
from src.models import LocationEnum, CV
from typing import List

class CVAnalyzer:
    """
    Simule l'extraction NLP d'un CV.
    Dans un cas réel, utiliserait spaCy/Transformers ici.
    """
    
    @staticmethod
    def extract_years(text: str) -> float:
        # Recherche basique de patterns "X ans d'expérience"
        match = re.search(r'(\d+)\s*(ans|years|\+)', text, re.IGNORECASE)
        if match:
            return float(match.group(1))
        return 0.0

    @staticmethod
    def extract_skills(text: str, known_skills_db: List[str]) -> List[str]:
        found_skills = []
        text_lower = text.lower()
        for skill in known_skills_db:
            # Normalisation simple
            if skill.lower() in text_lower:
                found_skills.append(skill)
        return list(set(found_skills)) # Unique

    def parse_cv(self, cv_text: str, candidate_id: str) -> CV:
        # Base de données de compétences connues (Mock de taxonomie)
        taxonomy = ["python", "java", "sql", "machine learning", "react", "aws", "excel"]
        
        skills = self.extract_skills(cv_text, taxonomy)
        exp = self.extract_years(cv_text)
        
        # Simulation localisation (dans un vrai cas, NER pour lieux)
        loc = LocationEnum.PARIS if "paris" in cv_text.lower() else LocationEnum.REMOTE
        
        return CV(
            id=candidate_id,
            name="Candidat Inconnu",
            skills=skills,
            years_experience=exp,
            location=loc,
            availability_immediate=True, # Par défaut
            raw_text=cv_text
        )
