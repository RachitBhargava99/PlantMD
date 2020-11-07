from pydantic import BaseModel

from datetime import datetime
from typing import List, Optional


# ===================================
# Disease Models start here
# ===================================
class DiseaseBase(BaseModel):
    name: str
    scientific_name: str
    fruit: str


class DiseaseCreate(DiseaseBase):
    class Config:
        orm_mode = True


class Disease(DiseaseBase):
    id: int

    class Config:
        orm_mode = True


class DiseaseList(BaseModel):
    diseases: List[Disease]


# ===================================
# Symptom Models start here
# ===================================
class SymptomBase(BaseModel):
    name: str
    affected_part: str


class SymptomCreate(SymptomBase):
    class Config:
        orm_mode = True


class Symptom(SymptomBase):
    id: int

    class Config:
        orm_mode = True


class SymptomList(BaseModel):
    diseases: List[Symptom]


# ===================================
# Symptom-Disease Linkage Models start here
# ===================================
class SymptomDiseaseLinkBase(BaseModel):
    disease_id: int
    symptom_id: int


class SymptomDiseaseLinkCreate(SymptomDiseaseLinkBase):
    class Config:
        orm_mode = True


class SymptomDiseaseLink(SymptomDiseaseLinkBase):
    class Config:
        orm_mode = True


# ===================================
# Custom Input Models start here
# ===================================
class ImageInput(BaseModel):
    b64_img: str
