# ==========================================
# 3. Module A: Intelligent Matching Engine
# ==========================================

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum

class MatchingEngine:
    def __init__(self, weights: Dict[str, float] = None):
        # Poids par défaut
        self.weights = weights or {
            "skills": 0.5,
            "experience": 0.3,
            "location": 0.2
        }
    
    def _calculate_skill_score(self, cv_skills: List[str], required_skills: List[str]) -> float:
        if not required_skills:
            return 1.0 # Pas de prérequis = 100%
        
        # Méthode simple : Rappel (Recall) -> Combien de requis sont possédés ?
        # On pourrait utiliser la similarité cosinus ici sur des embeddings
        required_set = set(s.lower() for s in required_skills)
        candidate_set = set(s.lower() for s in cv_skills)
        
        match_count = len(required_set.intersection(candidate_set))
        return match_count / len(required_set)

    def _calculate_experience_score(self, cv_exp: float, required_exp: float) -> float:
        if cv_exp >= required_exp:
            return 1.0
        # Pénalité linéaire mais ne descend pas sous 0
        return max(0.0, cv_exp / required_exp)

    def _calculate_location_score(self, cv_loc: LocationEnum, job_loc: LocationEnum, remote_allowed: bool) -> float:
        if cv_loc == job_loc:
            return 1.0
        if remote_allowed and cv_loc == LocationEnum.REMOTE:
            return 1.0
        return 0.0

    def compute_match(self, cv: CV, offer: JobOffer) -> float:
        s_skill = self._calculate_skill_score(cv.skills, offer.required_skills)
        s_exp = self._calculate_experience_score(cv.years_experience, offer.min_years_experience)
        s_loc = self._calculate_location_score(cv.location, offer.location, offer.remote_allowed)
        
        score = (
            (s_skill * self.weights["skills"]) +
            (s_exp * self.weights["experience"]) +
            (s_loc * self.weights["location"])
        )
        
        return round(score * 100, 2) # Pourcentage

    def explain_score(self, cv: CV, offer: JobOffer, score: float) -> str:
        # Logique simple de génération de texte
        missing = set(offer.required_skills) - set(cv.skills)
        explanation = f"Score : {score}/100. "
        
        if score > 80:
            explanation += "Excellent match. "
        elif score > 50:
            explanation += "Match correct. "
        else:
            explanation += "Match faible. "
            
        if missing:
            explanation += f"Compétences manquantes : {', '.join(missing)}."
        if cv.years_experience < offer.min_years_experience:
            explanation += f" Expérience insuffisante ({cv.years_experience} ans vs {offer.min_years_experience} requis)."
            
        return explanation

