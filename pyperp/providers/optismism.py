from pyperp.provider import ApiProvider

class OptimismProvider(ApiProvider):
    
    def __init__(
        self, 
        endpoint: str    
    ):
        super().__init__(endpoint)