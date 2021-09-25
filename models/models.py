from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    BINARY,
    Boolean,
    DateTime,
    ForeignKey,
    Float,
    Table
)

from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship
from sqlalchemy.types import UserDefinedType
from sqlalchemy import func

from db import Base

class Bank(Base):
    __tablename__ = "banks"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    blockchain_wallet = Column(String, nullable=False)

class Insurer(Base):
    __tablename__ = "insurers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    blockchain_wallet = Column(String, nullable=False)

class InsurerUser(Base):
    __tablename__ = "insurers_users"

    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False)
    password = Column(BINARY, nullable=False)
    insurerID = Column(Integer, ForeignKey('insurers.id'), nullable=False)


class BankUser(Base):
    __tablename__ = "banks_users"

    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False)
    password = Column(BINARY, nullable=False)
    insurerID = Column(Integer, ForeignKey('banks.id'), nullable=False)


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False)
    password = Column(BINARY, nullable=False)
    blockchain_wallet = Column(String, nullable=False)

