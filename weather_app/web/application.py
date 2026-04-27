"""FastAPI application factory."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from weather_app.web.api.router import api_router
from weather_app.web.lifespan import lifespan_setup

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"


def get_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="weather_app",
        lifespan=lifespan_setup,
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
    )

    app.include_router(router=api_router, prefix="/api")
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

    @app.get("/", include_in_schema=False)
    async def root() -> RedirectResponse:
        """Redirect root to login page."""
        return RedirectResponse(url="/login")

    @app.get("/login", include_in_schema=False)
    async def login_page() -> FileResponse:
        """Serve the login page."""
        return FileResponse(STATIC_DIR / "login.html")

    @app.get("/signup", include_in_schema=False)
    async def signup_page() -> FileResponse:
        """Serve the signup page."""
        return FileResponse(STATIC_DIR / "signup.html")

    @app.get("/dashboard", include_in_schema=False)
    async def dashboard_page() -> FileResponse:
        """Serve the dashboard page."""
        return FileResponse(STATIC_DIR / "dashboard.html")

    return app
