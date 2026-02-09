# ==========================================
# 4. Module C: Recommendation System
# ==========================================

import re
import math
from matcher import MatchingEngine
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum

class RecommendationSystem:
    def __init__(self, matcher: MatchingEngine):
        self.matcher = matcher

    def recommend_candidates(self, offer: JobOffer, candidates: List[CV], top_k: int = 5) -> List[Dict]:
        results = []
        
        for cv in candidates:
            score = self.matcher.compute_match(cv, offer)
            
            # Ici, on pourrait ajouter un facteur de "Popularité" ou "Click-through rate" historique
            # final_score = score * 0.9 + popularity_factor * 0.1
            
            explanation = self.matcher.explain_score(cv, offer, score)
            
            results.append({
                "cv_id": cv.id,
                "score": score,
                "explanation": explanation,
                "cv_obj": cv
            })
            
        # Tri décroissant
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

