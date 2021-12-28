from pyperp.providers import ApiProvider
from pyperp.contracts.types import (
    MarketInfo
)
import logging


class MarketRegistry:
    def __init__(
        self,
        provider: ApiProvider
    ):
        self._provider = provider
        self.logger = logging.logger("MarketRegistry")

        logger.info("Loading MarketRegistry Contract")
        _market_registry_meta = self._provider.load_meta(
            "MarketRegistry"
        )
        _market_registry = self._provider.api.eth.contract(
            address=_market_registry_meta["address"],
            abi=_market_registry_meta["abi"]
        )
        logger.info("MarketRegistry Contract Loaded")

    def get_quote_token(self):
        return self._market_registry.functions.getQuoteToken().call()

    def get_uniswap_v3_factory(self):
        return self._market_registry.functins.getUniswapV3Factory().call()

    def get_max_orders_per_market(self):
        return self._market_registry.functions.getMarketOrdersPerMarket(
        ).call()

    def get_pool(
        self,
        base_token: str
    ):
        return self._market_registry.functions.getPool(
            base_token
        ).call()

    def get_fee_ratio(
        self,
        base_token: str
    ):
        return self._market_registry.functions.getFeeRatio(
            base_token
        ).call()

    def get_insurance_fund_fee_ratio(
        self,
        base_token: str
    ):
        return self._market_registry.functions.getInsuraceFundFeeRatio(
            base_token
        ).call()

    def get_market_info(
        self,
        base_token: str
    ):
        resp = self._market_registry.functions.getMarketInfo(
            base_token
        ).call()
        return MarketInfo.from_dict(resp)
