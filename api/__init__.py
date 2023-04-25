import api.routers as api_routers
from fastapi import FastAPI
from common import add_custom_errors, handle_cors, encrypter_middleware


def create_app():
    app = FastAPI()
    add_custom_errors(app)
    app.include_router(api_routers.health_router)
    app.include_router(api_routers.session_router)
    app.include_router(api_routers.product_router)
    app.include_router(api_routers.inventory_router)
    handle_cors(app)
    encrypter_middleware(app)
    return app
