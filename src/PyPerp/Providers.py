from web3 import Web3, middleware
from web3.gas_strategies.time_based import medium_gas_price_strategy

class Providers:
    def __init__(self, l1, l2, testnet:bool):
        self.testnet = testnet
        self.l1 = l1 
        self.l2 = l2
        #self.l1.eth.set_gas_price_strategy(medium_gas_price_strategy)
        #self.l2.eth.set_gas_price_strategy(medium_gas_price_strategy)
        #self.l1.middleware_onion.add(middleware.time_based_cache_middleware)
        #self.l1.middleware_onion.add(middleware.latest_block_based_cache_middleware)
        #self.l1.middleware_onion.add(middleware.simple_cache_middleware)
        #self.l2.middleware_onion.add(middleware.time_based_cache_middleware)
        #self.l2.middleware_onion.add(middleware.latest_block_based_cache_middleware)
        #self.l2.middleware_onion.add(middleware.simple_cache_middleware)