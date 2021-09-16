import constants
import json
import MetaData from MetaData

#TO-DO:
#1.) implement all the functions
#2.) look for all the ways to import a wallet
#3.) create a seperate abstraction for wallet if necessary

class Account:
    def __init__(self,l1provider,l2provider,l1wallet,l2wallet):
        #todo : validate l1wallet
        self._layer1wallet = l1wallet
        #todo : validate l2wallet
        self._layer2wallet = l2wallet

    @property
    def layer1wallet(self):
        return self._layer1wallet

    @layer1wallet.setter
    def layer1wallet(self, w):
        #todo : validate argument
        self._layer1wallet = w

    @property
    def layer2wallet(self):
        return self._layer2wallet

    @layer2wallet.setter
    def layer2wallet(self, w):
        #todo : validate argument
        self._layer2wallet = w

    def depositToxDai(self, account, provider, amount):
        #todo: checkl1 balance
        #todo: do for all available layer1 tokens

        meta = MetaData(provider.testnet)
        with open("abi/TetherToken.json") as f:
            TetherTokenAbi = json.load(f)
        with open("abi/RootBridge.json") as f:
            RootBridgeAbi = json.load(f)
        UsdcAddr = meta.getL1ExtContractAddress("usdc")
        layer1BridgeAddr = meta.getL1ContractAddress("RootBridge")
        layer1Usdc = provider.l1.eth.contract(address=UsdcAddr, abi=TetherTokenAbi)
        layer1Bridge = provider.l1.eth.contract(address=layer1BridgeAddr, abi=RootBridgeAbi)
        approveTxHash = layer1Usdc.functions.approve(layer1Bridge.address, constants.MaxUInt256).transact()
        provider.l1.eth.wait_for_transaction_receipt(approveTxHash)
        transferTxHash = layer1Bridge.functions.erc20Transfer(layer1Usdc.address, self._layer1wallet.address ,json.dumps(f"{{d:{amount}}}")).transact()
        receipt = provider.l1.eth.wait_for_transaction_receipt(transferTxHash)
    
    def withdrawToEthereum(self, account, provider, amount):
        #todo: checkl2balance
        #todo: do for all available layer2 tokens
        meta = MetaData(provider.testnet)
        with open("abi/TetherToken.json") as f:
            TetherTokenAbi = json.load(f)
        with open("abi/ClientBridge.json") as f:
            ClientBridgeAbi = json.load(f)
        UsdcAddr = meta.getL2ExtContractAddress("usdc")
        layer2BridgeAddr = meta.getL2ContractAdderss("ClientBridge")
        layer2Usdc = provider.l2.eth.contract(address=UsdcAddr, abi=TetherTokenAbi)
        layer2Bridge = provider.l2.eth.contract(address=layer2BridgeAddr, abi=ClientBridgeAbi)
        approveTxHash = layer2Usdc.functions.approve(layer2Bridge.address, constants.MaxUInt256).transact()
        provider.l1.wait_for_transaction_receipt(approveTxHash)
        transferTxHash = layer2Brige.functions.erc20Transfer(layer2Usdc.address,self._layer2wallet.address,json.dumps(f"{{d:{amount}}}")).transact()
        receipt = provider.l2.eth.wait_for_transaction_receipt(transferTxHash)
    