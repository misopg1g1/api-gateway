import publishers

from fastapi import APIRouter, Body

health_router = APIRouter(prefix="/health", tags=["Health Check"])


@health_router.get("/")
def health():
    '''retorna 200 si el microservicio esta activo.'''
    return {"msg": "healthy!!!!!"}


@health_router.post("/kombu")
def health(data=Body()):
    publisher = publishers.new_order_email_publisher()
    publisher.publish_user_to_verify(data)
    publisher.connection.close()
    return {"msg": "mensaje enviado a la cola!!"}
