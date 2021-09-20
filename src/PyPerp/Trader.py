import constants
import json
from MetaData import MetaData
from constants import Side
from decimal import Decimal 
from utils import *

#TO-DO:
#1.) implement all the functions
#2.) look for all the ways to import a wallet
#3.) create a seperate abstraction for wallet if necessary

class Trader:
    def __init__(self,provider,l1wallet,l2wallet):
        #todo : validate l1wallet
        self._layer1wallet = l1wallet
        #todo : validate l2wallet
        self._layer2wallet = l2wallet
        self._provider = provider

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

    def l1WalletBalance(self):
        return self._provider.l1.eth.getBalance(self._layer1wallet.address)

    def l2WalletBalance(self):
        return self._provider.l2.eth.getBalance(self._layer2wallet.address)

    def depositToxDai(self, amount):
        #todo: checkl1 balance
        #todo: do for all available layer1 tokens

        meta = MetaData(self._provider.testnet)
        with open("abi/TetherToken.json") as f:
            TetherTokenAbi = json.load(f)
        with open("abi/RootBridge.json") as f:
            RootBridgeAbi = json.load(f)
        UsdcAddr = meta.getL1ExtContractAddress("usdc")
        layer1BridgeAddr = meta.getL1ContractAddress("RootBridge")
        layer1Usdc = self._provider.l1.eth.contract(address=UsdcAddr, abi=TetherTokenAbi)
        layer1Bridge = self._provider.l1.eth.contract(address=layer1BridgeAddr, abi=RootBridgeAbi)
        approveTxHash = layer1Usdc.functions.approve(layer1Bridge.address, constants.MaxUInt256).transact()
        self._provider.l1.eth.wait_for_transaction_receipt(approveTxHash)
        transferTxHash = layer1Bridge.functions.erc20Transfer(layer1Usdc.address, self._layer1wallet.address ,json.dumps(f"{{d:{amount}}}")).transact()
        receipt = self._provider.l1.eth.wait_for_transaction_receipt(transferTxHash)
    
    def withdrawToEthereum(self, amount):
        #todo: checkl2balance
        #todo: do for all available layer2 tokens
        meta = MetaData(self._provider.testnet)
        with open("abi/TetherToken.json") as f:
            TetherTokenAbi = json.load(f)
        with open("abi/ClientBridge.json") as f:
            ClientBridgeAbi = json.load(f)
        UsdcAddr = meta.getL2ExtContractAddress("usdc")
        layer2BridgeAddr = meta.getL2ContractAdderss("ClientBridge")
        layer2Usdc = self._provider.l2.eth.contract(address=UsdcAddr, abi=TetherTokenAbi)
        layer2Bridge = self._provider.l2.eth.contract(address=layer2BridgeAddr, abi=ClientBridgeAbi)
        approveTxHash = layer2Usdc.functions.approve(layer2Bridge.address, constants.MaxUInt256).transact()
        self._provider.l1.wait_for_transaction_receipt(approveTxHash)
        transferTxHash = layer2Brige.functions.erc20Transfer(layer2Usdc.address,self._layer2wallet.address,json.dumps(f"{{d:{amount}}}")).transact()
        receipt = self._provider.l2.eth.wait_for_transaction_receipt(transferTxHash)
    
    def openPosition(self, amm, side, quoteAssetAmount: Decimal, leverage: Decimal, baseAssetAmountLimit: Decimal):
        
        #todo: handle error
        if side!=0 and side!=1:
            return

        #todo: handle error
        if quoteAssetAmount <= 0:
            return 

        #todo: handle error
        if leverage <= 0 or leverage > 10:
            return

        meta = MetaData(self._provider.testnet)
        Amm = getAmm(amm,self._provider)
        if Amm == None:
            return 

        clearingHouseAddr = meta.getL2ContractAddress("ClearingHouse")
        with open("abi/ClearingHouse.json") as f:
            clearingHouseAbi = json.load(f)
        clearingHouse = self._provider.l2.eth.contract(address=clearingHouseAddr, abi=clearingHouseAbi)
           
        tx = clearingHouse.functions.openPosition(Amm.address, side.value, quoteAssetAmount, leverage, baseAssetAmountLimit).trasact({
            'from':self._layer2wallet.address,
        })
        receipt = self._provider.l2.eth.wait_for_trasaction_receipt(tx)

    def closePosition(self, amm, quoteAssetAmountLimit: Decimal):

        meta = MetaData(self._provider.testnet)
        
        Amm = getAmm(amm,self._provider)
        if Amm == None:
            return 
        
        clearingHouseAddr = meta.getL2ContractAddress("ClearingHouse")
        with open("abi/ClearingHouse.json") as f:
            clearingHouseAbi = json.load(f)
        clearingHouse = self._provider.l2.eth.contract(address=clearingHouseAddr, abi=clearingHouseAbi)

        tx  = clearingHouse.functions.closePosition(Amm.address, quoteAssetAmountLimit).transact({
            'from':self._layer2wallet.address
        })
        receipt = self._provider.l2.eth.wait_for_transaction_receipt(tx)

    def getPersonalPositionWithFundingPayment(self, amm, trader=None):
        #note: return for all open positions
        Amm = getAmm(amm,self._provider)
        if Amm == None:
            return 
        if trader is None:
            trader = self._layer2wallet.address

        meta = MetaData(self._provider.testnet)
        clearingHouseViewerAddr = meta.getL2ContractAddress("ClearingHouseViewer")
        with open("abi/ClearingHouseViewer.json") as f:
            clearingHouseViewerAbi = json.load(f)
        clearingHouseViewer = self._provider.l2.eth.contract(address=clearingHouseViewerAddr, abi=clearingHouseViewerAbi)

        return clearingHouseViewer.functions.getPersonalPositionWithFundingPayment(Amm.address,trader.address).call        

    def getUnrealizedPnl(self, amm, pnlCalcOption, trader = None):
        #note: return for all open positions
        Amm = getAmm(amm,self._provider)
        if Amm == None:
            return 
        if trader is None:
            trader = self._layer2wallet.address

        meta = MetaData(self._provider.testnet)
        clearingHouseViewerAddr = meta.getL2ContractAddress("ClearingHouseViewer")
        with open("abi/ClearingHouseViewer.json") as f:
            clearingHouseViewerAbi = json.load(f)
        clearingHouseViewer = self._provider.l2.eth.contract(address=clearingHouseViewerAddr, abi=clearingHouseViewerAbi)

        return clearingHouseViewer.functions.getUnrealizedPnl(Amm.address,trader,pnlCalcOption.value)

    def getEntryPrice(self, amm):

        position = self.getPersonalPositionWithFundingPayment(amm)
        openNotional = Decimal(position.openNotional.d, DEFAULT_DECIMAL)
        size  = Decimal(position.size.d, DEFAULT_DECIMAL)

        entryPrice = abs(openNotional/size)
        return entryPrice

    