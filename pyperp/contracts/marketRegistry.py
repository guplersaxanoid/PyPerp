'''MarketRegistry Class.'''

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
        '''
        Initialize provider.
        Arguments:
        provider - an object of classes derived from ApiProvider
        '''
        self._provider = provider
        self.logger = logging.getLogger("MarketRegistry")

        self.logger.info("Loading MarketRegistry Contract")
        market_registry_meta = self._provider.load_meta(
            "MarketRegistry"
        )
        self.market_registry = self._provider.api.eth.contract(
            address=market_registry_meta["address"],
            abi=market_registry_meta["abi"]
        )
        self.logger.info("MarketRegistry Contract Loaded")

    def get_quote_token(self):
        '''
        Returns address of quote token contract.
        '''
        return self.market_registry.functions.getQuoteToken().call()

    def get_uniswap_v3_factory(self):
        '''
        Returns address of UniswapV3Factory contract.
        '''
        return self.market_registry.functions.getUniswapV3Factory().call()

    def get_max_orders_per_market(self):
        '''
        Returns maximum orders per market.
        '''
        return self.market_registry.functions.getMaxOrdersPerMarket(
        ).call()

    def get_pool(
        self,
        base_token: str
    ):
        '''
        Returns pool address of a base token.
        Arguments:
        base_token - contract address of base token
        '''
        return self.market_registry.functions.getPool(
            base_token
        ).call()

    def get_fee_ratio(
        self,
        base_token: str
    ):
        '''
        Returns fee ratio for a base token.
        Argments:
        base_token - contract address of base token
        '''
        return self.market_registry.functions.getFeeRatio(
            base_token
        ).call()

    def get_insurance_fund_fee_ratio(
        self,
        base_token: str
    ):
        '''
        Returns insurance fund fee ratio for a base token.
        Arguments:
        base_token - contract address of base token
        '''
        return self.market_registry.functions.getInsuranceFundFeeRatio(
            base_token
        ).call()

    def get_market_info(
        self,
        base_token: str
    ):
        '''
        Returns Market Info for a base token.
        Arguments:
        base_token - contract address of base token
        '''
        resp = self.market_registry.functions.getMarketInfo(
            base_token
        ).call()
        return MarketInfo(*resp)
