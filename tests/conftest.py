"""Fixtures compartidas de las pruebas.

Para la prueba de integración se levanta la app real pero apuntando a una
base de datos SQLite en memoria, sobreescribiendo la dependencia `get_db`.
Así no se necesita PostgreSQL para correr los tests (útil también en CI).
"""
import os

# Fuerza SQLite antes de importar la app, para que las pruebas no dependan
# del driver de PostgreSQL ni de una base de datos real.
os.environ["DATABASE_URL"] = "sqlite://"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_db
from app.main import app

# Importa los modelos para registrarlos en la metadata.
from app.models import client, ticket  # noqa: F401


@pytest.fixture
def client_app():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
