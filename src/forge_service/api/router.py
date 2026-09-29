from fastapi import APIRouter

from forge_service.api.routes.health import router as health_router
from forge_service.api.routes.metrics import router as metrics_router
from forge_service.api.routes.simulation import router as simulation_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(metrics_router)
api_router.include_router(simulation_router)
