"""Esquemas Pydantic para Ticket (validación y serialización)."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.ticket import TicketStatus


class TicketBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)


class TicketCreate(TicketBase):
    client_id: int


class TicketStatusUpdate(BaseModel):
    status: TicketStatus


class TicketRead(TicketBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    client_id: int
    status: TicketStatus
    created_at: datetime
