# ==========================================
# 1. Data Structures (Mock Data)
# ==========================================

from dataclasses import dataclass
from typing import List
from enum import Enum

class LocationEnum(Enum):
    PARIS = "Paris"
    LYON = "Lyon"
    REMOTE = "Remote"

@dataclass
class CV:
    id: str
    name: str
    skills: List[str]
    years_experience: float
    location: LocationEnum
    availability_immediate: bool
    raw_text: str = "" # Pour simuler le texte du CV

@dataclass
class JobOffer:
    id: str
    title: str
    required_skills: List[str]
    min_years_experience: float
    location: LocationEnum
    remote_allowed: bool
