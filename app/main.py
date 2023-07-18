from fastapi import FastAPI
from . import models
from .database import engine
from .routers import api
from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api.router)
