"""Pruebas unitarias del servicio de clientes (sin base de datos)."""
import pytest

from app.schemas.client import ClientCreate
from app.services.client_service import ClientService
from app.services.exceptions import ConflictError, NotFoundError
from tests.fakes import FakeClientRepository


def test_create_client_persists_and_returns_it():
    service = ClientService(FakeClientRepository())

    created = service.create_client(
        ClientCreate(name="Ana", email="ana@x.com", company="Finanz")
    )

    assert created.id is not None
    assert created.name == "Ana"
    assert len(service.list_clients()) == 1


def test_create_client_with_duplicate_email_raises_conflict():
    service = ClientService(FakeClientRepository())
    service.create_client(
        ClientCreate(name="Ana", email="ana@x.com", company="Finanz")
    )

    with pytest.raises(ConflictError):
        service.create_client(
            ClientCreate(name="Otra", email="ana@x.com", company="Finanz")
        )


def test_get_missing_client_raises_not_found():
    service = ClientService(FakeClientRepository())

    with pytest.raises(NotFoundError):
        service.get_client(999)
