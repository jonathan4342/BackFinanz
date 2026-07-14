"""Implementaciones del repositorio de auditoría."""
import logging
from datetime import datetime, timezone

from app.repositories.interfaces import AuditRepository

logger = logging.getLogger(__name__)


class MongoAuditRepository(AuditRepository):
    """Guarda los eventos de auditoría en MongoDB.

    Los fallos de Mongo se registran pero no se propagan: la auditoría no
    debe impedir la operación principal (crear/actualizar un ticket).
    """

    def __init__(self, collection):
        self._collection = collection

    def log(self, user: str, action: str, ticket_id: int) -> None:
        event = {
            "user": user,
            "action": action,
            "ticket_id": ticket_id,
            "timestamp": datetime.now(timezone.utc),
        }
        try:
            self._collection.insert_one(event)
        except Exception as exc:  # pragma: no cover - Mongo opcional
            logger.warning("No se pudo registrar el evento de auditoría: %s", exc)


class NullAuditRepository(AuditRepository):
    """Implementación no-op (usada cuando la auditoría está deshabilitada)."""

    def log(self, user: str, action: str, ticket_id: int) -> None:
        return None
