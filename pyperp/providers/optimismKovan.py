from pyperp.provider import ApiProvider

class OptimismKovanProvider(ApiProvider):
    
    def __init__(
        self, 
        endpoint: str    
    ):
        super().__init__(endpoint)
        self.abi_dir = "optimismKovan"
