'''ApiProvider class'''

from web3 import Web3
import pkgutil
from eth_account import Account
import json


class ApiProvider:

    abi_dir: str

    def __init__(
        self,
        endpoint: str,
        account: Account
    ):
        '''
        Initialize endpoint and account.
        Argument:
        endpoint - Endpoint URL of RPC provider'
        account - Account object to manage keypair
        '''
        self._api = self._wrap_api(endpoint)
        self._account = account

    def _wrap_api(self, endpoint):
        '''
        Generate HTTPProvider or WebsocketProvider object.
        Argument:
        endpoint - Endpoint URL
        '''
        protocol = endpoint.split(':')[0]
        if protocol == 'https' or protocol == 'http':
            provider = Web3.HTTPProvider(endpoint)
        elif protocol == 'ws' or protocol == 'wss':
            provider = Web3.WebsocketProvider(endpoint)
        else:
            raise ValueError(
                f'Unknown protocol in the given endpoint: "{endpoint}"')
        return Web3(provider)

    @property
    def api(self):
        return self._api

    @property
    def account(self):
        return self._account

    def load_meta(self, contract_name):
        '''
        Returns metadata and ABI of a contract.
        Argument:
        contract_name - name of the contract
        '''
        try:
            return json.loads(
                pkgutil.get_data(
                    __name__, f"../abi/{self.abi_dir}/{contract_name}.json")
            )
        except BaseException:
            print(
                f"contract not found: abi/{self.abi_dir}/{contract_name}.json")
            return
