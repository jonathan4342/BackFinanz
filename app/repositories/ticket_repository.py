"""Implementación SQLAlchemy del repositorio de tickets."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ticket import Ticket, TicketStatus
from app.repositories.interfaces import TicketRepository


class SqlAlchemyTicketRepository(TicketRepository):
    def __init__(self, db: Session):
        self._db = db

    def create(self, client_id: int, title: str, description: str) -> Ticket:
        ticket = Ticket(client_id=client_id, title=title, description=description)
        self._db.add(ticket)
        self._db.commit()
        self._db.refresh(ticket)
        return ticket

    def list(self) -> list[Ticket]:
        return list(self._db.scalars(select(Ticket)).all())

    def get(self, ticket_id: int) -> Ticket | None:
        return self._db.get(Ticket, ticket_id)

    def update_status(self, ticket: Ticket, status: TicketStatus) -> Ticket:
        ticket.status = status
        self._db.commit()
        self._db.refresh(ticket)
        return ticket
