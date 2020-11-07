from fastapi import FastAPI

import yaml

from db import models
from db.db import engine
from api.api import api_router

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="FastMD", docs_url='/')
app.openapi_schema = yaml.load(open('swagger.yaml').read())
app.include_router(api_router)
