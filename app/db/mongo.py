"""Conexión a MongoDB para los eventos de auditoría.

La auditoría es un valor agregado y no debe acoplar la aplicación a pymongo
al arrancar: el import y la conexión son perezosos, y los errores se manejan
en la capa de dependencias / repositorio.
"""
from functools import lru_cache

from app.core.config import settings


@lru_cache
def get_mongo_client():
    # Import perezoso: solo se carga pymongo cuando realmente se usa Mongo.
    from pymongo import MongoClient

    # serverSelectionTimeoutMS bajo para no bloquear si Mongo no responde.
    return MongoClient(settings.MONGO_URL, serverSelectionTimeoutMS=2000)


def get_audit_collection():
    return get_mongo_client()[settings.MONGO_DB]["audit_events"]
