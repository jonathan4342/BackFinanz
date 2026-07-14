# Backend — Gestión de Clientes y Tickets

API REST en **Python + FastAPI** para la gestión de clientes y tickets de soporte. Aplica arquitectura por capas y principios SOLID.

## Stack

- FastAPI + Uvicorn
- SQLAlchemy 2.0 + PostgreSQL
- Pydantic v2
- MongoDB para eventos de auditoría (opcional)
- Pytest (pruebas) · Ruff (linter)

## Requisitos

- Python 3.11
- PostgreSQL (o una URL de conexión, p. ej. Neon)

## Instalación y ejecución

```bash
python -m venv .venv
# Windows: .\.venv\Scripts\Activate.ps1
# Linux/Mac: source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

La API queda en `http://localhost:8000` y la documentación interactiva (Swagger) en `http://localhost:8000/docs`.

## Configuración

La conexión a la base de datos se define por variables de entorno (hay un `.env.example` de referencia). La forma más simple es una URL completa:

```
DATABASE_URL=postgresql://usuario:password@host:5432/basededatos
```

Variables disponibles:

- `DATABASE_URL` — URL completa de PostgreSQL (tiene prioridad si se define).
- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `POSTGRES_HOST`, `POSTGRES_PORT` — alternativa por partes.
- `MONGO_URL`, `MONGO_DB` — conexión a MongoDB para la auditoría (opcional).

Las tablas se crean automáticamente al arrancar la aplicación.

## Endpoints

Clientes:

- `POST /clients` — crear un cliente
- `GET /clients` — listar clientes
- `GET /clients/{id}` — consultar un cliente por id

Tickets:

- `POST /tickets` — crear un ticket asociado a un cliente
- `GET /tickets` — listar tickets
- `PATCH /tickets/{id}/status` — actualizar el estado (Pendiente, En progreso, Finalizado)

Estado del servicio: `GET /health`

## Pruebas

Las pruebas usan SQLite en memoria, por lo que no requieren una base de datos real:

```bash
pytest
```

Linter:

```bash
ruff check .
```

## Estructura del proyecto

```
app/
├── controllers/   # Routers / endpoints (capa HTTP) + inyección de dependencias
├── services/      # Lógica de negocio
├── repositories/  # Acceso a datos (interfaces + implementaciones)
├── models/        # Modelos ORM (SQLAlchemy)
├── schemas/       # Esquemas Pydantic (validación / DTO)
├── core/          # Configuración
├── db/            # Sesión de BD y conexión a MongoDB
└── main.py        # Punto de entrada de la aplicación
tests/             # Pruebas unitarias e integración (Pytest)
database/          # Scripts SQL (PostgreSQL) y de MongoDB
```

## Auditoría (MongoDB)

Cada creación o cambio de estado de un ticket registra un evento de auditoría (usuario, acción, ticket_id, fecha/hora) en MongoDB. Es un valor agregado y no bloquea la operación si Mongo no está disponible. El usuario se toma de la cabecera opcional `X-User` (por defecto `system`).

## Docker

Para levantar toda la solución (backend, frontend, PostgreSQL y MongoDB) se usa el `docker-compose.yml` de la raíz del proyecto:

```bash
docker compose up --build
```

## Documentación adicional

- `salesforce.md` — propuesta de integración con Salesforce.
- `Finanz.postman_collection.json` — colección de Postman para probar la API.
