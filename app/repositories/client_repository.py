"""Implementación SQLAlchemy del repositorio de clientes."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.client import Client
from app.repositories.interfaces import ClientRepository


class SqlAlchemyClientRepository(ClientRepository):
    def __init__(self, db: Session):
        self._db = db

    def create(self, name: str, email: str, company: str) -> Client:
        client = Client(name=name, email=email, company=company)
        self._db.add(client)
        self._db.commit()
        self._db.refresh(client)
        return client

    def list(self) -> list[Client]:
        return list(self._db.scalars(select(Client)).all())

    def get(self, client_id: int) -> Client | None:
        return self._db.get(Client, client_id)

    def get_by_email(self, email: str) -> Client | None:
        return self._db.scalar(select(Client).where(Client.email == email))
