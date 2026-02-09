# ==========================================
# 2. Module B: CV Analysis (Parser & Extractor)
# ==========================================

import re
import os
from src.models import LocationEnum, CV
from typing import List

# Imports des librairies (gestion d'erreur si non installées)
try:
    import pdfplumber
    from docx import Document
except ImportError:
    raise ImportError("Les librairies 'pdfplumber' et 'python-docx' sont requises.")
class CVAnalyzer:
    """
    Service responsable de l'extraction et de la structuration des données de CVs.

    Cette classe gère le pipeline de traitement : lecture de fichiers (PDF, DOCX),
    nettoyage du texte et extraction d'entités (compétences, expérience) basée
    sur des règles (Regex) et une taxonomie prédéfinie.

    Attributs:
        taxonomy (List[str]): Liste de référence des compétences à extraire (en minuscule).
    Simule l'extraction NLP d'un CV.
    Dans un cas réel, utiliserait spaCy/Transformers ici.
    """    
    def __init__(self):
        self.taxonomy = ["python", "java", "sql", "machine learning", "react", "aws", "excel"]

    
    @staticmethod
    def extract_years(text: str) -> float:
        # Recherche basique de patterns "X ans d'expérience"
        match = re.search(r'(\d+)\s*(ans|years|\+)', text, re.IGNORECASE)
        if match:
            return float(match.group(1))
        return 0.0
    
    def _extract_years(self, text: str) -> float:
        # Recherche basique de patterns "X ans d'expérience"
        match = re.search(r'(\d+)\s*(ans|years|\+)', text, re.IGNORECASE)
        if match:
            return float(match.group(1))
        return 0.0

    
    def _extract_skills(self, text: str) -> List[str]:
        """
        Extrait les compétences du texte en se basant sur la taxonomie de l'analyseur.
        
        Args:
            text (str): Texte du CV.
            
        Returns:
            List[str]: Liste des compétences trouvées.
        """
        text_lower = text.lower()
        found_skills = []
        # On parcourt la taxonomie définie dans __init__
        for skill in self.taxonomy:
            if skill in text_lower:
                found_skills.append(skill)
        return list(set(found_skills))
    
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

    def _read_docx(self, file_path: str) -> str:
        """
        Extrait le texte brut d'un fichier DOCX (Word).

        Args:
            file_path (str): Chemin vers le fichier DOCX.

        Returns:
            str: Texte extrait du document Word.
        """
        text = ""
        try:
            doc = Document(file_path)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            print(f"Erreur lecture DOCX {file_path}: {e}")
            return ""
        return text
    
    def parse_from_file(self, file_path: str, candidate_id: str) -> Optional[CV]:
        """
        Point d'entrée principal pour parser un CV depuis un fichier.

        Détecte l'extension du fichier (.pdf, .docx, .txt).
        """
        if not os.path.exists(file_path):
            print(f"Fichier introuvable : {file_path}")
            return None

        ext = os.path.splitext(file_path)[1].lower()
        
        text_content = ""
        if ext == ".pdf":
            text_content = self._read_pdf(file_path)
        elif ext == ".docx":
            text_content = self._read_docx(file_path)
        elif ext == ".txt":
            with open(file_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
        else:
            print(f"Format de fichier non supporté : {ext}")
            return None

        # Une fois le texte extrait, on utilise la logique NLP existante
        return self.parse_from_text(text_content, candidate_id)
    
    def _read_pdf(self, file_path: str) -> str:
        """
        Extrait le texte brut d'un fichier PDF.

        Args:
            file_path (str): Chemin vers le fichier PDF.

        Returns:
            str: Texte concaténé de toutes les pages du PDF.
        """
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"
        except Exception as e:
            print(f"Erreur lecture PDF {file_path}: {e}")
            return ""
        return text
    
    def parse_from_text(self, text: str, candidate_id: str) -> CV:
        """Logique NLP d'extraction de champs (comme avant)."""
        skills = self._extract_skills(text)
        exp = self._extract_years(text)
        loc = self._guess_location(text)

        # Appel correct pour récupérer un Enum
        loc = self._guess_location(text) 
        
        return CV(
            id=candidate_id,
            name="Candidat Extrait", 
            skills=skills,
            years_experience=exp,
            location=loc,
            availability_immediate=True,
            raw_text=text
        )
    
    def _guess_location(self, text: str):
        """
        Devine la localisation et retourne un Enum LocationEnum.
        
        Args:
            text (str): Texte du CV.
            
        Returns:
            LocationEnum: L'enum correspondant, ou PARIS par défaut.
        """
        text_lower = text.lower()
        if "paris" in text_lower:
            return LocationEnum.PARIS
        if "lyon" in text_lower:
            return LocationEnum.LYON
        if "remote" in text_lower or "télétravail" in text_lower:
            return LocationEnum.REMOTE
            
        # Valeur par défaut si rien n'est trouvé
        return LocationEnum.PARIS 