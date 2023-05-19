import publishers

from fastapi import APIRouter, Body

health_router = APIRouter(prefix="/health", tags=["Health Check"])


@health_router.get("/")
def health():
    '''retorna 200 si el microservicio esta activo.'''
    return {"msg": "healthy!!!!!"}
