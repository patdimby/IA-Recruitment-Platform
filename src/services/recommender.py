# ==========================================
# 4. Module C: Recommendation System
# ==========================================

from services.matcher import MatchingEngine
from typing import List, Dict


class RecommendationSystem:
    """
    Système de recommandation et de classement (Ranking).

    Ce service prend en entrée une offre et une liste de candidats,
    calcule leur score de compatibilité via le MatchingEngine, puis
    les classe par ordre de pertinence décroissante.

    Attributs:
        matcher (MatchingEngine): Instance du moteur de matching utilisée pour le scoring.
    """
    def __init__(self, matcher: MatchingEngine):
        self.matcher = matcher

    def recommend_candidates(self, offer: JobOffer, candidates: List[CV], top_k: int = 5) -> List[Dict]:
        """
        Génère une liste recommandée des meilleurs candidats pour une offre donnée.

        Le processus inclut :
        1. Calcul du score de matching pour chaque candidat.
        2. Génération d'une explication textuelle.
        3. Tri décroissant par score.
        4. Limitation aux top_k résultats.

        Args:
            offer (JobOffer): L'offre pour laquelle on cherche des candidats.
            candidates (List[CV]): La liste de tous les candidats potentiels.
            top_k (int, optional): Nombre maximum de résultats à retourner. Defaults à 5.

        Returns:
            List[Dict]: Liste des dictionnaires contenant les détails du candidat recommandé,
                        le score et l'explication. Triée par pertinence.
        """
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

