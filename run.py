import time
from pathlib import Path

from wrapper import ContractWrapper

contract = ContractWrapper("http://127.0.0.1:8545", Path("contract.sol"))
insurer_account = contract.web3.eth.account.privateKeyToAccount(
    "0x4f3edf983ac636a65a842ce7c78d9aa706d3b113bce9c46f30d7d21715b23b1d")
bank_account = contract.web3.eth.account.privateKeyToAccount(
    "0x6cbed15c793ce57650b9877cf6fa156fbef513c4e6134f022a85b1ffdd59b2a1")
user_account = contract.web3.eth.account.privateKeyToAccount(
    "0x6370fd033278c143179d81c5526140625662b8daa446c22ee2d73db3707e620c")

contract_address = contract.create(insurer_account, {
    "userAddress": user_account.address,
    "bankAddress": bank_account.address,
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

print("InsCompany_address:", contract.get_ins_company_address(contract_address))
print("Bank_address:", contract.get_bank_address(contract_address))
print("user address:", contract.get_user_address(contract_address, insurer_account))
print("is active:", contract.is_active(contract_address, insurer_account))
contract.set_payment_recieved(10, 10, contract_address, bank_account)
print("is active:", contract.is_active(contract_address, insurer_account))
print("Get Info:", contract.get_contract_info(contract_address, user_account))
