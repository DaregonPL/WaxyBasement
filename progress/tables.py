from sqlalchemy import Column, Integer, String
from progress.core import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(
        Integer,
        primary_key=True,
        unique=True,
    )
    name = Column(
        String(length=64),
        nullable=False
    )
    scene = Column(
        String(length=64),
        nullable=False
    )
    page = Column(
        Integer,
        nullable=False
    )
    inventory = Column(
        String(length=4096)
    )