"""Lógica de negocio de tickets.

Depende de las abstracciones de repositorio (DIP). Valida que el cliente
asociado exista antes de crear un ticket y registra eventos de auditoría.
"""
from app.models.ticket import Ticket, TicketStatus
from app.repositories.audit_repository import NullAuditRepository
from app.repositories.interfaces import (
    AuditRepository,
    ClientRepository,
    TicketRepository,
)
from app.schemas.ticket import TicketCreate
from app.services.exceptions import NotFoundError


class TicketService:
    def __init__(
        self,
        ticket_repository: TicketRepository,
        client_repository: ClientRepository,
        audit: AuditRepository | None = None,
    ):
        self._tickets = ticket_repository
        self._clients = client_repository
        # Si no se inyecta auditoría, se usa una implementación no-op.
        self._audit = audit or NullAuditRepository()

    def create_ticket(self, data: TicketCreate, user: str = "system") -> Ticket:
        if self._clients.get(data.client_id) is None:
            raise NotFoundError(f"Cliente {data.client_id} no encontrado")
        ticket = self._tickets.create(
            client_id=data.client_id,
            title=data.title,
            description=data.description,
        )
        self._audit.log(user, "CREATE_TICKET", ticket.id)
        return ticket

    def list_tickets(self) -> list[Ticket]:
        return self._tickets.list()

    def update_status(
        self, ticket_id: int, status: TicketStatus, user: str = "system"
    ) -> Ticket:
        ticket = self._tickets.get(ticket_id)
        if ticket is None:
            raise NotFoundError(f"Ticket {ticket_id} no encontrado")
        updated = self._tickets.update_status(ticket, status)
        self._audit.log(user, f"UPDATE_STATUS:{status.value}", ticket_id)
        return updated
