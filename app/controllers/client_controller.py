"""Endpoints HTTP de clientes.

Capa delgada: valida entrada/salida con schemas, delega en el servicio y
traduce las excepciones de dominio a códigos HTTP.
"""
from fastapi import APIRouter, HTTPException, status

from app.controllers.deps import ClientServiceDep
from app.schemas.client import ClientCreate, ClientRead
from app.services.exceptions import ConflictError, NotFoundError

router = APIRouter(prefix="/clients", tags=["clients"])


@router.post("", response_model=ClientRead, status_code=status.HTTP_201_CREATED)
def create_client(data: ClientCreate, service: ClientServiceDep):
    try:
        return service.create_client(data)
    except ConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.get("", response_model=list[ClientRead])
def list_clients(service: ClientServiceDep):
    return service.list_clients()


@router.get("/{client_id}", response_model=ClientRead)
def get_client(client_id: int, service: ClientServiceDep):
    try:
        return service.get_client(client_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
