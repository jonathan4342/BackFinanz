"""Endpoints HTTP de tickets."""
from fastapi import APIRouter, HTTPException, status

from app.controllers.deps import TicketServiceDep
from app.schemas.ticket import TicketCreate, TicketRead, TicketStatusUpdate
from app.services.exceptions import NotFoundError

router = APIRouter(prefix="/tickets", tags=["tickets"])


@router.post("", response_model=TicketRead, status_code=status.HTTP_201_CREATED)
def create_ticket(data: TicketCreate, service: TicketServiceDep):
    try:
        return service.create_ticket(data)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.get("", response_model=list[TicketRead])
def list_tickets(service: TicketServiceDep):
    return service.list_tickets()


@router.patch("/{ticket_id}/status", response_model=TicketRead)
def update_ticket_status(
    ticket_id: int, data: TicketStatusUpdate, service: TicketServiceDep
):
    try:
        return service.update_status(ticket_id, data.status)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
