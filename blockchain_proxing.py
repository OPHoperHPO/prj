import auth
from wrapper import ContractWrapper
from pathlib import Path
import schemas
from auth import manager
from fastapi import Depends
from main import app, get_db
from models import models
from fastapi.responses import JSONResponse
from fastapi import Header
from blockchain_wrapper import BlockchainWrapper



@app.post("/api/v1/create_contract")
async def create_contract(
    contract_information: schemas.CreateContract,
    user=Depends(manager),
    db=Depends(get_db),
    authentication=Header(None),
):
    if not isinstance(user, models.InsurerUser):
        return JSONResponse(
            status_code=401,
            content={
                "result": "error",
                "result_description": "Only insurer can create contract",
            },
        )
    contract = ContractWrapper("http://127.0.0.1:8545", Path("contract.sol"), "Contract")
    new_account = False
    insurer_account = None
    bank_account = None
    user_account = None
    try:
        insurer_account = (
            db.query(models.Insurer).filter(models.Insurer.id == user.insurer_id).one()
        )
        bank_account = (
            db.query(models.Bank)
            .filter(models.Bank.id == contract_information.bank_name)
            .one()
        )
        user_account = (
            db.query(models.Client)
            .filter(models.Client.login == contract_information.email)
            .one_or_none()
        )

        if user_account is None:
            user_account = auth.register_new_user(
                schemas.User(
                    login=contract_information.email,
                    password=contract_information.client_password,
                    client_passphrase=contract_information.client_passphrase,
                )
            )
            new_account = True
    except:
        return JSONResponse(
            status_code=400,
            content={"result": "error", "result_description": "no insurer or bank"},
        )
    insurer_wallet = contract.web3.eth.account.privateKeyToAccount(
        await auth.get_pk(authentication, insurer_account)
    )
    bank_wallet = bank_account.wallet_address
    user_wallet = user_account.wallet_address

    contract_address = contract.create(
        insurer_account,
        {
            "userAddress": user_wallet,
            "bankAddress": bank_wallet,
            "bankName": contract_information.bank_name,
            "insCompName": insurer_account.name,
            "userInfo": {
                "fullName": contract_information.FIO,
                "creditContractNumber": contract_information.bank_number,
                "creditContractTimestamp": contract_information.bank_date,
                "contractNumber": contract_information.insurer_number,
                "totalAmount": contract_information.amount,
                "contractRisksType": contract_information.type,
            },
        },
    )

    contract_model = models.Contract(
        address=contract_address,
        contruct_number=contract_information.insurer_number,
        bank_id=bank_account.id,
        insurer_id=user.insurer_id,
        client_id=user_account.id,
    )
    db.add(contract_model)
    db.commit()
    db.flush()
    return JSONResponse(status_code=200, content={
        "address": contract_address,
        "new_account": new_account
    })
