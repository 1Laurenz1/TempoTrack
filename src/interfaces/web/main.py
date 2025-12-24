from fastapi import FastAPI

from .routes import api_router


def create_app():
    app = FastAPI(
        title="TempoTrack",
        debug=True,
        swagger_ui_parameters={"persistAuthorization": True},
    )

    
    app.include_router(api_router.router)
    
    return app
