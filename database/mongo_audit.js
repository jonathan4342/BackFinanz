// =====================================================================
// MongoDB - Colección de auditoría
// ---------------------------------------------------------------------
// La colección "audit_events" se crea sola al insertar el primer evento
// (Mongo es schemaless). Este script crea índices útiles y deja un
// documento de ejemplo. Ejecutar con:  mongosh finanz_audit database/mongo_audit.js
// =====================================================================

const db = db.getSiblingDB('finanz_audit');

// Índices para consultar la auditoría por ticket y por fecha.
db.audit_events.createIndex({ ticket_id: 1 });
db.audit_events.createIndex({ timestamp: -1 });
db.audit_events.createIndex({ user: 1 });

// Estructura de un evento de auditoría (ejemplo):
db.audit_events.insertOne({
    user: 'system',
    action: 'CREATE_TICKET',
    ticket_id: 1,
    timestamp: new Date()
});

print('Colección audit_events lista con índices.');
