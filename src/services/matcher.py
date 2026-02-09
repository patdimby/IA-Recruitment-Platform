# ==========================================
# 3. Module A: Intelligent Matching Engine
# ==========================================

from typing import List, Dict
from src.models import LocationEnum, CV, JobOffer

class MatchingEngine:
    """
    Moteur de calcul de score de compatibilité (Matching).

    Cette classe évalue la pertinence d'un candidat pour une offre spécifique
    en pondérant plusieurs critères (compétences, expérience, localisation).
    Le score final est un pourcentage entre 0 et 100.

    Attributs:
        weights (Dict[str, float]): Dictionnaire définissant le poids de chaque critère
                                    dans le calcul final (doit sommer à 1.0).
    """
    def __init__(self, weights: Dict[str, float] = None):
        # Poids par défaut
        self.weights = weights or {
            "skills": 0.5,
            "experience": 0.3,
            "location": 0.2
        }
    
    def _calculate_skill_score(self, cv_skills: List[str], required_skills: List[str]) -> float:
        """
        Calcule le score de correspondance des compétences techniques.

        Utilise le taux de rappel (Recall) : combien de compétences requises
        sont présentes dans le profil du candidat.

        Args:
            cv_skills (List[str]): Liste des compétences du candidat.
            required_skills (List[str]): Liste des compétences requises par l'offre.

        Returns:
            float: Score entre 0.0 et 1.0.
        """
        if not required_skills:
            return 1.0 # Pas de prérequis = 100%
        
        # Méthode simple : Rappel (Recall) -> Combien de requis sont possédés ?
        # On pourrait utiliser la similarité cosinus ici sur des embeddings
        required_set = set(s.lower() for s in required_skills)
        candidate_set = set(s.lower() for s in cv_skills)
        
        match_count = len(required_set.intersection(candidate_set))
        return match_count / len(required_set)

    def _calculate_experience_score(self, cv_exp: float, required_exp: float) -> float:
        """
        Calcule le score basé sur l'années d'expérience.

        Si le candidat a plus d'expérience que requis, le score est maximal (1.0).
        Sinon, le score est proportionnel au ratio (cv_exp / required_exp).

        Args:
            cv_exp (float): Années d'expérience du candidat.
            required_exp (float): Années d'expérience minimales requises.

        Returns:
            float: Score entre 0.0 et 1.0.
        """
        if cv_exp >= required_exp:
            return 1.0
        # Pénalité linéaire mais ne descend pas sous 0
        return max(0.0, cv_exp / required_exp)

    def _calculate_location_score(self, cv_loc: LocationEnum, job_loc: LocationEnum, remote_allowed: bool) -> float:
        """
        Calcule le score de compatibilité géographique.

        Args:
            cv_loc (LocationEnum): Localisation du candidat.
            job_loc (LocationEnum): Localisation du poste.
            remote_allowed (bool): True si l'offre autorise le télétravail.

        Returns:
            float: 1.0 si compatible, 0.0 sinon.
        """
        if cv_loc == job_loc:
            return 1.0
        if remote_allowed and cv_loc == LocationEnum.REMOTE:
            return 1.0
        return 0.0

    def compute_match(self, cv: CV, offer: JobOffer) -> float:
        """
        Calcule le score de compatibilité global (0-100) entre un CV et une offre.

        Agrège les sous-scores (skills, exp, location) en fonction des poids définis.

        Args:
            cv (CV): Objet CV du candidat.
            offer (JobOffer): Objet Offre de mission.

        Returns:
            float: Score global arrondi, sur une échelle de 0 à 100.
        """
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
        """
        Génère une explication textuelle lisible pour un recruteur humain.

        Analyse les écarts (compétences manquantes, manque d'expérience) pour
        justifier le score calculé.

        Args:
            cv (CV): Objet CV du candidat.
            offer (JobOffer): Objet Offre de mission.
            score (float): Le score calculé (utilisé pour déterminer le ton du message).

        Returns:
            str: Phrase explicative du score.
        """
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

