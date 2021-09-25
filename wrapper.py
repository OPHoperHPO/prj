import web3
import eth_account
from pathlib import Path
from solcx import compile_source


class BaseContractWrapper:
    def __init__(self, rpc_address: str, contract_file: Path, contract_name: str):
        self.web3 = web3.Web3(web3.HTTPProvider(rpc_address))
        self.contract_name = contract_name
        self.abi, self.bytecode = self.compile_contract(contract_file)

    def compile_contract(self, sol_file: Path):
        """Compiles solidity contract."""
        if isinstance(sol_file, str):
            with open(sol_file) as f:
                src = f.read()
        elif isinstance(sol_file, Path):
            src = sol_file.read_text()
        else:
            raise NotImplemented("Unknown type of input sol filepath")
        compiled_sol = compile_source(src, optimize=True, allow_paths=[Path("./")])
        contract = compiled_sol[f'<stdin>:{self.contract_name}']
        bytecode = contract['bin']
        abi = contract['abi']
        return abi, bytecode

    def get_contract_by_address(self, contract_address):
        contract = self.web3.eth.contract(address=contract_address,
                                          abi=self.abi)
        return contract


class ContractWrapper(BaseContractWrapper):
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

    def get_bank_address(self, contract_address):
        contract = self.get_contract_by_address(contract_address)
        return contract.functions.bankAddress().call()

    def get_bank_name(self, contract_address):
        contract = self.get_contract_by_address(contract_address)
        return contract.functions.bankName().call()

    def get_insurance_company_name(self, contract_address):
        contract = self.get_contract_by_address(contract_address)
        return contract.functions.insCompName().call()

    def get_ins_company_address(self, contract_address):
        contract = self.get_contract_by_address(contract_address)
        return contract.functions.insCompAddress().call()

    def get_user_address(self, contract_address,
                         account: eth_account.account.LocalAccount):
        contract = self.get_contract_by_address(contract_address)
        # TODO Пофиксить проблему с помощью обработки raw транзакций.
        #  Как выход создавать новый объект при каждом запросе
        #  Во время множества асинхронных запросов к функции может произойти коллизия аккаунтов
        #  и она вернёт ошибку доступа.
        self.web3.eth.default_account = account.address

        return contract.functions.getContractAddresses().call()[0]

    def get_insurance_contract_address(self, contract_address,
                                       account: eth_account.account.LocalAccount):
        contract = self.get_contract_by_address(contract_address)
        # TODO Пофиксить проблему с помощью обработки raw транзакций.
        #  Как выход создавать новый объект при каждом запросе
        #  Во время множества асинхронных запросов к функции может произойти коллизия аккаунтов
        #  и она вернёт ошибку доступа.
        self.web3.eth.default_account = account.address

        return contract.functions.getContractAddresses().call()[3]

    def is_active(self, contract_address,
                  account: eth_account.account.LocalAccount):
        contract = self.get_contract_by_address(contract_address)
        # TODO Пофиксить проблему с помощью обработки raw транзакций.
        #  Как выход создавать новый объект при каждом запросе
        #  Во время множества асинхронных запросов к функции может произойти коллизия аккаунтов
        #  и она вернёт ошибку доступа.
        self.web3.eth.default_account = account.address

        return contract.functions.isActive().call()

    def is_expired(self, contract_address,
                   account: eth_account.account.LocalAccount):
        contract = self.get_contract_by_address(contract_address)
        # TODO Пофиксить проблему с помощью обработки raw транзакций.
        #  Как выход создавать новый объект при каждом запросе
        #  Во время множества асинхронных запросов к функции может произойти коллизия аккаунтов
        #  и она вернёт ошибку доступа.
        self.web3.eth.default_account = account.address

        return contract.functions.isExpired().call()

    def indebtedness_update(self, amount: int, endTimestamp: int, contract_address,
                            account: eth_account.account.LocalAccount):
        contract = self.get_contract_by_address(contract_address)
        transaction = contract.functions.indebtednessUpdate(
            amount, endTimestamp
        ).buildTransaction({
            'gas': 4712388,
            'gasPrice': 100000000000,
            'from': account.address,
            'nonce': self.web3.eth.get_transaction_count(account.address)
        })
        signed_txn = self.web3.eth.account.signTransaction(transaction,
                                                           private_key=account.privateKey)
        self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return True

    def get_contract_info(self, contract_address,
                          account: eth_account.account.LocalAccount):
        contract = self.get_contract_by_address(contract_address)
        # TODO Пофиксить проблему с помощью обработки raw транзакций.
        #  Как выход создавать новый объект при каждом запросе
        #  Во время множества асинхронных запросов к функции может произойти коллизия аккаунтов
        #  и она вернёт ошибку доступа.
        self.web3.eth.default_account = account.address

        data = contract.functions.getContractInfo().call()
        nt = ["is_active",
              "is_expired",
              "userFullname",
              "creditContractNumber",
              "creditContractTimestamp",
              "contractNumber",
              "contractTimestamp",
              "totalAmount",
              "paymentTimestamp",
              "paymentAmount",
              "indebtednessAmount",
              "indebtednessDate",
              "contractRisks",
              "contractRisksType"]
        return dict(zip(nt, data))

    def createInsurnanceCase(self, reason: str, condition: str,
                             phoneNumber: str,
                             email: str,
                             damageAmount: int,
                             damageDate: int,
                             contract_address,
                             account: eth_account.account.LocalAccount):
        contract = self.get_contract_by_address(contract_address)
        transaction = contract.functions.createInsurnanceCase(
            reason, condition, phoneNumber, email, damageAmount, damageDate
        ).buildTransaction({
            'gas': 4712388,
            'gasPrice': 100000000000,
            'from': account.address,
            'nonce': self.web3.eth.get_transaction_count(account.address)
        })
        signed_txn = self.web3.eth.account.signTransaction(transaction,
                                                           private_key=account.privateKey)
        self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return self.get_insurance_contract_address(contract_address, account)

    def deactivate(self, contract_address,
                   account: eth_account.account.LocalAccount):
        contract = self.get_contract_by_address(contract_address)
        transaction = contract.functions.deactivateContract(
        ).buildTransaction({
            'gas': 4712388,
            'gasPrice': 100000000000,
            'from': account.address,
            'nonce': self.web3.eth.get_transaction_count(account.address)
        })
        signed_txn = self.web3.eth.account.signTransaction(transaction,
                                                           private_key=account.privateKey)
        self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return True

    def set_payment_recieved(self, payment_timestamp: int, payment_amount: int,
                             contract_address,
                             account: eth_account.account.LocalAccount):
        contract = self.get_contract_by_address(contract_address)
        transaction = contract.functions.setPaymentRecieved(
            payment_timestamp, payment_amount
        ).buildTransaction({
            'gas': 4712388,
            'gasPrice': 100000000000,
            'from': account.address,
            'nonce': self.web3.eth.get_transaction_count(account.address)
        })
        signed_txn = self.web3.eth.account.signTransaction(transaction,
                                                           private_key=account.privateKey)
        self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return True


class InsurnanceCaseContractWrapper(BaseContractWrapper):

    def get_contract_by_address(self, contract_address):
        contract = self.web3.eth.contract(address=contract_address,
                                          abi=self.abi)
        return contract

    def get_contract_info(self, contract_address,
                          account: eth_account.account.LocalAccount):
        contract = self.get_contract_by_address(contract_address)
        # TODO Пофиксить проблему с помощью обработки raw транзакций.
        #  Как выход создавать новый объект при каждом запросе
        #  Во время множества асинхронных запросов к функции может произойти коллизия аккаунтов
        #  и она вернёт ошибку доступа.
        self.web3.eth.default_account = account.address

        data = contract.functions.getInfo().call()
        nt = ["parentContractAddress",
              "reason",
              "condition",
              "phoneNumber",
              "email",
              "happenedDate",
              "damageAmount",
              "isPaymentConfirmed",
              "isClosed",
              "paymentAmount",
              "isPaymentConfirmedByBank",
              "rejectCause"]
        return dict(zip(nt, data))

    def close_reject(self,
                     cause: str,
                     contract_address,
                     account: eth_account.account.LocalAccount):
        contract = self.get_contract_by_address(contract_address)
        transaction = contract.functions.createInsurnanceCase(cause) \
            .buildTransaction({
            'gas': 4712388,
            'gasPrice': 100000000000,
            'from': account.address,
            'nonce': self.web3.eth.get_transaction_count(account.address)
        })
        signed_txn = self.web3.eth.account.signTransaction(transaction,
                                                           private_key=account.privateKey)
        self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return True

    def confirm_payment_from_bank(self,
                                  contract_address,
                                  account: eth_account.account.LocalAccount):
        contract = self.get_contract_by_address(contract_address)
        transaction = contract.functions.confirmPaymentFromBank() \
            .buildTransaction({
            'gas': 4712388,
            'gasPrice': 100000000000,
            'from': account.address,
            'nonce': self.web3.eth.get_transaction_count(account.address)
        })
        signed_txn = self.web3.eth.account.signTransaction(transaction,
                                                           private_key=account.privateKey)
        self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return True

    def confirm_by_insurance_company(self,
                                     payment_amount: int,
                                     contract_address,
                                     account: eth_account.account.LocalAccount):
        contract = self.get_contract_by_address(contract_address)
        transaction = contract.functions.confirm(payment_amount) \
            .buildTransaction({
            'gas': 4712388,
            'gasPrice': 100000000000,
            'from': account.address,
            'nonce': self.web3.eth.get_transaction_count(account.address)
        })
        signed_txn = self.web3.eth.account.signTransaction(transaction,
                                                           private_key=account.privateKey)
        self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return True

    def update(self,
               reason: str,
               condition: str,
               phoneNumber: str,
               email: str,
               damageAmount: int,
               damageDate: int,
               contract_address,
               account: eth_account.account.LocalAccount):
        contract = self.get_contract_by_address(contract_address)
        transaction = contract.functions.update(reason,
                                                condition,
                                                phoneNumber,
                                                email,
                                                damageAmount,
                                                damageDate) \
            .buildTransaction({
            'gas': 4712388,
            'gasPrice': 100000000000,
            'from': account.address,
            'nonce': self.web3.eth.get_transaction_count(account.address)
        })
        signed_txn = self.web3.eth.account.signTransaction(transaction,
                                                           private_key=account.privateKey)
        self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return True
