from fastapi import APIRouter
from fastapi_pagination import add_pagination

from .review import router as review_router

router_v1 = APIRouter()
router_v1.include_router(review_router, tags=["Review"], prefix="/review")
add_pagination(router_v1)
