from fastapi import APIRouter

from .health import router as health_router
from .item import router as items_router
from .list import router as list_router

router = APIRouter()
router.include_router(health_router)
router.include_router(items_router)
router.include_router(list_router)
