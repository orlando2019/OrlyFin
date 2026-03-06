from fastapi import APIRouter

from app.domains.auth_users.interfaces.api import router as auth_router
from app.domains.auth_users.interfaces.api import users_router
from app.domains.rbac.interfaces.api import router as rbac_router
from app.interfaces.api.v1.health import router as health_router

router = APIRouter()
router.include_router(health_router, tags=["system"])
router.include_router(auth_router)
router.include_router(users_router)
router.include_router(rbac_router)
