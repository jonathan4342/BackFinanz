-- =====================================================================
-- Datos de ejemplo (opcional) - PostgreSQL
-- Ejecutar DESPUÉS de postgres_schema.sql.
-- =====================================================================

INSERT INTO clients (name, email, company) VALUES
    ('Ana Torres',   'ana@acme.com',    'Acme'),
    ('Luis Gómez',   'luis@globex.com', 'Globex'),
    ('María Ruiz',   'maria@initech.com', 'Initech')
ON CONFLICT (email) DO NOTHING;

INSERT INTO tickets (client_id, title, description, status) VALUES
    (1, 'Error al iniciar sesión', 'El usuario no puede autenticarse', 'PENDIENTE'),
    (1, 'Factura incorrecta',      'El total no coincide',            'EN_PROGRESO'),
    (2, 'Solicitud de acceso',     'Requiere permisos de admin',      'FINALIZADO');
