from fastapi import FastAPI, HTTPException, status, Depends
from typing import List
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db
from .routers import api

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(api.router)
