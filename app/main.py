"""Punto de entrada de la aplicación FastAPI."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import client_controller, ticket_controller
from app.db.base import Base
from app.db.session import engine

# Importa los modelos para que queden registrados en la metadata antes de
# crear las tablas.
from app.models import client, ticket  # noqa: F401


def create_app() -> FastAPI:
    app = FastAPI(title="Gestión de Clientes y Tickets", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Crea las tablas al arrancar (suficiente para el alcance de la prueba;
    # en producción se usarían migraciones con Alembic).
    Base.metadata.create_all(bind=engine)

    app.include_router(client_controller.router)
    app.include_router(ticket_controller.router)

    @app.get("/health", tags=["health"])
    def health():
        return {"status": "ok"}

    return app


app = create_app()
