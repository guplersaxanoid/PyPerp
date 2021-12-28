from pyperp.providers import ApiProvider
import eth_account import Account
from web3 import Web3
from pyperp.contracts.types import (
    OpenOrderInfo,
    FundingGrowth
)

class OrderBook:
    def __init__(
        self,
        provider: ApiProvider,
        wallet: Account
    ):
        self._provider = provider
        self.wallet = wallet
        self.logger = logging.getLogger("OrderBook")

        logging.info("Loading OrderBook contract")
        _order_book_meta = self._provider.load_meta("OrderBook")
        self._order_book = self._provider._api.eth.contract(
            address=_order_book_meta["address"],
            abi=_order_book_meta["abi"]
        )
        logging.info("OrderBook contract loaded")

    def get_exchange(self):
        return self._order_book.functions.getExchange().call()

    def get_open_order_ids(
        self,
        trader: str,
        base_token: str,
    ):
        assert(
            Web3.isAddress(trader),
            f"Trader address {trader} must be a checksum address"
        )
        assert(
            Web3.isAddress(base_token),
            f"Base Token address {base_token} must be a checksum address"
        )

        return self._order_book.functions.getOpenOrderIds(
            trader,
            base_token
        ).call()

    def get_open_order_by_id(
        self,
        orderId: str
    ):
        #TODO: assert bytes repr of orderId
        resp = self._order_book.functions.getOpenOrderById(
            orderId
        ).call()
        return OpenOrderInfo.from_tuple(resp)

    def getOpenOrder(
        self,
        trader: str,
        base_token: str,
        lower_tick: int,
        upper_tick: int
    ):
        resp = self._order_book.functions.getOpenOrder(
            trader,
            base_token,
            lower_tick,
            upper_tick
        ).call()
        return OpenOrderInfo.from_tuple(resp)

    def has_order(
        self,
        trader: str,
        tokens: list[str]
    ):
        return self._order_book.functions.hasOrder(
            trader,
            tokens
        ).call()

    def get_total_quote_balance_and_pending_fee(
        self,
        trader: str,
        base_token: list[str]
    ):
        #TODO: return totalQuoteAmountInPool and totalPendingFee in dict
        return self._order_book.functions.getTotalQuoteBalanceAndPendingFee(
            trader,
            base_token
        ).call()

    def get_total_token_amount_in_pool_and_pending_fee(
        self,
        trader: str,
        base_token: str,
        fetch_base: bool
    ):
        return self._order_book.functions.getTotalTokenAmountInPoolAndPendingFee(
            trader,
            base_token,
            fetch_base
        ).call()

    def get_liquidity_coefficient_in_funding_payment(
        self,
        trader: str,
        base_token: str,
        funding_growth_global: FundingGrowth
    ):
        return self._order_book.functions.getLiquidityCoefficientInFundingPayment(
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
        return self._order_book.functions.getPendingFee(
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
        return self._order_book.functions.getTotalOrderDebt(
            trader,
            base_token,
            fetch_base
        ).call()
