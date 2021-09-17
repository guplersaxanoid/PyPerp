import constants
import json
import MetaData from MetaData
from constants import Side
from decimal import Decimal 
from utils import *

#TO-DO:
#1.) implement all the functions
#2.) look for all the ways to import a wallet
#3.) create a seperate abstraction for wallet if necessary

class Trader:
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

    def depositToxDai(self, provider, amount):
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
    
    def withdrawToEthereum(self, provider, amount):
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
    
    def openPosition(self, provider, amm, side, quoteAssetAmount: Decimal, leverage: Decimal, baseAssetAmountLimit: Decimal):
        
        #todo: handle error
        if side!=0 and side!=1:
            return

        #todo: handle error
        if quoteAssetAmount <= 0:
            return 

        #todo: handle error
        if leverage <= 0 or leverage > 10:
            return

        meta = MetaData(provider.testnet)
        Amm = getAmm(amm,provider)
        if Amm == None:
            return 

        clearingHouseAddr = meta.getL2ContractAddress("ClearingHouse")
        with open("abi/ClearingHouse.json") as f:
            clearingHouseAbi = json.load(f)
        clearingHouse = provider.l2.eth.contract(address=clearingHouseAddr, abi=clearingHouseAbi)
           
        tx = clearingHouse.functions.openPosition(Amm.address, side, quoteAssetAmount, leverage, baseAssetAmountLimit).trasact({
            'from':self._layer2wallet.address,
        })
        receipt = provider.l2.eth.wait_for_trasaction_receipt(tx)

    def closePosition(self, provider, amm, quoteAssetAmountLimit: Decimal):

        meta = MetaData(provider.testnet)
        
        Amm = getAmm(amm,provider)
        if Amm == None:
            return 
        
        clearingHouseAddr = meta.getL2ContractAddress("ClearingHouse")
        with open("abi/ClearingHouse.json") as f:
            clearingHouseAbi = json.load(f)
        clearingHouse = provider.l2.eth.contract(address=clearingHouseAddr, abi=clearingHouseAbi)

        tx  = clearingHouse.functions.closePosition(Amm.address, quoteAssetAmountLimit).transact({
            'from':self._layer2wallet.address
        })
        receipt = provider.l2.eth.wait_for_transaction_receipt(tx)

    def getPersonalPositionWithFundingPayment(self, provider, amm, trader=None):
        #note: return for all open positions
        Amm = getAmm(amm,provider)
        if Amm == None:
            return 
        if trader is None:
            trader = self._layer2wallet.address

        meta = MetaData(provider.testnet)
        clearingHouseViewerAddr = meta.getL2ContractAddress("ClearingHouseViewer")
        with open("abi/ClearingHouseViewer.json") as f:
            clearingHouseViewerAbi = json.load(f)
        clearingHouseViewer = provider.l2.eth.contract(address=clearingHouseViewerAddr, abi=clearingHouseViewerAbi)

        return clearingHouseViewer.functions.getPersonalPositionWithFundingPayment(Amm.address,trader.address)        

    def queryUnrealizedPnl(self):
        #note: return for all open positions
        pass 

    def getEntryPrice(self):
        pass 

    def estimateLiquidationPrice(self):
        pass 