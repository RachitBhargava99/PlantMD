from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import yaml

from db import models
from db.db import engine
from api.api import api_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="PlantMD", docs_url='/')
# app.openapi_schema = yaml.load(open('swagger.yaml').read())
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
