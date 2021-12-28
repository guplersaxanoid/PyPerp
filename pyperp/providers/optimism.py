from pyperp.providers import ApiProvider
from eth_account import Account
class OptimismProvider(ApiProvider):
    
    def __init__(
        self, 
        endpoint: str,
        account: Account
    ):
        super().__init__(endpoint, account)
        self.abi_dir = "optimism"
