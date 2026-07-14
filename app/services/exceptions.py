"""Excepciones de dominio.

Independientes del framework: los servicios las lanzan y la capa de
controllers las traduce a respuestas HTTP.
"""


class DomainError(Exception):
    """Error base de la capa de negocio."""


class NotFoundError(DomainError):
    """Un recurso solicitado no existe."""


class ConflictError(DomainError):
    """Violación de una regla de unicidad/estado."""
