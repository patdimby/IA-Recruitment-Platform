# ==========================================
# 1. Data Structures (Mock Data)
# ==========================================

from dataclasses import dataclass
from typing import List
from enum import Enum

class LocationEnum(Enum):
    """
    Énumération des localisations possibles pour les candidats et les offres.
    
    Attributs:
        PARIS (str): Localisation Paris.
        LYON (str): Localisation Lyon.
        REMOTE (str): Télétravail / Remote.
    """
    PARIS = "Paris"
    LYON = "Lyon"
    REMOTE = "Remote"

@dataclass
class CV:
    """
    Modèle de données représentant le profil d'un candidat.

    Attributs:
        id (str): Identifiant unique du candidat dans le système.
        name (str): Nom complet du candidat.
        skills (List[str]): Liste des compétences techniques détectées (ex: python, sql).
        years_experience (float): Nombre total d'années d'expérience professionnelle.
        location (LocationEnum): Localisation géographique principale du candidat.
        availability_immediate (bool): Indique si le candidat est disponible immédiatement.
        raw_text (str): Texte brut extrait du CV original (utile pour re-traitement).
    """
    id: str
    name: str
    skills: List[str]
    years_experience: float
    location: LocationEnum
    availability_immediate: bool
    raw_text: str = "" # Pour simuler le texte du CV

    def __init__(
        self,
        id: str,
        name: str,
        skills: list[str],
        years_experience: float,
        location: LocationEnum,
        availability_immediate: bool,
        raw_text: str | None = None
    ):
        if years_experience < 0:
            raise ValueError("years_experience must be >= 0")

        self.id = id
        self.name = name

        # ✅ NORMALISATION ICI
        self.skills = [s.lower().strip() for s in skills]

        self.years_experience = years_experience
        self.location = location
        self.availability_immediate = availability_immediate
        self.raw_text = raw_text

@dataclass
class JobOffer:
    """
    Modèle de données représentant une offre de mission/emploi.

    Attributs:
        id (str): Identifiant unique de l'offre.
        title (str): Intitulé du poste (ex: Data Scientist).
        required_skills (List[str]): Liste des compétences techniques obligatoires ou recommandées.
        min_years_experience (float): Nombre d'années d'expérience minimum requises.
        location (LocationEnum): Localisation du poste.
        remote_allowed (bool): Indique si le télétravail est autorisé pour ce poste.
    """
    id: str
    title: str
    required_skills: List[str]
    min_years_experience: float
    location: LocationEnum
    remote_allowed: bool

    def __init__(
        self,
        id: str,
        title: str,
        required_skills: list[str],
        min_years_experience: float,
        location: LocationEnum,
        remote_allowed: bool
    ):
        if min_years_experience < 0:
            raise ValueError("min_years_experience must be >= 0")

        self.id = id
        self.title = title

        # ✅ NORMALISATION ICI
        self.required_skills = [s.lower().strip() for s in required_skills]

        self.min_years_experience = min_years_experience
        self.location = location
        self.remote_allowed = remote_allowed

    def __post_init__(self):
        """
        Méthode appelée automatiquement après la création de l'objet.
        Normalise les compétences en minuscule et supprime les doublons.
        """
        if self.skills:
            # On convertit tout en minuscule et on supprime les doublons (set)
            self.skills = list(set(s.lower() for s in self.skills))
        else:
            self.skills = []