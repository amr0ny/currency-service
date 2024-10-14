from fastapi import FastAPI

from containers import Services, Adapters
from routes import router

def app_factory():
    app = FastAPI()
    app.services = Services()
    app.services.wire(modules=["routes.exchange_routes", "services"])

    app.include_router(router)

    return app


app = app_factory()