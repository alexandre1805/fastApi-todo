from fastapi import APIRouter

from .health import router as health_router
from .item import router as items_router

router = APIRouter()
router.include_router(health_router)
router.include_router(items_router)