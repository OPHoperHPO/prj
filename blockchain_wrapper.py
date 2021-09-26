import hashlib
import random
import time

import eth_account.signers.local
from web3 import Web3, HTTPProvider
from solcx import compile_source
from models import models
from Crypto.Cipher import AES
from Crypto import Random

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
        key = hashlib.sha256(passfrase.encode()).digest()
        initialization_vector = Random.new().read(AES.block_size)
        cipher_config = AES.new(key, AES.MODE_CBC, initialization_vector)
        pk = web3.eth.account.create(time.time_ns()).privateKey
        return initialization_vector, cipher_config.encrypt(pk), hashlib.sha256(pk)

    def create_contract(
        self, insurer: models.Insurer, bank: models.Bank, client: models.Client
    ):
        contract = web3.eth.contract(*self.compile_contract())
        tx_hash = contract.constructor(bank.blockchain_wallet)

    @staticmethod
    def get_wallet(private_key):
        try:
            return web3.eth.account.from_key(private_key)
        except ValueError:
            return None
