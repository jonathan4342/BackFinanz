-- =====================================================================
-- Esquema PostgreSQL - Gestión de Clientes y Tickets
-- ---------------------------------------------------------------------
-- La aplicación crea estas tablas automáticamente al arrancar
-- (SQLAlchemy Base.metadata.create_all). Este script se proporciona para
-- crear el esquema de forma manual o como documentación de referencia.
-- Refleja exactamente el modelo ORM.
-- =====================================================================

-- Tipo enumerado para el estado del ticket.
-- Los valores son los NOMBRES del enum de Python (la API los muestra como
-- "Pendiente", "En progreso", "Finalizado").
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'ticketstatus') THEN
        CREATE TYPE ticketstatus AS ENUM ('PENDIENTE', 'EN_PROGRESO', 'FINALIZADO');
    END IF;
END$$;

-- ---------------------------------------------------------------------
-- Tabla: clients
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS clients (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(120) NOT NULL,
    email       VARCHAR(255) NOT NULL UNIQUE,
    company     VARCHAR(120) NOT NULL,
    created_at  TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_clients_id ON clients (id);

-- ---------------------------------------------------------------------
-- Tabla: tickets
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS tickets (
    id          SERIAL PRIMARY KEY,
    client_id   INTEGER NOT NULL REFERENCES clients (id) ON DELETE CASCADE,
    title       VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    status      ticketstatus NOT NULL DEFAULT 'PENDIENTE',
    created_at  TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS ix_tickets_id ON tickets (id);
CREATE INDEX IF NOT EXISTS ix_tickets_client_id ON tickets (client_id);
