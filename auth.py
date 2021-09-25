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

secret = "27416c619e2583dd7023ff9590b2d931458a11d58595971c96f566d1d5fa533c46413dca20bf7c99e12776a9da8bb3bdd2fa2cd65fb6a4\
8ac7a6bc3517b8d95229666d88887c1d8170907cce7ddb1d3b0e4dc6cc1a5f373d5293c77d0b042b8a5d965baeb28bf6006a732d3242e77c4f2b8e75\
e6a92055d442361c1a949a564c03f1862352508c4062562ff697320608af17a99050f493c4cb468419bfbd967cbfdadf70d01c2128c9ffccf143ad82\
4d5adb1d2a6715805dc99691e5158e4a8b34e44f0f91d3e44a89967f0ae46472082b8c14c97bf072095d0fce0a31c4e8883bd7025be7e005e1273b77\
07adc8da5ba42c01bb5cf837f2ff1b71c82caf5eb6"

manager = LoginManager(secret, token_url="/auth/token")


@manager.user_loader()
async def user_loader(email: str):
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

    user = await user_loader(email)

    if not user:
        raise InvalidCredentialsException
    elif not verify_password(password, user.salt, user.password):
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data={
            "sub": user.login,
            "rol": 0
            if user is models.BankUserWithBank
            else 1
            if user is models.InsurerUserWithInsurer
            else 2,
        }
    )

    response = JSONResponse(status_code=200, content={"result": "success"})

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
    user_model.blockchain_wallet = BlockchainWrapper.create_wallet(user.passphrase)
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
    bank_model: models.Bank = models.Bank(user.bank)
    bank = db.query(bank_model).one_or_none()
    if not bank:
        (
            bank_model.nonce,
            bank_model.blockchain_wallet,
            bank_model.tag,
        ) = BlockchainWrapper.create_wallet(user.passphrase)
        db.add(bank_model)
        db.commit()
        db.flush()
    else:
        bank_model = bank

    user_model.bank_id = bank_model.id
    db.add(user_model)
    db.commit()
    db.flush()


@app.post("/api/v1/register_insurer_user")
async def register_new_insurer_user(
    user: schemas.InsurerUser, db: Session = Depends(get_db)
):
    user_model: models.InsurerUser = models.InsurerUser(login=user.login)
    insurer_model: models.Insurer = models.Insurer(user.insurer)
    insurer = db.query(insurer_model).one_or_none()
    if not insurer:
        (
            insurer_model.nonce,
            insurer_model.blockchain_wallet,
            insurer_model.tag,
        ) = BlockchainWrapper.create_wallet(user.passphrase)
        db.add(insurer_model)
        db.commit()
        db.flush()
    else:
        insurer_model = insurer

    user_model.bank_id = insurer_model.id
    db.add(user_model)
    db.commit()
    db.flush()


@app.post("/api/v1/check_pass_phrase")
async def check_pass_phrase(passphrase: str, user=Depends(manager)):
    pass
