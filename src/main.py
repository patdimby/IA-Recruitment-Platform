# ==========================================
# 5. Testing & Execution (Main)
# ==========================================

from dataclasses import dataclass, field

from src.models import JobOffer, LocationEnum
from src.services.analyzer import CVAnalyzer
from src.services.matcher import MatchingEngine
from src.services.recommender import RecommendationSystem

if __name__ == "__main__":
    # 1. Setup
    analyzer = CVAnalyzer()
    matcher = MatchingEngine()
    reco_system = RecommendationSystem(matcher)

    # 2. Définition d'une offre
    offre_data_scientist = JobOffer(
        id="JOB_001",
        title="Data Scientist Senior",
        required_skills=["python", "machine learning", "sql"],
        min_years_experience=5.0,
        location=LocationEnum.PARIS,
        remote_allowed=True
    )

    # 3. Simulation de parsing de CVs (Texte brut -> Objet CV)
    raw_cv_1 = "Développeur Python expérimenté avec 5 ans d'expérience en Machine Learning et SQL. Basé à Paris."
    raw_cv_2 = "Data Analyst junior. Je connais Python et Excel. 2 ans d'expérience. Je cherche du remote."
    raw_cv_3 = "Lead Data Engineer. 10 ans d'expérience. Java, Python, SQL, AWS. Basé à Lyon."

    cv1 = analyzer.parse_cv(raw_cv_1, "CAND_1")
    cv2 = analyzer.parse_cv(raw_cv_2, "CAND_2")
    cv3 = analyzer.parse_cv(raw_cv_3, "CAND_3")
    
    candidates_db = [cv1, cv2, cv3]

    print("--- RÉSULTATS DU TEST ---\n")

    # 4. Test Unitaire : Matching
    print(f"[TEST MATCHING] Comparaison {offre_data_scientist.title} vs {cv1.name}")
    score1 = matcher.compute_match(cv1, offre_data_scientist)
    print(f"Score attendu ~90 (Skills parfaits, Exp ok, Loc ok). Score obtenu : {score1}")
    print(f"Explication : {matcher.explain_score(cv1, offre_data_scientist, score1)}\n")

    # 5. Test Unitaire : Recommendation
    print(f"[TEST RECOMMANDATION] Top 3 candidats pour : {offre_data_scientist.title}")
    recommendations = reco_system.recommend_candidates(offre_data_scientist, candidates_db, top_k=3)
    
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. ID: {rec['cv_id']} | Score: {rec['score']} | Exp: {rec['explanation']}")

    # 6. Validation simple
    assert score1 > 85, "Le score pour CAND_1 devrait être élevé"
    assert recommendations[0]['cv_id'] == "CAND_1", "CAND_1 devrait être le top recommandé"
    
    print("\n--- SUITE DES TESTS : OK ---")