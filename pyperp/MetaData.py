"""Contain the MetaData class."""

import requests
import json


class MetaData:
    """Fetch metadata json file from officially hosted URL and retieve contract addresses from it."""

    def __init__(self, testnet: bool):
        """
        Arguments:
        tesnet: True if testnet metadata is used. Otherwise, False.
        """
        if testnet:
            self._store = "https://metadata.perp.exchange/staging.json"
        else:
            self._store = "https://metadata.perp.exchange/production.json"
        self.fetchMeta()

    @property
    def metadataStore(self):
        """Getter for metadata URL."""
        return self._store

    @metadataStore.setter
    def metadataStore(self, s):
        """Get metadata URL."""
        self._store = s
        self.fetchMeta()

    def fetchMeta(self):
        """Download metadata json file."""
        self.meta = requests.get(self._store).json()

    def getL1ContractAddress(self, name):
        """
        Retrieve Layer 1 contract address.

        Arguments:
        name -- name of the layer 1 contract
        """
        return self.meta["layers"]["layer1"]["contracts"][name]["address"]

    def getL2ContractAddress(self, name):
        """
        Retrieve Layer 2 contract address.

        Arguments:
        name -- name of the layer 2 contract.
        """
        return self.meta["layers"]["layer2"]["contracts"][name]["address"]

    def getL1ExtContractAddress(self, name):
        """
        Retrieve Layer 1 external contract address.

        Arguments:
        name -- name of the layer 1 external contract
        """
        return self.meta["layers"]["layer1"]["externalContracts"][name]

    def getL2ExtContractAddress(self, name):
        """
        Retrieve Layer 2 external contract address.

        Arguments:
        name -- name of the layer 2 external contract
        """
        return self.meta["layers"]["layer2"]["externalContracts"][name]
