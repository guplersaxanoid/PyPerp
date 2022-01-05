'''Vault class'''

from pyperp.providers import ApiProvider
import logging
from pyperp.common.types import (
    GasParams
)


class Vault:
    def __init__(
        self,
        provider: ApiProvider
    ):
        '''
        Initialize provider.
        Arguments:
        provider - an object of class derived from ApiProvider
        '''
        self._provider = provider
        self.account = self._provider.account
        self.logger = logging.getLogger("Vault")

        self.logger.info("Loading Vault contract")
        vault_meta = self._provider.load_meta("Vault")
        self.vault = self._provider._api.eth.contract(
            address=vault_meta["address"],
            abi=vault_meta["abi"]
        )
        self.logger.info("Vault contract loaded")

        self.logger.info("Loading USDC contract")
        usdc_meta = self._provider.load_meta("USDC")
        self.usdc = self._provider.api.eth.contract(
            address=usdc_meta["address"],
            abi=usdc_meta["abi"]
        )
        self.logger.info("USDC contract loaded")

    def approve_vault_to_use_usdc(
        self,
        gas_params: GasParams
    ):
        '''
        Approve Vault contract to use USDC
        Arguments:
        gas_params: GasParams object
        '''
        logging.info("Approving ClearingHouse to use USDC")
        nonce = self._provider.api.eth.get_transaction_count(
            self.account.address
        )

        tx_params = {
            'nonce': nonce,
            **(gas_params.to_dict())
        }

        tx = self.usdc.functions.approve(
            self.vault.address,
            2**256 - 1
        ).buildTransaction(tx_params)

        signed_tx = self._provider.api.eth.account.sign_transaction(
            tx, self.account.key.hex()
        )

        tx_hash = self._provider.api.eth.send_raw_transaction(
            signed_tx.rawTransaction.hex()
        )

        receipt = self._provider.api.eth.wait_for_transaction_receipt(
            tx_hash
        )

        return receipt

    def deposit(
        self,
        token: str,
        amount_x10_D: int,
        gas_params: GasParams
    ):
        '''
        Deposit collateral amount.
        Arguments:
        token - Token address
        amount_x10_D - amount to deposit
        gas_params - GasParams object
        '''
        nonce = self._provider.api.eth.get_transaction_count(
            self.account.address
        )

        tx_params = {
            'nonce': nonce,
            **(gas_params.to_dict())
        }

        tx = self.vault.functions.deposit(
            token,
            amount_x10_D
        ).buildTransaction(tx_params)

        signed_tx = self._provider.api.eth.account.sign_transaction(
            tx, self.account.key.hex()
        )

        tx_hash = self._provider.api.eth.send_raw_transaction(
            signed_tx.rawTransaction.hex()
        )

        receipt = self._provider.api.eth.wait_for_transaction_receipt(
            tx_hash
        )

        return receipt

    def deposit_for(
        self,
        to: str,
        token: str,
        amount_x10_D: int,
        gas_params: GasParams
    ):
        '''
        Deposit collateral for a different address.
        Arguments:
        to - wallet address to deposit to
        token - contract address of token
        amount_x10_D - amount to deposit
        gas_params - GasParams object
        '''
        nonce = self._provider.api.eth.get_transaction_count(
            self.account.address
        )

        tx_params = {
            'nonce': nonce,
            **(gas_params.to_dict())
        }

        tx = self.vault.functions.depositFor(
            to,
            token,
            amount_x10_D
        ).buildTransaction(tx_params)

        signed_tx = self._provider.api.eth.account.sign_transaction(
            tx, self.account.key.hex()
        )

        tx_hash = self._provider.api.eth.send_raw_transaction(
            signed_tx.rawTransaction.hex()
        )

        receipt = self._provider.api.eth.wait_for_transaction_receipt(
            tx_hash
        )

        return receipt

    def withdraw(
        self,
        token: str,
        amount_x10_D: int,
        gas_params: GasParams
    ):
        '''
        Withdraw collateral amount.
        Arguments:
        token - Token address
        amount_x10_D - amount to withdraw
        gas_params - GasParams object
        '''
        nonce = self._provider.api.eth.get_transaction_count(
            self.account.address
        )

        tx_params = {
            'nonce': nonce,
            **(gas_params.to_dict())
        }

        tx = self.vault.functions.withdraw(
            token,
            amount_x10_D
        ).buildTransaction(tx_params)

        signed_tx = self._provider.api.eth.account.sign_transaction(
            tx, self.account.key.hex()
        )

        tx_hash = self._provider.api.eth.send_raw_transaction(
            signed_tx.rawTransaction.hex()
        )

        receipt = self._provider.api.eth.wait_for_transaction_receipt(
            tx_hash
        )

        return receipt

    def get_settlement_token(self):
        '''
        Returns settlement token address.
        '''
        return self.vault.functions.getSettlementToken(
        ).call()

    def decimals(self):
        '''
        Returns number of decimals.
        '''
        return self.vault.functions.decimals().call()

    def get_total_debt(self):
        '''
        Returns total debt.
        '''
        return self.vault.functions.getTotalDebt().call()

    def get_clearing_house_config(self):
        '''
        Returns contract address of ClearingHouseConfig
        '''
        return self.vault.functions.getClearingHouseConfig().call()

    def get_account_balance(self):
        '''
        Returns contract address of AccountBalance
        '''
        return self.vault.functions.getAccountBalance().call()

    def get_insurance_fund(self):
        '''
        Returns contract address of InsuranceFund
        '''
        return self.vault.functions.getInsuranceFund().call()

    def get_exchange(self):
        '''
        Returns contract address of Exchange
        '''
        return self.vault.functions.getExchange().call()

    def get_clearing_house(self):
        '''
        Returns contract address of ClearingHouse
        '''
        return self.vault.functions.getClearingHouse().call()

    def get_free_collateral(
        self,
        trader: str
    ):
        '''
        Check how much collateral a trader can withdraw.
        Arguments:
        trader - wallet adderss of trader
        '''
        return self.vault.functions.getFreeCollateral(
            trader
        ).call()

    def get_balance(
        self,
        trader: str
    ):
        '''
        Returns vault balance of trader.
        Arguments:
        trader - wallet address of trader
        '''
        return self.vault.functions.getBalance(trader).call()

    def get_free_collateral_by_ratio(
        self,
        trader: str,
        ratio: int
    ):
        '''
        Returns free collateral by ratio.
        Arguments:
        trader - wallet address of trader
        ratio - ratio
        '''
        return self.vault.functions.getFreeCollateralByRatio(
            trader, ratio
        ).call()
