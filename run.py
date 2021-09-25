import time
from pathlib import Path
from wrapper import ContractWrapper

contract = ContractWrapper("http://127.0.0.1:8545", Path("contract.sol"))
insurer_account = contract.web3.eth.account.privateKeyToAccount(
    "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d")

contract_address = contract.create(insurer_account, {
    "userAddress": insurer_account.address,
    "bankAddress": insurer_account.address,
    "bankName": "SberBank",
    "insCompName": "INGOSTRAX",
    "userInfo": {
        "fullName": "Vladimir Putin",
        "creditContractNumber": 1,
        "creditContractTimestamp": int(time.time()),
        "contractNumber": 1,
        "totalAmount": 1000,
        "contractRisksType": "health"
    }
})

print(contract.get_ins_company_address(contract_address))
print(contract.get_bank_address(contract_address))
print(contract.get_user_address(contract_address, insurer_account))
print()
