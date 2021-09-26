import schemas
from models import models
from main import app, get_db

from fastapi_login import LoginManager
from sqlalchemy.orm.session import Session
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from fastapi_login.exceptions import InvalidCredentialsException
import hashlib, os
from blockchain_wrapper import BlockchainWrapper
from Crypto.Cipher import AES
from sqlalchemy import or_

secret = "27416c619e2583dd7023ff9590b2d931458a11d58595971c96f566d1d5fa533c46413dca20bf7c99e12776a9da8bb3bdd2fa2cd65fb6a4\
8ac7a6bc3517b8d95229666d88887c1d8170907cce7ddb1d3b0e4dc6cc1a5f373d5293c77d0b042b8a5d965baeb28bf6006a732d3242e77c4f2b8e75\
e6a92055d442361c1a949a564c03f1862352508c4062562ff697320608af17a99050f493c4cb468419bfbd967cbfdadf70d01c2128c9ffccf143ad82\
4d5adb1d2a6715805dc99691e5158e4a8b34e44f0f91d3e44a89967f0ae46472082b8c14c97bf072095d0fce0a31c4e8883bd7025be7e005e1273b77\
07adc8da5ba42c01bb5cf837f2ff1b71c82caf5eb6"

manager = LoginManager(secret, token_url="/api/v1/login", use_cookie=True)


@manager.user_loader()
def user_loader(email: str):
    db: Session = next(get_db())
    as_client = (
        db.query(models.Client).filter(models.Client.login == email).one_or_none()
    )
    as_bank = (
        db.query(models.BankUserWithBank)
        .filter(models.BankUserWithBank.login == email)
        .one_or_none()
    )
    as_insurer = (
        db.query(models.InsurerUserWithInsurer)
        .filter(models.InsurerUserWithInsurer.login == email)
        .one_or_none()
    )
    if as_client:
        return as_client
    if as_bank:
        return as_bank
    if as_insurer:
        return as_insurer
    return None


def hash_password(password: str, salt: bytes = os.urandom(32)) -> (bytes, bytes):
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 10000)
    return key, salt


def verify_password(plain_password: str, password_salt: bytes, password_hash: bytes):
    return password_hash == hash_password(plain_password, password_salt)[0]


@app.post("/api/v1/login")
async def login(response: JSONResponse, data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    user = user_loader(email)

    if not user:
        raise InvalidCredentialsException
    elif not verify_password(password, user.salt, user.password):
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data={
            "sub": user.login,
            "rol": 0
            if isinstance(user, models.BankUserWithBank)
            else 1
            if isinstance(user, models.InsurerUserWithInsurer)
            else 2,
        }
    )

    response = JSONResponse(
        status_code=200,
        content={
            "result": "success",
            "user_role": 0
            if isinstance(user, models.BankUserWithBank)
            else 1
            if isinstance(user, models.InsurerUserWithInsurer)
            else 2,
            "wallet_address": user.wallet_address
            if isinstance(user, models.Client)
            else user.bank.wallet_address
            if isinstance(user, models.BankUser)
            else user.insurer.wallet_address,
        },
    )

    # response.set_cookie("access-token", value=access_token, httponly=True, samesite="none", secure=True) // kinda template for future bugfixes????

    manager.set_cookie(response, access_token)
    return response


@app.post("/api/v1/register")
async def register_new_user(user: schemas.User, db: Session = Depends(get_db)):
    user_model: models.Client = models.Client(login=user.login)
    user_by_login = user_loader(user.login)
    if user_by_login:
        return JSONResponse(
            status_code=400,
            content={
                "result": "error",
                "result_description": "User with this email already exists",
            },
        )
    password, salt = hash_password(user.password)
    user_model.password = password
    user_model.salt = salt
    (
        user_model.cipher_initialization_vector,
        user_model.blockchain_wallet,
        user_model.wallet_hash,
        user_model.wallet_address,
    ) = BlockchainWrapper.create_wallet(user.passphrase)
    user_model.wallet_hash = user_model.wallet_hash.digest()

    db.add(user_model)
    db.commit()
    db.flush()
    return JSONResponse(
        status_code=200,
        content={
            "status": "success",
        },
    )


@app.post("/api/v1/register_bank_user")
async def register_new_bank_user(user: schemas.BankUser, db: Session = Depends(get_db)):
    user_model: models.BankUser = models.BankUser(login=user.login)
    user_by_login = user_loader(user.login)
    if user_by_login:
        return JSONResponse(
            status_code=400,
            content={
                "result": "error",
                "result_description": "User with this email already exists",
            },
        )
    bank_model: models.Bank = models.Bank(name=user.bank)
    bank = db.query(models.Bank).filter(models.Bank.name == user.bank).one_or_none()

    if not bank:
        (
            bank_model.cipher_initialization_vector,
            bank_model.blockchain_wallet,
            bank_model.wallet_hash,
            bank_model.wallet_address,
        ) = BlockchainWrapper.create_wallet(user.passphrase)
        bank_model.wallet_hash = bank_model.wallet_hash.digest()
        db.add(bank_model)
        db.commit()
        db.flush()
    else:
        bank_model = bank

    user_model.bank_id = bank_model.id
    user_model.password, user_model.salt = hash_password(user.password)
    db.add(user_model)
    db.commit()
    db.flush()


@app.post("/api/v1/register_insurer_user")
async def register_new_insurer_user(
    user: schemas.InsurerUser, db: Session = Depends(get_db)
):
    user_model: models.InsurerUser = models.InsurerUser(login=user.login)
    user_by_login = user_loader(user.login)
    if user_by_login:
        return JSONResponse(
            status_code=400,
            content={
                "result": "error",
                "result_description": "User with this email already exists",
            },
        )
    insurer_model: models.Insurer = models.Insurer(name=user.insurer)
    insurer = (
        db.query(models.Insurer)
        .filter(models.Insurer.name == user.insurer)
        .one_or_none()
    )
    if not insurer:
        (
            insurer_model.cipher_initialization_vector,
            insurer_model.blockchain_wallet,
            insurer_model.wallet_hash,
            insurer_model.wallet_address,
        ) = BlockchainWrapper.create_wallet(user.passphrase)
        insurer_model.wallet_hash = insurer_model.wallet_hash.digest()
        db.add(insurer_model)
        db.commit()
        db.flush()
    else:
        insurer_model = insurer

    user_model.insurer_id = insurer_model.id
    user_model.password, user_model.salt = hash_password(user.password)
    db.add(user_model)
    db.commit()
    db.flush()


@app.post("/api/v1/check_pass_phrase")
async def check_pass_phrase(passphrase: str, user=Depends(manager), db=Depends(get_db)):
    checking_entry = None
    if user is models.BankUser:
        checking_entry = db.query(models.Bank).filter(id == user.bank_id).one()
    elif user is models.InsurerUser:
        checking_entry = db.query(models.Insurer).filter(id == user.insurer_id).one()
    else:
        checking_entry = user

    cipher_key = hashlib.sha256(passphrase.encode()).digest()
    cipher_config = AES.new(
        cipher_key, AES.MODE_CBC, checking_entry.cipher_initialization_vector
    )
    private_wallet_key = cipher_config.decrypt(checking_entry.blockchain_wallet)
    return {
        "result": hashlib.sha256(private_wallet_key).digest()
        == checking_entry.wallet_hash,
    }


@app.post("/api/v1/get_encrypted_private_key")
async def get_encrypted_private_key(user=Depends(manager)):
    if not isinstance(user, models.Client):
        return JSONResponse(
            status_code=401,
            content={"result": "error", "result_description": "Client only method"},
        )

    return user.blockchain_wallet.hex()


@app.get("/api/v1/search_contract/{contruct_number}", response_model=schemas.Contract)
async def get_contract(contruct_number: str, user=Depends(manager), db=Depends(get_db)):
    if isinstance(user, models.BankUser):
        contract = (
            db.query(models.Contract)
            .filter(
                or_(models.Contract.bank_id == user.bank_id),
                models.Contract.contract_number == contruct_number,
            )
            .one_or_none()
        )
    elif isinstance(user, models.InsurerUser):
        contract = (
            db.query(models.Contract)
            .filter(
                or_(
                    models.Contract.insurer_id == user.id,
                ),
                models.Contract.contract_number == contruct_number,
            )
            .one_or_none()
        )
    else:
        contract = (
            db.query(models.Contract)
            .filter(
                or_(
                    models.Contract.client_id == user.id,
                ),
                models.Contract.contract_number == contruct_number,
            )
            .one_or_none()
        )
    if contract is None:
        JSONResponse(status_code=404, content={"result": "Not found"})

    return contract
