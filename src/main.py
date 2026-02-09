# ==========================================
# 5. Testing & Execution (Main)
# ==========================================
"""
Main execution script for AI Recruitment Platform demonstration.

This script demonstrates the complete workflow:
1. Initialize all services (Analyzer, Matcher, Recommender)
2. Define sample job offers
3. Parse candidate CVs
4. Compute matching scores
5. Generate ranked recommendations

Usage:
    python main.py
"""

import logging
import sys
import os
from pathlib import Path

# Ajoute le dossier parent (la racine du projet) au chemin de recherche de Python
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models import JobOffer, LocationEnum
from services.analyzer import CVAnalyzer
from services.matcher import MatchingEngine
from services.recommender import RecommendationSystem

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('recruitment_demo.log')
    ]
)
logger = logging.getLogger(__name__)


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def main():
    """
    Main demonstration function.
    
    Executes a complete workflow showing:
    - CV parsing from text
    - Matching score calculation
    - Candidate ranking and recommendation
    """
    print_section("🤖 AI RECRUITMENT PLATFORM - DEMONSTRATION")
    
    # =========================================================================
    # 1. INITIALIZATION
    # =========================================================================
    print_section("1. Service Initialization")
    
    try:
        analyzer = CVAnalyzer()
        matcher = MatchingEngine()
        recommender = RecommendationSystem(matcher)
        print("✓ All services initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize services: {e}")
        sys.exit(1)
    
    # =========================================================================
    # 2. DEFINE JOB OFFER
    # =========================================================================
    print_section("2. Job Offer Definition")
    
    job_data_scientist = JobOffer(
        id="JOB_001",
        title="Data Scientist Senior",
        required_skills=["python", "machine learning", "sql"],
        min_years_experience=5.0,
        location=LocationEnum.PARIS,
        remote_allowed=True
    )
    
    print(f"Job ID: {job_data_scientist.id}")
    print(f"Title: {job_data_scientist.title}")
    print(f"Required Skills: {', '.join(job_data_scientist.required_skills)}")
    print(f"Min Experience: {job_data_scientist.min_years_experience} years")
    print(f"Location: {job_data_scientist.location.value}")
    print(f"Remote Allowed: {'Yes' if job_data_scientist.remote_allowed else 'No'}")
    
    # =========================================================================
    # 3. PARSE CANDIDATE CVs
    # =========================================================================
    print_section("3. CV Parsing & Extraction")
    
    # Sample CVs (raw text format)
    raw_cvs = {
        "CAND_1": (
            "Alice Dupont\n"
            "Développeur Python expérimenté avec 5 ans d'expérience en "
            "Machine Learning et SQL. Basé à Paris. Disponible immédiatement."
        ),
        "CAND_2": (
            "Bob Martin\n"
            "Data Analyst junior. Je connais Python et Excel. "
            "2 ans d'expérience. Je cherche du remote."
        ),
        "CAND_3": (
            "Charlie Bernard\n"
            "Lead Data Engineer. 10 ans d'expérience. "
            "Java, Python, SQL, AWS. Basé à Lyon."
        )
    }
    
    candidates = []
    
    for candidate_id, raw_text in raw_cvs.items():
        try:
            cv = analyzer.parse_from_text(raw_text, candidate_id)
            candidates.append(cv)
            
            print(f"\n✓ Parsed {candidate_id}:")
            print(f"  Name: {cv.name}")
            print(f"  Skills: {', '.join(cv.skills) if cv.skills else 'None detected'}")
            print(f"  Experience: {cv.years_experience} years")
            print(f"  Location: {cv.location.value}")
            
        except Exception as e:
            logger.error(f"Failed to parse CV {candidate_id}: {e}")
            continue
    
    if not candidates:
        logger.error("No candidates were successfully parsed. Exiting.")
        sys.exit(1)
    
    # =========================================================================
    # 4. INDIVIDUAL MATCHING TEST
    # =========================================================================
    print_section("4. Individual Matching Score Test")
    
    test_candidate = candidates[0]  # Alice Dupont
    
    print(f"\nTesting match: {job_data_scientist.title} vs {test_candidate.name}")
    print(f"Expected: ~90-100 (perfect skills, experience OK, location match)")
    
    try:
        score = matcher.compute_match(test_candidate, job_data_scientist)
        explanation = matcher.explain_score(test_candidate, job_data_scientist, score)
        
        print(f"\n✓ Score Obtained: {score}/100")
        print(f"✓ Explanation: {explanation}")
        
    except Exception as e:
        logger.error(f"Matching failed: {e}")
    
    # =========================================================================
    # 5. RECOMMENDATION SYSTEM TEST
    # =========================================================================
    print_section("5. Candidate Recommendation Ranking")
    
    print(f"\nGenerating top 3 candidates for: {job_data_scientist.title}")
    
    try:
        recommendations = recommender.recommend_candidates(
            job_data_scientist, 
            candidates, 
            top_k=3
        )
        
        print(f"\n{'Rank':<6} {'ID':<12} {'Name':<20} {'Score':<10} {'Explanation'}")
        print("-" * 100)
        
        for i, rec in enumerate(recommendations, 1):
            print(
                f"{i:<6} {rec['cv_id']:<12} {rec['cv_name']:<20} "
                f"{rec['score']:<10.2f} {rec['explanation']}"
            )
        
    except Exception as e:
        logger.error(f"Recommendation failed: {e}")
        sys.exit(1)
    
    # =========================================================================
    # 6. VALIDATION CHECKS
    # =========================================================================
    print_section("6. Validation & Assertions")
    
    try:
        # Test 1: Top candidate should have high score
        assert recommendations[0]['score'] >= 80, \
            f"Top candidate score too low: {recommendations[0]['score']}"
        print("✓ Test 1 Passed: Top candidate has score >= 80")
        
        # Test 2: Candidates should be sorted by score
        scores = [rec['score'] for rec in recommendations]
        assert scores == sorted(scores, reverse=True), \
            "Candidates are not sorted by score"
        print("✓ Test 2 Passed: Candidates are properly sorted")
        
        # Test 3: Alice (CAND_1) should be top recommendation
        assert recommendations[0]['cv_id'] == "CAND_1", \
            f"Expected CAND_1 as top, got {recommendations[0]['cv_id']}"
        print("✓ Test 3 Passed: CAND_1 is the top recommendation")
        
        print("\n✅ All validation checks passed!")
        
    except AssertionError as e:
        logger.error(f"Validation failed: {e}")
        sys.exit(1)
    
    # =========================================================================
    # 7. SUMMARY
    # =========================================================================
    print_section("7. Demonstration Summary")
    
    print(f"""
✓ Services Initialized: 3 (Analyzer, Matcher, Recommender)
✓ CVs Parsed: {len(candidates)}
✓ Matching Scores Calculated: {len(candidates)}
✓ Recommendations Generated: {len(recommendations)}
✓ Validation Tests Passed: 3/3

The AI Recruitment Platform demonstration completed successfully!
Check 'recruitment_demo.log' for detailed execution logs.
    """)
    
    return 0


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nDemonstration interrupted by user.")
        sys.exit(130)
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        sys.exit(1)
