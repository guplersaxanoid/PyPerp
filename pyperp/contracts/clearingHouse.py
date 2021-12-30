from pyperp.providers import ApiProvider
from pyperp.contracts.types import (
    AddLiquidityParams,
    OpenPositionParams,
    ClosePositionParams,
    RemoveLiquidityParams
)
from pyperp.common.types import GasParams
from web3 import Web3
from eth_account import Account
import logging 
from dataclasses import astuple

class ClearingHouse:
    def __init__(self, provider: ApiProvider):
        self._provider = provider
        self.account = self._provider.account
        self.logger = logging.getLogger("ClearingHouse")

        self.logger.info("Loading ClearingHouse contract")
        clearing_house_meta = self._provider.load_meta("ClearingHouse")
        self.clearing_house = self._provider.api.eth.contract(
            address=clearing_house_meta["address"],
            abi=clearing_house_meta["abi"]
        )
        self.logger.info("ClearingHouse contract loaded")

        self.logger.info("Loading USDC contract")
        usdc_meta = self._provider.load_meta("USDC")
        self.usdc = self._provider.api.eth.contract(
            address=usdc_meta["address"],
            abi=usdc_meta["abi"]
        )
        self.logger.info("USDC contract loaded")

        self.logger.info("Loading vBTC contract")
        vbtc_meta = self._provider.load_meta("vBTC")
        self.vbtc = self._provider.api.eth.contract(
            address=vbtc_meta["address"],
            abi=vbtc_meta["abi"]
        )
        self.logger.info("vBTC contract loaded")

        #TODO: load vETH and approve usage


    def approve_clearinghouse_to_use_usdc(
        self,
        gas_params: GasParams
    ):
        logging.info("Approving ClearingHouse to use USDC")
        nonce = self._provider.api.eth.get_transaction_count(
            self.account.address
        )

        tx_params = {
            'nonce': nonce,
            **(gas_params.to_dict())
        }
        
        tx = self.usdc.functions.approve(
            self.clearing_house.address,
            2**256-1
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

    def approve_clearinghouse_to_use_vbtc(
        self,
        gas_params: GasParams
    ):
        logging.info("Approving ClearingHouse to use vBTC")
        nonce = self._provider.api.eth.get_transaction_count(
            self.account.address
        )

        tx_params = {
            'nonce': nonce,
            **(gas_params.to_dict())
        }
        
        tx = self.vbtc.functions.approve(
            self.clearing_house.address,
            2**256-1
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
    
    def add_liquidity(
        self,
        params: AddLiquidityParams,
        gas_params: GasParams
    ):
        nonce = self._provider.api.eth.get_transaction_count(
            self.account.address
        )

        tx_params = {
            'nonce': nonce,
            **(gas_params.to_dict())
        }

        tx = self.clearing_house.functions.addLiquidity(
            params.to_dict()
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

    def remove_liquidity(
        self,
        params: RemoveLiquidityParams,
        gas_params: GasParams
    ):
        nonce = self._provider.api.eth.get_transaction_count(self.wallet.address)
        
        tx_params = {
            'nonce': nonce,
            **(gas_params.to_dict())
        }

        tx = self.clearing_house.functions.removeLiquidity(
            astuple(params)
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

    def settle_all_funding(
        self,
        trader: str,
        gas_params: GasParams
    ):
        assert(
            Web3.isAddress(trader),
            f"Trader address {trader} must be an address"    
        )
        nonce = self._provider.api.eth.get_transaction_count(self.wallet.address)
        
        tx_params = {
            'nonce': nonce,
            **(gas_params.to_dict())
        }
        
        tx = self.clearing_house.functions.settleAllFunding(
            trader
        ).buildTransaction(tx_params)

        signed_tx = self._provider.api.eth.account.sign_transaction(
            tx, self.account.key.hex()
        )

        tx_hash = self._provider.api.eth.send_raw_transaction(
            signed_tx.rawTransaction
        )

        receipt = self._provider.api.eth.wait_for_transaction_receipt(
            tx_hash
        )

        return receipt

    def open_position(
        self,
        params: OpenPositionParams,
        gas_params: GasParams
    ):
        nonce = self._provider.api.eth.get_transaction_count(
            self.account.address
        )
        
        tx_params = {
            'nonce': nonce,
            **(gas_params.to_dict())
        }

        tx = self.clearing_house.functions.openPosition(
            astuple(params)
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

    def close_position(
        self,
        params: ClosePositionParams,
        gas_params: GasParams
    ):
        nonce = self._provider.api.eth.get_transaction_count(
            self.account.address
        )
        
        tx_params = {
            'nonce': nonce,
            **(gas_params.to_dict())
        }
        
        tx = self.clearing_house.functions.closePosition(
            astuple(params)
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

    def liquidate(
        self,
        trader: str,
        base_token: str,
        gas_params: GasParams
    ):
        assert(
            Web3.isAddress(trader),
            f'trader address {trader} must be a checksum address'
        )
        assert(
            Web3.isAddress(base_token),
            f'Base Token address {base_token} must be a checkcum address'
        )

        nonce = self._provider.api.eth.get_transaction_count(self.wallet.address)
        
        tx_params = {
            'nonce': nonce,
            **(gas_params.to_dict())
        }
        
        tx = self.clearing_house.functions.liquidate(
            trader,
            base_token
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

    #TODO: implement cancelExcessOrders

    def cancel_all_excess_orders(
        self,
        maker: str,
        base_token: str,
        gas_params: GasParams
    ):
        assert(
            Web3.isAddress(maker),
            f'Maker address {maker} must be a checksum address'
        )
        assert(
            Web3.isAddress(base_token),
            f'Base Token address {base_token} must be a checksum address'
        )

        nonce = self._provider.api.eth.get_transaction_count(
            self.account.address
        )
        
        tx_params = {
            'nonce': nonce,
            **(gas_params.to_dict())
        }
        
        tx = self.clearing_house.functions.cancelAllExcessOrders(
            maker,
            base_token
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

    def close_position_in_closed_market(
        self,
        trader: str,
        base_token: str,
        gas_params: GasParams
    ):
        assert(
            Web3.isAddress(trader),
            f'trader address {trader} must be a checksum address'
        )
        assert(
            Web3.isAddress(base_token),
            f'Base Token address {base_token} must be a checkcum address'
        )

        nonce = self._provider.api.eth.get_transaction_count(
            self.account.address
        )
        
        tx_params = {
            'nonce': nonce,
            **(gas_params.to_dict())
        }
        
        tx = self.clearing_house.functions.closePositionInClosedMarket(
            trader,
            base_token
        ).buildTransaction({
            'nonce': nonce,
            **gas_params.to_dict()
        })

        signed_tx = self._provider.api.eth.sign_transaction(
            tx, self.wallet.key
        )

        receipt = self._provider.api.eth.send_raw_transaction(
            signed_tx.rawTransaction
        )

        return receipt

    def uniswap_v3_mint_callback(
        self,
        amount0Owed: int,
        amount1Owed: int,
        data: str,
        gas_params: GasParams
    ):
        nonce = self._provider.api.eth.get_transaction_count(
            self.account.address
        )
        
        tx_params = {
            'nonce': nonce,
            **(gas_params.to_dict())
        }
        
        tx = self.clearing_house.functions.uninswapV3MintCallback(
            amount0Owed,
            amount1Owed,
            data
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

    def uniswap_v3_mint_callback(
        self,
        amount0Delta: int,
        amount1Delta: int,
        data: str,
        gas_params: GasParams
    ):
        nonce = self._provider.api.eth.get_transaction_count(
            self.account.address
        )
        
        tx_params = {
            'nonce': nonce,
            **(gas_params.to_dict())
        }
        
        tx = self.clearing_house.functions.uninswapV3SwapCallback(
            amount0Delta,
            amount1Delta,
            data
        ).buildTransaction(tx_params)

        signed_tx = self._provider.api.eth.account.sign_transaction(
            tx, self.account.key.hex()
        )

        tx_hash = self._provider.api.eth.send_raw_transaction(
            signed_tx.rawTransaction
        )

        receipt = self._provider.api.eth.wait_for_transaction_receipt(
            tx_hash
        )

        return receipt

    def get_quote_token(self):
        return self.clearing_house.functions.getQuoteToken(
        ).call()

    def get_uniswap_v3_factory(self):
        return self.clearing_house.functions.getUniswapV3Factory(
        ).call()

    def getclearing_house_config(self):
        return self.clearing_house.functions.getClearingHouseConfig(
        ).call()
    
    def get_vault(self):
        return self.clearing_house.functions.getVault().call()

    def get_exchange(self):
        return self.clearing_house.functions.getExchange().call()

    def get_order_book(self):
        return self.clearing_house.functions.getOrderBook().call()

    def get_account_balance(self):
        return self.clearing_house.functions.getAccountBalance().call()

    def get_insurance_fund(self):
        return self.clearing_house.functions.getInsuraceFund().call()

    def get_account_value(
        self,
        trader: str
    ):
        assert(
            Web3.isAddress(trader),
            f'trader address {trader} must be a checksum address'
        )
        return self.clearing_house.functions.getAccountValue(trader).call()
