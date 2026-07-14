"""Interfaces (abstracciones) de los repositorios.

Definir estas ABC permite aplicar el Principio de Inversión de Dependencias
(DIP): los servicios dependen de estas abstracciones, no de la
implementación concreta de SQLAlchemy. Esto facilita sustituir el
almacenamiento o inyectar mocks en las pruebas.
"""
from abc import ABC, abstractmethod

from app.models.client import Client
from app.models.ticket import Ticket, TicketStatus


class ClientRepository(ABC):
    @abstractmethod
    def create(self, name: str, email: str, company: str) -> Client: ...

    @abstractmethod
    def list(self) -> list[Client]: ...

    @abstractmethod
    def get(self, client_id: int) -> Client | None: ...

    @abstractmethod
    def get_by_email(self, email: str) -> Client | None: ...


class TicketRepository(ABC):
    @abstractmethod
    def create(self, client_id: int, title: str, description: str) -> Ticket: ...

    @abstractmethod
    def list(self) -> list[Ticket]: ...

    @abstractmethod
    def get(self, ticket_id: int) -> Ticket | None: ...

    @abstractmethod
    def update_status(self, ticket: Ticket, status: TicketStatus) -> Ticket: ...


class AuditRepository(ABC):
    """Registro de eventos de auditoría (base no relacional, ej. MongoDB)."""

    @abstractmethod
    def log(self, user: str, action: str, ticket_id: int) -> None: ...
