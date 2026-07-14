"""Lógica de negocio de tickets.

Depende de las abstracciones de repositorio (DIP). Valida que el cliente
asociado exista antes de crear un ticket.
"""
from app.models.ticket import Ticket, TicketStatus
from app.repositories.interfaces import ClientRepository, TicketRepository
from app.schemas.ticket import TicketCreate
from app.services.exceptions import NotFoundError


class TicketService:
    def __init__(
        self,
        ticket_repository: TicketRepository,
        client_repository: ClientRepository,
    ):
        self._tickets = ticket_repository
        self._clients = client_repository

    def create_ticket(self, data: TicketCreate) -> Ticket:
        if self._clients.get(data.client_id) is None:
            raise NotFoundError(f"Cliente {data.client_id} no encontrado")
        return self._tickets.create(
            client_id=data.client_id,
            title=data.title,
            description=data.description,
        )

    def list_tickets(self) -> list[Ticket]:
        return self._tickets.list()

    def update_status(self, ticket_id: int, status: TicketStatus) -> Ticket:
        ticket = self._tickets.get(ticket_id)
        if ticket is None:
            raise NotFoundError(f"Ticket {ticket_id} no encontrado")
        return self._tickets.update_status(ticket, status)
