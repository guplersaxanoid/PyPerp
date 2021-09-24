import requests
import json

class MetaData:
    def __init__(self, testnet: bool):
        if testnet:
            self._store =  "https://metadata.perp.exchange/staging.json"
        else:
            self._store = "https://metadata.perp.exchange/production.json"
        self.fetchMeta()

    @property
    def metadataStore(self):
        return self._store

    @metadataStore.setter
    def metadataStore(self, s):
        self._store = s
        self.fetchMeta()
    
    def fetchMeta(self):
        self.meta = requests.get(self._store).json()

    def getL1ContractAddress(self, name):
        return self.meta["layers"]["layer1"]["contracts"][name]["address"]

    def getL2ContractAddress(self, name):
        return self.meta["layers"]["layer2"]["contracts"][name]["address"]

    def getL1ExtContractAddress(self, name):
        return self.meta["layers"]["layer1"]["externalContracts"][name]

    def getL2ExtContractAddress(self, name):
        return self.meta["layers"]["layer2"]["externalContracts"][name]