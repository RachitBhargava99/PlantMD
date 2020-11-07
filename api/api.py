from fastapi import APIRouter

from api.diseases.routes import router as disease_router
from api.symptoms.routes import router as symptom_router

api_router = APIRouter()

api_router.include_router(router=disease_router, prefix='/disease')
api_router.include_router(router=symptom_router, prefix='/symptom')
