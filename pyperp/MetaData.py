"""Contain the MetaData class."""

import requests


class MetaData:
    """Work with the official metadata files."""

    def __init__(self, testnet: bool):
        """
        Arguments:
        tesnet: True if testnet metadata is used. Otherwise, False.
        """
        if testnet:
            self._store = "https://metadata.perp.exchange/staging.json"
        else:
            self._store = "https://metadata.perp.exchange/production.json"
        self.fetch_meta()

    @property
    def metadata_store(self):
        """Getter for metadata URL."""
        return self._store

    @metadataStore.setter
    def metadata_store(self, s):
        """Get metadata URL."""
        self._store = s
        self.fetch_meta()

    def fetch_meta(self):
        """Download metadata json file."""
        self.meta = requests.get(self._store).json()

    def get_l1_contract_address(self, name):
        """
        Retrieve Layer 1 contract address.

        Arguments:
        name -- name of the layer 1 contract
        """
        return self.meta["layers"]["layer1"]["contracts"][name]["address"]

    def get_l2_contract_address(self, name):
        """
        Retrieve Layer 2 contract address.

        Arguments:
        name -- name of the layer 2 contract.
        """
        return self.meta["layers"]["layer2"]["contracts"][name]["address"]

    def get_l1_ext_contract_address(self, name):
        """
        Retrieve Layer 1 external contract address.

        Arguments:
        name -- name of the layer 1 external contract
        """
        return self.meta["layers"]["layer1"]["externalContracts"][name]

    def get_l2_ext_contract_address(self, name):
        """
        Retrieve Layer 2 external contract address.

        Arguments:
        name -- name of the layer 2 external contract
        """
        return self.meta["layers"]["layer2"]["externalContracts"][name]
