from fastapi import FastAPI, APIRouter
from . import posts

router = APIRouter(
    prefix="/api/v1"
)

router.include_router(posts.router)
