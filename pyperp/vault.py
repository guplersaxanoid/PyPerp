from pyperp import ApiProvider
from web3 import Web3 
from eth_account import Account
import logging
from pyperp.types import (
    GasParams
)

class Vault:
    def __init__(
        self,
        provider: ApiProvider,
        wallet: Account
    ):
        self.provider = provider
        self.wallet = wallet
        self.logger = logging.logger("Vault")
        
        logging.info("Loading Vault contract")
        _vault_meta = self._provider.load_meta("Vault")
        self._vault = self._provider._api.eth.contract(
            address=_vault_meta["address"],
            abi=_vault_meta["abi"]
        )
        logging.info("Vault contract loaded")

    def deposit(
        self,
        token: str,
        amount_x10_D: str,
        gas_params: GasParams
    ):
        nonce = self._provider.eth.get_transaction_count(self.wallet.address)
        tx = self._vault.functions.deposit(
            token,
            amount_x10_D
        ).buildTransaction({
            'nonce': nonce,
            **gas_params
        })

        signed_tx = self._provider.eth.sign_transaction(
            tx, self.wallet.key
        )

        receipt = self._provider.eth.send_raw_transaction(
            signed_tx
        )

        return receipt

    def deposit_for(
        self,
        to: str,
        token: str,
        amount_x10_D: str,
        gas_params: GasParams
    ):
        nonce = self._provider.eth.get_transaction_count(self.wallet.address)
        tx = self._vault.functions.depositFor(
            to,
            token,
            amount_x10_D
        ).buildTransaction({
            'nonce': nonce,
            **gas_params
        })

        signed_tx = self._provider.eth.sign_transaction(
            tx, self.wallet.key
        )

        receipt = self._provider.eth.send_raw_transaction(
            signed_tx
        )

        return receipt

    def withdraw(
        self,
        token: str,
        amount_x10_D: str,
        gas_params: GasParams
    ):
        nonce = self._provider.eth.get_transaction_count(self.wallet.address)
        tx = self._vault.functions.withdraw(
            token,
            amount_x10_D
        ).buildTransaction({
            'nonce': nonce,
            **gas_params
        })

        signed_tx = self._provider.eth.sign_transaction(
            tx, self.wallet.key
        )

        receipt = self._provider.eth.send_raw_transaction(
            signed_tx
        )

        return receipt

    def get_settlement_token(self):
        return self._vault.functions.getSettlementToken(
        ).call()

    def decimals(self):
        return self._vault.functions.decimals().call()
    
    def get_total_debt(self):
        return self._vault.functions.getTotalDebt().call()

    def get_clearing_house_config(self):
        return self._vault.functions.getClearingHouseConfig().call()
    
    def get_account_balance(self):
        return self._vault.functions.getAccountBalance().call()

    def get_insurance_fund(self):
        return self._vault.functions.getInsuranceFund().call()

    def get_exchange(self):
        return self._vault.functions.getExchange().call()

    def get_clearing_house(self):
        return self._vault.functions.getClearingHouse().call()

    def get_free_collateral(self):
        return self._vault.functions.getFreeCollateral().call()

    def get_balance(
        self,
        trader: str
    ):
        return self._vault.functions.getBalance(trader).call()

    def get_free_collateral_by_ratio(
        self,
        trader: str,
        ratio: int
    ):
        return self._vault.functions.getFreeCollateralByRatio(
            trader, ratio
        ).call()