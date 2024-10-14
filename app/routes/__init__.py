from fastapi import APIRouter

from routes.exchange_routes import exchange_router
router = APIRouter()
router.include_router(exchange_router, prefix="/api", tags=["exchange"])