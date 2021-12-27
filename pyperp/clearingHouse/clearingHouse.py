from pyperp import ApiProvider
from pyperp.clearingHouse.types import (
    AddLiquidityParams,
    OpenPositionParams,
    ClosePositionParams,
    RemoveLiquidityParams
)
from types import GasParams
from web3 import Web3
from eth_account import Account

class ClearingHouse:
    def __init__(self, provider: ApiProvider, wallet: Account):
        self._provider = provider
        self.account = account
        self.logger = logging.getLogger("ClearingHouse")

        logging.info("Loading ClearingHouse contract")
        _clearing_house_meta = self._provider.load_meta("ClearingHouse")
        self._clearing_house = self._provider.api.eth.contract(
            address=_clearing_house_meta["address"],
            abi=_clearing_house_meta["abi"]
        )
        logging.info("ClearingHouse contract loaded")

        logging.info("Loading USDC contract")
        _USDC_meta = self._provider.load_meta("USDC")
        self._USDC = self._provider.api.eth.contract(
            address=_USDC_meta["address"],
            abi=_USDC_meta["abi"]
        )
        logging.info("USDC contract loaded")


    def approve_clearinghouse_to_use_usdc(
        self,
        gas_params: GasParams
    ):
        logging.info("Approving ClearingHouse to use USDC")
        nonce = self._provider.api.eth.get_transaction_count(
            self.account.address
        )
        tx = self._USDC.functions.approve(
            _clearing_house_meta["address"],
            2**256-1
        ).buildTransaction({
            'nonce': nonce,
            **gas_params
        })

    
    def add_liquidity(
        params: AddLiquidityParams,
        gas_params: GasParams
    ):
        nonce = self._provider.eth.get_transaction_count(self.wallet.address)
        tx = self._clearing_house.functions.addLiquidity(
            params.toDict()
        ).buildTransaction({
            'nonce': nonce,
            **gas_params.toDict()
        })

        signed_tx = self._provider.eth.sign_transaction(
            tx, self.wallet.key
        )

        receipt = self._provider.eth.send_raw_transaction(
            signed_tx.rawTransaction
        )

        return receipt

    def remove_liquidity(
        params: RemoveLiquidityParams,
        wallet: Account,
        gas_params: GasParams
    ):
        nonce = self._provider.eth.get_transaction_count(self.wallet.address)
        tx = self._clearing_house.functions.removeLiquidity(
            params.toDict()
        ).buildTransaction({
            'nonce': nonce,
            **gas_params.toDict()
        })

        signed_tx = self._provider.eth.sign_transaction(
            tx, self.wallet.key
        )

        receipt = self._provider.eth.send_raw_transaction(
            signed_tx.rawTransaction
        )

        return receipt

    def settle_all_funding(
        trader: str,
        gas_params: GasParams
    ):
        assert(
            Web3.isAddress(trader)
            f"Trader address {trader} must be an address"    
        )
        nonce = self._provider.eth.get_transaction_count(self.wallet.address)
        tx = self._clearing_house.functions.settleAllFunding(
            trader
        ).buildTransaction({
            'nonce': nonce,
            **gas_params.toDict()
        })

        signed_tx = self._provider.eth.sign_transaction(
            tx, self.wallet.key
        )

        receipt = self._provider.eth.send_raw_transaction(
            signed_tx.rawTransaction
        )

        return receipt

    def open_position(
        params: OpenPositionParams,
        gas_params: GasParams
    ):
        nonce = self._provider.eth.get_transaction_count(self.wallet.address)
        tx = self._clearing_house.functions.openPosition(
            params.toDict()
        ).buildTransaction({
            'nonce': nonce,
            **gas_params.toDict()
        })

        signed_tx = self._provider.eth.sign_transaction(
            tx, self.wallet.key
        )

        receipt = self._provider.eth.send_raw_transaction(
            signed_tx.rawTransaction
        )

        return receipt

    def close_position(
        params: ClosePositionParams,
        gas_params: GasParams
    ):
        nonce = self._provider.eth.get_transaction_count(self.wallet.address)
        tx = self._clearing_house.functions.closePosition(
            params.toDict()
        ).buildTransaction({
            'nonce': nonce,
            **gas_params.toDict()
        })

        signed_tx = self._provider.eth.sign_transaction(
            tx, self.wallet.key
        )

        receipt = self._provider.eth.send_raw_transaction(
            signed_tx.rawTransaction
        )

        return receipt

    def liquidate(
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

        nonce = self._provider.eth.get_transaction_count(self.wallet.address)
        tx = self._clearing_house.functions.liquidate(
            trader,
            base_token
        ).buildTransaction({
            'nonce': nonce,
            **gas_params.toDict()
        })

        signed_tx = self._provider.eth.sign_transaction(
            tx, self.wallet.key
        )

        receipt = self._provider.eth.send_raw_transaction(
            signed_tx.rawTransaction
        )

        return receipt

    #TODO: implement cancelExcessOrders

    def cancel_all_excess_orders(
        maker: str,
        base_token: str,
        gas_params: GasParams
    ):
        assert(
            Web3.isAddress(trader),
            f'Maker address {maker} must be a checksum address'
        )
        assert(
            Web3.isAddress(base_token),
            f'Base Token address {base_token} must be a checkcum address'
        )

        nonce = self._provider.eth.get_transaction_count(self.wallet.address)
        tx = self._clearing_house.functions.cancelAllExcessOrders(
            maker,
            base_token
        ).buildTransaction({
            'nonce': nonce,
            **gas_params.toDict()
        })

        signed_tx = self._provider.eth.sign_transaction(
            tx, self.wallet.key
        )

        receipt = self._provider.eth.send_raw_transaction(
            signed_tx.rawTransaction
        )

        return receipt

    def close_position_in_closed_market(
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

        nonce = self._provider.eth.get_transaction_count(self.wallet.address)
        tx = self._clearing_house.functions.closePositionInClosedMarket(
            trader,
            base_token
        ).buildTransaction({
            'nonce': nonce,
            **gas_params.toDict()
        })

        signed_tx = self._provider.eth.sign_transaction(
            tx, self.wallet.key
        )

        receipt = self._provider.eth.send_raw_transaction(
            signed_tx.rawTransaction
        )

        return receipt

    def uniswap_v3_mint_callback(
        amount0Owed: int,
        amount1Owed: int,
        data: str,
        gas_params: GasParams
    ):
        nonce = self._provider.eth.get_transaction_count(self.wallet.address)
        tx = self._clearing_house.functions.uninswapV3MintCallback(
            amount0Owed,
            amount1Owed,
            data
        ).buildTransaction({
            'nonce': nonce,
            **gas_params.toDict()
        })

        signed_tx = self._provider.eth.sign_transaction(
            tx, self.wallet.key
        )

        receipt = self._provider.eth.send_raw_transaction(
            signed_tx.rawTransaction
        )

        return receipt

    def uniswap_v3_mint_callback(
        amount0Delta: int,
        amount1Delta: int,
        data: str,
        gas_params: GasParams
    ):
        nonce = self._provider.eth.get_transaction_count(self.wallet.address)
        tx = self._clearing_house.functions.uninswapV3SwapCallback(
            amount0Delta,
            amount1Delta,
            data
        ).buildTransaction({
            'nonce': nonce,
            **gas_params.toDict()
        })

        signed_tx = self._provider.eth.sign_transaction(
            tx, self.wallet.key
        )

        receipt = self._provider.eth.send_raw_transaction(
            signed_tx.rawTransaction
        )

        return receipt

    def get_quote_token():
        return self._clearing_house.functions.getQuoteToken(
        ).call()

    def get_uniswap_v3_factory():
        return self._clearing_house.functions.getUniswapV3Factory(
        ).call()

    def get_clearing_house_config():
        return self._clearing_house.functions.getClearingHouseConfig(
        ).call()
    
    def get_vault():
        return self._clearing_house.functions.getVault().call()

    def get_exchange():
        return self._clearing_house.functions.getExchange().call()

    def get_order_book():
        return self._clearing_house.functions.getOrderBook().call()

    def get_account_balance():
        return self._clearing_house.functions.getAccountBalance().call()

    def get_insurance_fund():
        return self._clearing_house.functions.getInsuraceFund().call()

    def get_account_value(
        trader: str
    ):
        assert(
            Web3.isAddress(trader),
            f'trader address {trader} must be a checksum address'
        )
        return self._clearing_house.functions.getAccountValue(trader).call()
