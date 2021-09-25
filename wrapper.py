import web3
import eth_account
from pathlib import Path
from solcx import compile_source


class ContractWrapper:
    def __init__(self, rpc_address: str, contract_file: Path):
        self.web3 = web3.Web3(web3.HTTPProvider(rpc_address))
        self.abi, self.bytecode = self.compile_contract(contract_file)

    @staticmethod
    def compile_contract(sol_file: Path):
        """Compiles solidity contract."""
        if isinstance(sol_file, str):
            with open(sol_file) as f:
                src = f.read()
        elif isinstance(sol_file, Path):
            src = sol_file.read_text()
        else:
            raise NotImplemented("Unknown type of input sol filepath")
        compiled_sol = compile_source(src, optimize=True, allow_paths=[Path("./")])
        contract = compiled_sol['<stdin>:Contract']
        bytecode = contract['bin']
        abi = contract['abi']
        return abi, bytecode

    def create(self,
               insurer_account: eth_account.account.LocalAccount,
               info: dict,
               gas=4712388,
               gas_price=100000000000) -> str:
        """Deploys contract to blockchain from specific account"""

        contract = self.web3.eth.contract(abi=self.abi, bytecode=self.bytecode)
        tx_hash = contract.constructor(
            info["bankAddress"],
            info["userAddress"],
            info["bankName"],
            info["insCompName"],
            info["userInfo"]["fullName"],
            info["userInfo"]["creditContractNumber"],
            info["userInfo"]["creditContractTimestamp"],
            info["userInfo"]["contractNumber"],
            info["userInfo"]["totalAmount"],
            info["userInfo"]["contractRisksType"], ).buildTransaction(
            {
                'gas': gas,
                'gasPrice': gas_price,
                'from': insurer_account.address,
                'nonce': self.web3.eth.get_transaction_count(insurer_account.address, "pending")
            })
        signed_txn = self.web3.eth.account.signTransaction(tx_hash, private_key=insurer_account.privateKey)
        contract_hash = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        contract_tx_info = self.web3.eth.wait_for_transaction_receipt(contract_hash)
        contract_address = contract_tx_info["contractAddress"]
        return contract_address

    def get_contract_by_address(self, contract_address):
        contract = self.web3.eth.contract(address=contract_address,
                                          abi=self.abi)
        return contract

    def get_bank_address(self, contract_address):
        contract = self.get_contract_by_address(contract_address)
        return contract.functions.bankAddress().call()

    def get_ins_company_address(self, contract_address):
        contract = self.get_contract_by_address(contract_address)
        return contract.functions.insCompAddress().call()

    def get_user_address(self, contract_address,
                         account: eth_account.account.LocalAccount):
        contract = self.get_contract_by_address(contract_address)
        return contract.functions.getContractAddresses().call()
