import pytest
from src.models import CV, JobOffer, LocationEnum
from src.services.analyzer import CVAnalyzer
from src.services.matcher import MatchingEngine
from src.services.recommender import RecommendationSystem

# ==========================================
# FIXTURES (Données de test réutilisables)
# ==========================================

@pytest.fixture
def sample_job_offer():
    """Une offre de référence pour les tests."""
    return JobOffer(
        id="JOB_101",
        title="Data Scientist",
        required_skills=["python", "machine learning", "sql"],
        min_years_experience=5.0,
        location=LocationEnum.PARIS,
        remote_allowed=True
    )

@pytest.fixture
def perfect_candidate():
    """Un candidat qui correspond parfaitement à l'offre."""
    return CV(
        id="CAND_PERFECT",
        name="Alice Wonder",
        skills=["python", "machine learning", "sql", "tensorflow"],
        years_experience=6.0,
        location=LocationEnum.PARIS,
        availability_immediate=True
    )

@pytest.fixture
def junior_candidate():
    """Un candidat junior (manque d'expérience)."""
    return CV(
        id="CAND_JUNIOR",
        name="Bob Junior",
        skills=["python", "sql"],
        years_experience=2.0,
        location=LocationEnum.PARIS,
        availability_immediate=True
    )

@pytest.fixture
def remote_candidate():
    """Un candidat en remote (teste la logique géographique)."""
    return CV(
        id="CAND_REMOTE",
        name="Charlie Remote",
        skills=["python", "machine learning", "sql"],
        years_experience=5.0,
        location=LocationEnum.REMOTE,
        availability_immediate=True
    )

# ==========================================
# TESTS MODULE A & B : ANALYZER & MATCHING
# ==========================================

class TestCVAnalyzer:
    
    def test_extract_years_valid(self):
        """Test l'extraction correcte des années d'expérience."""
        text = "J'ai 5 ans d'expérience en développement."
        analyzer = CVAnalyzer()
        assert analyzer.extract_years(text) == 5.0

    def test_extract_years_invalid(self):
        """Test l'extraction quand aucune année n'est mentionnée."""
        text = "Je suis un développeur passionné."
        analyzer = CVAnalyzer()
        assert analyzer.extract_years(text) == 0.0

    def test_extract_skills_intersection(self):
        """Test que seules les compétences de la taxonomie sont extraites."""
        text = "Je connais python, java et excel."
        taxonomy = ["python", "sql", "java"]
        analyzer = CVAnalyzer()
        skills = analyzer.extract_skills(text, taxonomy)
        
        # 'excel' ne devrait pas être là car pas dans la taxonomy
        assert set(skills) == {"python", "java"}
        assert len(skills) == 2

class TestMatchingEngine:

    def test_perfect_match_score(self, perfect_candidate, sample_job_offer):
        """Test qu'un match parfait donne un score de 100."""
        engine = MatchingEngine()
        score = engine.compute_match(perfect_candidate, sample_job_offer)
        assert score == 100.0

    def test_junior_penalty(self, junior_candidate, sample_job_offer):
        """Test la pénalité sur l'expérience."""
        engine = MatchingEngine()
        score = engine.compute_match(junior_candidate, sample_job_offer)
        
        # Le score doit être plus bas que 100 à cause du manque d'expérience (2 vs 5 ans)
        # Et des compétences manquantes (Machine Learning)
        assert score < 80.0
        # Mais > 0 car les compétences partielles correspondent
        assert score > 0.0

    def test_skill_matching_logic(self, junior_candidate, sample_job_offer):
        """Test spécifique sur le calcul des compétences."""
        engine = MatchingEngine()
        
        # Candidat a python, sql (2/3 requis)
        skill_score = engine._calculate_skill_score(
            junior_candidate.skills, 
            sample_job_offer.required_skills
        )
        
        # On attend 0.667 (2/3) avec une tolérance de 0.01 au lieu de 0.66
        assert skill_score == pytest.approx(0.667, 0.01)

    def test_remote_allowed_logic(self, remote_candidate, sample_job_offer):
        """Test que le remote est accepté si l'offre le permet."""
        engine = MatchingEngine()
        
        # Si l'offre autorise le remote et que le candidat est remote -> Score loc = 1
        # Ici remote_allowed=True dans la fixture
        score = engine.compute_match(remote_candidate, sample_job_offer)
        
        # Comme skills et exp sont parfaits pour remote_candidate, le score doit être 100
        assert score == 100.0

    def test_location_rejection(self, remote_candidate):
        """Test le rejet si localisation incompatible."""
        # Offre qui n'accepte PAS le remote
        local_offer = JobOffer(
            id="JOB_LOCAL", title="Dev", required_skills=[], min_years_experience=0,
            location=LocationEnum.PARIS, remote_allowed=False
        )
        engine = MatchingEngine()
        
        score = engine.compute_match(remote_candidate, local_offer)
        # La localisation doit faire chuter le score à cause du poids 0.2
        # Si tout le reste est parfait (1.0), le score sera 0.8
        assert score == 80.0

# ==========================================
# TESTS MODULE C : RECOMMANDATION
# ==========================================

class TestRecommendationSystem:

    def test_ranking_order(self, sample_job_offer, perfect_candidate, junior_candidate):
        """Test que les candidats sont bien triés par score décroissant."""
        matcher = MatchingEngine()
        reco = RecommendationSystem(matcher)
        
        # On met le junior en premier dans la liste pour voir s'il est bien remonté après
        candidates = [junior_candidate, perfect_candidate]
        
        results = reco.recommend_candidates(sample_job_offer, candidates, top_k=2)
        
        # Le premier résultat doit être le candidat parfait (score 100)
        assert results[0]['cv_id'] == perfect_candidate.id
        assert results[0]['score'] == 100.0
        
        # Le second doit être le junior
        assert results[1]['cv_id'] == junior_candidate.id
        assert results[1]['score'] < results[0]['score']

    def test_top_k_limit(self, sample_job_offer, perfect_candidate, junior_candidate, remote_candidate):
        """Test que le système ne renvoie que le nombre demandé de résultats."""
        matcher = MatchingEngine()
        reco = RecommendationSystem(matcher)
        
        candidates = [perfect_candidate, junior_candidate, remote_candidate]
        
        # On demande top 1
        results = reco.recommend_candidates(sample_job_offer, candidates, top_k=1)
        
        assert len(results) == 1
        # Celui avec le meilleur score (Perfect ou Remote sont tous deux à 100, l'ordre dépend du tri stable de python)
        assert results[0]['score'] == 100.0