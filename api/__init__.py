import api.routers as api_routers
from fastapi import FastAPI
from common import add_custom_errors, handle_cors


def create_app():
    app = FastAPI()
    handle_cors(app)
    app.include_router(api_routers.health_router)
    @app.get("/{path:path}")
    def any_get():
        return "hola"
    add_custom_errors(app)
    return app
