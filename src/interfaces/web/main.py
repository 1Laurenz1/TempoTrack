from fastapi import FastAPI

from .routes import api_router


def create_app():
    app = FastAPI(
        title="TempoTrack",
        debug=True,
    )

    
    app.include_router(api_router.router)
    
    return app
