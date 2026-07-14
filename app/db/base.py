"""Base declarativa de SQLAlchemy.

Todos los modelos ORM heredan de `Base` para compartir metadata.
"""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
