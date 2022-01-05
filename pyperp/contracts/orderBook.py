'''OrderBook class.'''

from pyperp.providers import ApiProvider
from web3 import Web3
from pyperp.contracts.types import (
    OpenOrderInfo,
    FundingGrowth
)
from typing import List
import logging
from hexbytes import HexBytes


class OrderBook:
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
        self.wallet = self._provider.account
        self.logger = logging.getLogger("OrderBook")

        self.logger.info("Loading OrderBook contract")
        order_book_meta = self._provider.load_meta("OrderBook")
        self.order_book = self._provider._api.eth.contract(
            address=order_book_meta["address"],
            abi=order_book_meta["abi"]
        )
        self.logger.info("OrderBook contract loaded")

    def get_exchange(self):
        '''
        Return address of Exchange Contract
        '''
        return self.order_book.functions.getExchange().call()

    def get_open_order_ids(
        self,
        trader: str,
        base_token: str,
    ):
        '''
        Return open order ids.
        Arguments:
        trader - wallet address of trader
        base_token - contract address of base token
        '''
        assert(
            Web3.isAddress(trader),
            f"Trader address {trader} must be a checksum address"
        )
        assert(
            Web3.isAddress(base_token),
            f"Base Token address {base_token} must be a checksum address"
        )

        return self.order_book.functions.getOpenOrderIds(
            trader,
            base_token
        ).call()

    def get_open_order_by_id(
        self,
        order_id: HexBytes
    ):
        '''
        Returns OpenOrderInfo for an order id.
        Arguments:
        orderId - HexBytes object representing order id.
        '''
        resp = self.order_book.functions.getOpenOrderById(
            order_id
        ).call()
        return OpenOrderInfo.from_tuple(resp)

    def get_open_order(
        self,
        trader: str,
        base_token: str,
        lower_tick: int,
        upper_tick: int
    ):
        '''
        Returns an open order.
        Arguments:
        trader - wallet address of a trader
        base_token - contract address of a base token
        lower_tick - lower tick
        upper_tick - upper tick
        '''
        resp = self.order_book.functions.getOpenOrder(
            trader,
            base_token,
            lower_tick,
            upper_tick
        ).call()
        return OpenOrderInfo.from_tuple(resp)

    def has_order(
        self,
        trader: str,
        tokens: List[str]
    ):
        '''
        Checks if trader has an order in given tokens.
        Arguments:
        trader - wallet address of a trader
        tokens - list of token addresses
        '''
        return self.order_book.functions.hasOrder(
            trader,
            tokens
        ).call()

    def get_total_quote_balance_and_pending_fee(
        self,
        trader: str,
        base_token: List[str]
    ):
        '''
        Returns total quote balance and pending fee
        Arguments:
        trader - wallet address of trader
        base_token - contract address of token
        '''
        resp = self.order_book.functions.getTotalQuoteBalanceAndPendingFee(
            trader,
            base_token
        ).call()

        return {
            'total_quote_amount_in_pools': resp[0],
            'total_pending_fee': resp[1]
        }

    def get_total_token_amount_in_pool_and_pending_fee(
        self,
        trader: str,
        base_token: str,
        fetch_base: bool
    ):
        '''
        Returns total token amount and pending fee.
        Arguments:
        trader - wallet address of trader
        base_token - contract address of base token
        fetch_base - fetch base
        '''
        resp = self.order_book.functions.getTotalTokenAmountInPoolAndPendingFee(
            trader,
            base_token,
            fetch_base
        ).call()

        return {
            'token_amount': resp[0],
            'pending_fee': resp[1]
        }

    def get_liquidity_coefficient_in_funding_payment(
        self,
        trader: str,
        base_token: str,
        funding_growth_global: FundingGrowth
    ):
        '''
        Returns liquidity coefficient in funding payment
        Arguments:
        trader - wallet address of trader
        base_token - contract address of base token
        funding_growth_global - FundingGrowth object
        '''
        return self.order_book.functions.getLiquidityCoefficientInFundingPayment(
            trader,
            base_token,
            funding_growth_global.to_dict()
        ).call()

    def get_pending_fee(
        self,
        trader: str,
        base_token: str,
        lower_tick: int,
        upper_tick: int
    ):
        '''
        Returns pending fee.
        Arguments:
        trader - wallet address of trader
        base_token - contract address of base token
        lower_tick - lower tick
        upper_tick - upper tick
        '''
        return self.order_book.functions.getPendingFee(
            trader,
            base_token,
            lower_tick,
            upper_tick
        ).call()

    def get_total_order_debt(
        self,
        trader,
        base_token,
        fetch_base
    ):
        '''
        Returns total order debt.
        Arguments:
        trader - wallet address of trader
        base_token - contract address of base token
        fetch_base - fetch base
        '''
        return self.order_book.functions.getTotalOrderDebt(
            trader,
            base_token,
            fetch_base
        ).call()
