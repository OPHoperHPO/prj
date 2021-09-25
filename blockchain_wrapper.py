import time

import eth_account.signers.local
from web3 import Web3, HTTPProvider
from solcx import compile_source
from models import models
from Crypto.Cipher import AES

web3 = Web3(
    HTTPProvider("https://ropsten.infura.io/v3/15e005648051497a81b7d1c4ce4b8d12")
)


class BlockchainWrapper:
    def __init__(self):
        self.abi, self.bytecode = self.compile_contract()

    @staticmethod
    def compile_contract(contract_path="contract.sol"):
        compiled_sol = compile_source(open(contract_path).read(), optimize=True)
        contract_id, contract_interface = compiled_sol.popitem()
        bytecode = contract_interface["bin"]
        abi = contract_interface["abi"]
        return abi, bytecode

    @staticmethod
    def create_wallet(passfrase):
        return web3.eth.account.create(time.time_ns()).privateKey

    def create_contract(
        self, insurer: models.Insurer, bank: models.Bank, client: models.Client
    ):
        contract = web3.eth.contract(*self.compile_contract())
        tx_hash = contract.constructor(bank.blockchain_wallet)
