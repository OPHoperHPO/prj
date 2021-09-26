from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    LargeBinary,
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
    cipher_initialization_vector = Column(LargeBinary, nullable=False)
    blockchain_wallet = Column(LargeBinary, nullable=False)
    wallet_hash = Column(LargeBinary, nullable=False)


class BankWithUsers(Bank):
    users = relationship('BankUserWithBank', back_populates='bank')


class Insurer(Base):
    __tablename__ = "insurers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cipher_initialization_vector = Column(LargeBinary, nullable=False)
    blockchain_wallet = Column(LargeBinary, nullable=False)
    wallet_hash = Column(LargeBinary, nullable=False)


class InsurerWithUsers(Insurer):
    users = relationship('InsurerUserWithInsurer', back_populates='insurer')


class InsurerUser(Base):
    __tablename__ = "insurers_users"

    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False)
    password = Column(LargeBinary, nullable=False)
    salt = Column(LargeBinary, nullable=False)
    insurer_id = Column(Integer, ForeignKey('insurers.id'), nullable=False)


class InsurerUserWithInsurer(InsurerUser):
    insurer = relationship('InsurerWithUsers', back_populates='users')


class BankUser(Base):
    __tablename__ = "banks_users"

    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False)
    password = Column(LargeBinary, nullable=False)
    salt = Column(LargeBinary, nullable=False)
    bank_id = Column(Integer, ForeignKey('banks.id'), nullable=False)


class BankUserWithBank(BankUser):
    bank = relationship('BankWithUsers', back_populates='users')


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    login = Column(String, nullable=False)
    password = Column(LargeBinary, nullable=False)
    salt = Column(LargeBinary, nullable=False)
    cipher_initialization_vector = Column(LargeBinary, nullable=False)
    blockchain_wallet = Column(LargeBinary, nullable=False)
    wallet_hash = Column(LargeBinary, nullable=False)


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False)
    contract_number = Column(String, nullable=False)
    bank_id = Column(Integer, ForeignKey("banks.id"))
    insurer_id = Column(Integer, ForeignKey("insurers.id"))
    client_id = Column(Integer, ForeignKey("clients.id"))
