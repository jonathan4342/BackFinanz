"""Lógica de negocio de clientes.

Depende de la abstracción `ClientRepository` (DIP), no de su
implementación concreta. La instancia se inyecta por el constructor.
"""
from app.models.client import Client
from app.repositories.interfaces import ClientRepository
from app.schemas.client import ClientCreate
from app.services.exceptions import ConflictError, NotFoundError


class ClientService:
    def __init__(self, repository: ClientRepository):
        self._repository = repository

    def create_client(self, data: ClientCreate) -> Client:
        if self._repository.get_by_email(data.email):
            raise ConflictError(f"Ya existe un cliente con el correo {data.email}")
        return self._repository.create(
            name=data.name, email=data.email, company=data.company
        )

    def list_clients(self) -> list[Client]:
        return self._repository.list()

    def get_client(self, client_id: int) -> Client:
        client = self._repository.get(client_id)
        if client is None:
            raise NotFoundError(f"Cliente {client_id} no encontrado")
        return client
