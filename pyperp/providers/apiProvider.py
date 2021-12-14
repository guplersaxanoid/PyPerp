"""Contain the Providers class."""

from web3 import Web3

class ApiProvider:

    def __init__(
        self,
        endpoint: str
    ):
        self._api = self._wrap_api(endpoint)

    def _wrap_api(self, endpoint):
        protocol = endpoint.split(':')[0]
        if protocol == 'http':
            return Web3.HTTPProvider(endpoint)
        elif protocol == 'ws':
            return Web3.WebsocketProvider(endpoint)
        else:
            raise ValueError(f'Unknown protocol in the given endpoint: "{endpoint}"')

    @property
    def api(self):
        return self._api

    def meta