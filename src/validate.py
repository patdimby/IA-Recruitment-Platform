"""
Simple validation script (no pytest required).

This script validates the core functionality without external dependencies.
For full test suite, install pytest and run: pytest tests/ -v
"""

import sys
import os
from pathlib import Path

# Ajoute le dossier parent (la racine du projet) au chemin de recherche de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import JobOffer, CV, LocationEnum
from services.analyzer import CVAnalyzer
from services.matcher import MatchingEngine
from services.recommender import RecommendationSystem

def test_cv_analyzer():
    """Test CV Analyzer functionality."""
    print("\n🔍 Testing CV Analyzer...")
    
    analyzer = CVAnalyzer()
    
    # Test 1: Extract years
    text = "5 ans d'expérience en développement"
    years = analyzer.extract_years(text)
    assert years == 5.0, f"Expected 5.0, got {years}"
    print("  ✓ Extract years: PASSED")
    
    # Test 2: Extract skills
    text = "Je connais Python, SQL et React"
    skills = analyzer._extract_skills(text)
    assert "python" in skills and "sql" in skills and "react" in skills
    print("  ✓ Extract skills: PASSED")
    
    # Test 3: Parse from text
    cv_text = "Alice Dupont\nPython developer with 5 years in Paris"
    cv = analyzer.parse_from_text(cv_text, "TEST_001")
    assert cv.id == "TEST_001"
    assert cv.years_experience == 5.0
    assert "python" in cv.skills
    print("  ✓ Parse from text: PASSED")
    
    print("✅ CV Analyzer: ALL TESTS PASSED")


def test_matching_engine():
    """Test Matching Engine functionality."""
    print("\n🎯 Testing Matching Engine...")
    
    engine = MatchingEngine()
    
    # Test 1: Perfect match
    cv = CV(
        id="C1",
        name="Test",
        skills=["python", "sql", "machine learning"],
        years_experience=6.0,
        location=LocationEnum.PARIS,
        availability_immediate=True
    )
    
    job = JobOffer(
        id="J1",
        title="Data Scientist",
        required_skills=["python", "sql", "machine learning"],
        min_years_experience=5.0,
        location=LocationEnum.PARIS,
        remote_allowed=False
    )
    
    score = engine.compute_match(cv, job)
    assert score == 100.0, f"Expected 100.0, got {score}"
    print("  ✓ Perfect match: PASSED")
    
    # Test 2: Partial match
    cv2 = CV(
        id="C2",
        name="Test2",
        skills=["python", "sql"],  # Missing ML
        years_experience=3.0,  # Less experience
        location=LocationEnum.PARIS,
        availability_immediate=True
    )
    
    score2 = engine.compute_match(cv2, job)
    assert score2 < 100.0, f"Score should be less than 100, got {score2}"
    assert score2 > 0.0, f"Score should be positive, got {score2}"
    print("  ✓ Partial match: PASSED")
    
    # Test 3: Explanation
    explanation = engine.explain_score(cv, job, score)
    assert "Score" in explanation
    print("  ✓ Explanation generation: PASSED")
    
    print("✅ Matching Engine: ALL TESTS PASSED")


def test_recommendation_system():
    """Test Recommendation System functionality."""
    print("\n🏆 Testing Recommendation System...")
    
    matcher = MatchingEngine()
    recommender = RecommendationSystem(matcher)
    
    job = JobOffer(
        id="J1",
        title="Data Scientist",
        required_skills=["python", "machine learning"],
        min_years_experience=5.0,
        location=LocationEnum.PARIS,
        remote_allowed=True
    )
    
    cv1 = CV(
        id="C1",
        name="Perfect",
        skills=["python", "machine learning", "sql"],
        years_experience=6.0,
        location=LocationEnum.PARIS,
        availability_immediate=True
    )
    
    cv2 = CV(
        id="C2",
        name="Junior",
        skills=["python"],
        years_experience=2.0,
        location=LocationEnum.PARIS,
        availability_immediate=True
    )
    
    candidates = [cv2, cv1]  # Intentionally wrong order
    
    # Test 1: Ranking order
    results = recommender.recommend_candidates(job, candidates, top_k=2)
    assert results[0]['cv_id'] == "C1", f"Expected C1 first, got {results[0]['cv_id']}"
    assert results[1]['cv_id'] == "C2", f"Expected C2 second, got {results[1]['cv_id']}"
    print("  ✓ Ranking order: PASSED")
    
    # Test 2: Top-k limit
    results = recommender.recommend_candidates(job, candidates, top_k=1)
    assert len(results) == 1, f"Expected 1 result, got {len(results)}"
    print("  ✓ Top-k limit: PASSED")
    
    # Test 3: Result structure
    result = results[0]
    assert 'cv_id' in result
    assert 'score' in result
    assert 'explanation' in result
    print("  ✓ Result structure: PASSED")
    
    print("✅ Recommendation System: ALL TESTS PASSED")


def test_data_models():
    """Test data models."""
    print("\n📦 Testing Data Models...")
    
    # Test 1: CV creation
    cv = CV(
        id="TEST",
        name="Test User",
        skills=["Python", "SQL"],  # Will be normalized
        years_experience=5.0,
        location=LocationEnum.PARIS,
        availability_immediate=True
    )
    assert "python" in cv.skills, "Skills should be normalized to lowercase"
    print("  ✓ CV creation & normalization: PASSED")
    
    # Test 2: JobOffer creation
    job = JobOffer(
        id="JOB",
        title="Developer",
        required_skills=["Python"],
        min_years_experience=3.0,
        location=LocationEnum.PARIS,
        remote_allowed=True
    )
    assert "python" in job.required_skills
    print("  ✓ JobOffer creation & normalization: PASSED")
    
    # Test 3: Validation
    try:
        bad_cv = CV(
            id="BAD",
            name="Bad",
            skills=[],
            years_experience=-1.0,  # Should raise error
            location=LocationEnum.PARIS,
            availability_immediate=True
        )
        assert False, "Should have raised ValueError"
    except ValueError:
        print("  ✓ Validation (negative experience): PASSED")
    
    print("✅ Data Models: ALL TESTS PASSED")


def main():
    """Run all validation tests."""
    print("=" * 70)
    print("  🧪 RUNNING VALIDATION TESTS")
    print("=" * 70)
    
    try:
        test_data_models()
        test_cv_analyzer()
        test_matching_engine()
        test_recommendation_system()
        
        print("\n" + "=" * 70)
        print("  ✅ ALL VALIDATION TESTS PASSED! ✅")
        print("=" * 70)
        print("\nFor full test suite with coverage, install pytest:")
        print("  pip install pytest pytest-cov")
        print("  pytest tests/ -v --cov=src")
        
        return 0
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
