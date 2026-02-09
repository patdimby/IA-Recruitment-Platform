🤖 IA Recruitment Platform
Ce projet est une implémentation technique visant à démontrer la conception d'un système de matching intelligent pour une plateforme de recrutement. Il couvre l'analyse automatique de CVs, le calcul de score de compatibilité et la génération de recommandations.

🎯 Objectifs
L'objectif principal est de fournir une architecture claire et scalable pour répondre à un besoin métier concret : améliorer la qualité du matching candidats-offres grâce à l'IA.

🏗️ Architecture
Le système est conçu selon une architecture modulaire, séparant les responsabilités entre l'ingestion de données, le calcul de score et la recommandation.

graph TD    User[Recruteur / Candidat] -->|API Rest| API[Backend API Gateway]        subgraph "Backend Layer"        API --> ServiceIA[Service IA (Python)]        API --> DB[(PostgreSQL)]    end        subgraph "AI & Data Layer"        ServiceIA --> Parser[CV Parser Module]        ServiceIA --> Matcher[Matching Engine]        ServiceIA --> LLM[LLM Service (Explications)]                Parser --> VectorDB[(Vector DB - Embeddings)]        Matcher --> VectorDB    end        ServiceIA --> DB    ServiceIA --> VectorDB
🛠️ Stack Technique
Langage : Python 3.9+
NLP : spaCy (pour l'analyse syntaxique et l'extraction d'entités).
Algorithmes : Méthodes hybrides (Règles métier + Similarité vectorielle Cosine).
Base de données (Simulée) : Vector DB (Qdrant/Milvus concept) + PostgreSQL.
✨ Fonctionnalités
A. Matching Intelligent
Calcul d'un score de compatibilité (0-100) basé sur une pondération de critères :

Hard Skills : Jaccard index ou similarité sémantique.
Expérience : Comparaison ratio (années candidat / années requises).
Localisation : Filtre géographique.
B. Analyse Automatique de CV
Pipeline de traitement (ETL) :

Ingestion : Upload fichier.
Parsing : Extraction textuelle.
Extraction : Identification des compétences, dates et localisation via NLP.
C. Recommandation
Système de ranking (Learning to Rank conceptual) qui :

Classe les candidats par score de pertinence.
Intègre des signaux comportementaux (clics, masquages) pour réajuster le score final.
🚀 Installation & Démarrage
Prérequis
Python 3.9 ou supérieur
pip ou poetry
Étapes
Cloner le dépôt
bash

git clone https://github.com/VOTRE_PSEUDO/ai-recruitment-platform.git
cd ai-recruitment-platform
Créer l'environnement virtuel
bash

python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
Installer les dépendances
bash

pip install -r requirements.txt
Lancer la démonstration
bash

python src/main.py
🧪 Tests
Le projet inclut des tests unitaires pour valider la logique de matching.

bash

pytest tests/ -v
📂 Structure du Projet
text

.
├── src/
│   ├── models.py          # Modèles de données (CV, JobOffer)
│   ├── services/          # Cœur de l'IA
│   │   ├── analyzer.py    # Analyse NLP
│   │   ├── matcher.py     # Calcul de score
│   │   └── recommender.py # Ranking
│   └── main.py            # Exécution de démo
├── tests/                 # Tests unitaires
├── data/                  # Jeux de données de test
└── README.md
💡 Exemple de Résultat
L'exécution du script main.py produit une sortie console similaire à celle-ci :

text

--- RÉSULTATS DU TEST ---

[TEST MATCHING] Comparaison Data Scientist Senior vs Candidat Inconnu
Score attendu ~90 (Skills parfaits, Exp ok, Loc ok). Score obtenu : 91.66
Explication : Score : 91.66/100. Excellent match. 

[TEST RECOMMANDATION] Top 3 candidats pour : Data Scientist Senior
1. ID: CAND_1 | Score: 91.66 | Exp: Excellent match. 
2. ID: CAND_3 | Score: 75.0 | Exp: Match correct. Compétences manquantes : machine learning.
3. ID: CAND_2 | Score: 40.0 | Exp: Match faible. Compétences manquantes : machine learning, sql.
🔮 Améliorations Futures
LLM Integration : Utiliser GPT-4 ou Llama 2 pour générer des résumés de CV plus nuancés et des explications de rejet plus diplomates.
Vector Store réel : Remplacer l'implémentation en mémoire par Qdrant ou Pinecone.
API FastAPI : Exposer le moteur de matching via une API REST.
👤 Auteur
[RANOELISON Dimbisoa Patrick] - Développeur IA / Data Engineer