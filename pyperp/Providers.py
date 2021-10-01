"""Contain the Providers class."""

from web3 import Web3, middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy


class Providers:
    """Pack layer 1 and layer 2 providers in a single object."""

    def __init__(self, l1, l2, testnet: bool):
        """
        Arguments:
        l1 -- Layer 1 provider. Can be HTTP or IPC provider
        l2 -- Layer 2 provider. Can be HTTP or IPC provider
        testnet -- True if testnet is being used. False Otherwise.
        """
        self.testnet = testnet
        self.l1 = l1
        self.l2 = l2
        # self.l1.eth.set_gas_price_strategy(medium_gas_price_strategy)
        # self.l2.eth.set_gas_price_strategy(medium_gas_price_strategy)
        # self.l1.middleware_onion.add(middleware.time_based_cache_middleware)
        # self.l1.middleware_onion.add(middleware.latest_block_based_cache_middleware)
        # self.l1.middleware_onion.add(middleware.simple_cache_middleware)
        # self.l2.middleware_onion.add(middleware.time_based_cache_middleware)
        # self.l2.middleware_onion.add(middleware.latest_block_based_cache_middleware)
        # self.l2.middleware_onion.add(middleware.simple_cache_middleware)
