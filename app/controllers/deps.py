"""Cableado de dependencias (Composition Root).

Aquí se construyen repositorios y servicios y se exponen como
dependencias de FastAPI. Es el único lugar que conoce las
implementaciones concretas; el resto del código trabaja con abstracciones.
"""
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.client_repository import SqlAlchemyClientRepository
from app.repositories.interfaces import ClientRepository, TicketRepository
from app.repositories.ticket_repository import SqlAlchemyTicketRepository
from app.services.client_service import ClientService
from app.services.ticket_service import TicketService

DbSession = Annotated[Session, Depends(get_db)]


def get_client_repository(db: DbSession) -> ClientRepository:
    return SqlAlchemyClientRepository(db)


def get_ticket_repository(db: DbSession) -> TicketRepository:
    return SqlAlchemyTicketRepository(db)


def get_client_service(
    repo: Annotated[ClientRepository, Depends(get_client_repository)],
) -> ClientService:
    return ClientService(repo)


def get_ticket_service(
    ticket_repo: Annotated[TicketRepository, Depends(get_ticket_repository)],
    client_repo: Annotated[ClientRepository, Depends(get_client_repository)],
) -> TicketService:
    return TicketService(ticket_repo, client_repo)


ClientServiceDep = Annotated[ClientService, Depends(get_client_service)]
TicketServiceDep = Annotated[TicketService, Depends(get_ticket_service)]
