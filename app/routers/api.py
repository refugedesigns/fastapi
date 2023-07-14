from fastapi import APIRouter
from . import posts, users, auth

router = APIRouter(
    prefix="/api/v1"
)

router.include_router(posts.router)
router.include_router(users.router)
router.include_router(auth.router)
