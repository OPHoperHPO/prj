from pydantic import BaseModel, Field, validator
from typing import Optional, List


class User(BaseModel):
    login: str
    password: str
    passphrase: str

    class Config:
        orm_mode = True


class BankUser(User):
    bank: str


class InsurerUser(User):
    insurer: str


class Contract(BaseModel):
    address: str
    contract_number: str

    class Config:
        orm_mode = True


class CreateContract(BaseModel):
    FIO: str
    insurer_date: int
    bank_date: int
    insurer_number: int
    bank_number: int
    bank_name: str
    insurer_name: str
    email: str
    amount: int
    type: str
    client_password: str
    client_passphrase: str
