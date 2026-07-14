"""Pruebas unitarias del servicio de tickets (sin base de datos)."""
import pytest

from app.models.ticket import TicketStatus
from app.schemas.ticket import TicketCreate
from app.services.exceptions import NotFoundError
from app.services.ticket_service import TicketService
from tests.fakes import (
    FakeAuditRepository,
    FakeClientRepository,
    FakeTicketRepository,
)


def _service_with_client(audit=None):
    clients = FakeClientRepository()
    client = clients.create(name="Ana", email="ana@x.com", company="Finanz")
    service = TicketService(FakeTicketRepository(), clients, audit)
    return service, client


def test_create_ticket_starts_as_pending():
    service, client = _service_with_client()

    ticket = service.create_ticket(
        TicketCreate(client_id=client.id, title="Error", description="No entra")
    )

    assert ticket.id is not None
    assert ticket.status == TicketStatus.PENDIENTE


def test_create_ticket_for_missing_client_raises_not_found():
    service = TicketService(FakeTicketRepository(), FakeClientRepository())

    with pytest.raises(NotFoundError):
        service.create_ticket(
            TicketCreate(client_id=999, title="X", description="Y")
        )


def test_update_status_changes_ticket_status():
    service, client = _service_with_client()
    ticket = service.create_ticket(
        TicketCreate(client_id=client.id, title="Error", description="No entra")
    )

    updated = service.update_status(ticket.id, TicketStatus.FINALIZADO)

    assert updated.status == TicketStatus.FINALIZADO


def test_create_ticket_records_audit_event():
    audit = FakeAuditRepository()
    service, client = _service_with_client(audit)

    ticket = service.create_ticket(
        TicketCreate(client_id=client.id, title="Error", description="No entra"),
        user="ana",
    )

    assert len(audit.events) == 1
    assert audit.events[0] == {
        "user": "ana",
        "action": "CREATE_TICKET",
        "ticket_id": ticket.id,
    }
