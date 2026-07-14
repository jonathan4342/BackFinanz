"""Repositorios falsos en memoria para las pruebas unitarias.

Implementan las mismas interfaces (ABC) que los repositorios reales, lo que
permite probar los servicios de forma aislada, sin base de datos. Es la
ventaja práctica de aplicar el Principio de Inversión de Dependencias.
"""
from datetime import datetime

from app.models.client import Client
from app.models.ticket import Ticket, TicketStatus
from app.repositories.interfaces import (
    AuditRepository,
    ClientRepository,
    TicketRepository,
)


class FakeAuditRepository(AuditRepository):
    def __init__(self):
        self.events: list[dict] = []

    def log(self, user: str, action: str, ticket_id: int) -> None:
        self.events.append(
            {"user": user, "action": action, "ticket_id": ticket_id}
        )


class FakeClientRepository(ClientRepository):
    def __init__(self):
        self._items: dict[int, Client] = {}
        self._seq = 0

    def create(self, name: str, email: str, company: str) -> Client:
        self._seq += 1
        client = Client(
            id=self._seq,
            name=name,
            email=email,
            company=company,
            created_at=datetime.utcnow(),
        )
        self._items[client.id] = client
        return client

    def list(self) -> list[Client]:
        return list(self._items.values())

    def get(self, client_id: int) -> Client | None:
        return self._items.get(client_id)

    def get_by_email(self, email: str) -> Client | None:
        return next((c for c in self._items.values() if c.email == email), None)


class FakeTicketRepository(TicketRepository):
    def __init__(self):
        self._items: dict[int, Ticket] = {}
        self._seq = 0

    def create(self, client_id: int, title: str, description: str) -> Ticket:
        self._seq += 1
        ticket = Ticket(
            id=self._seq,
            client_id=client_id,
            title=title,
            description=description,
            status=TicketStatus.PENDIENTE,
            created_at=datetime.utcnow(),
        )
        self._items[ticket.id] = ticket
        return ticket

    def list(self) -> list[Ticket]:
        return list(self._items.values())

    def get(self, ticket_id: int) -> Ticket | None:
        return self._items.get(ticket_id)

    def update_status(self, ticket: Ticket, status: TicketStatus) -> Ticket:
        ticket.status = status
        return ticket
