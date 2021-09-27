from pyperp import constants
import json
from pyperp.MetaData import MetaData
from pyperp.constants import Side
from decimal import Decimal 
from pyperp.utils import *
from eth_abi import encode_single
import pkgutil

class Trader:
    def __init__(self,provider,l1wallet,l2wallet):
        self._layer1wallet = l1wallet
        self._layer2wallet = l2wallet
        self._provider = provider
        self.meta = MetaData.MetaData(provider.testnet)

        clearingHouseAddr = self.meta.getL2ContractAddress("ClearingHouse")
        clearingHouseAbi =  json.loads(pkgutil.get_data(__name__,"abi/ClearingHouse.json"))
        self.clearingHouse = self._provider.l2.eth.contract(address=clearingHouseAddr, abi=clearingHouseAbi)

        clearingHouseViewerAddr = self.meta.getL2ContractAddress("ClearingHouseViewer")
        clearingHouseViewerAbi = json.loads(pkgutil.get_data(__name__,"abi/ClearingHouseViewer.json"))
        self.clearingHouseViewer = self._provider.l2.eth.contract(address=clearingHouseViewerAddr, abi=clearingHouseViewerAbi)


    @property
    def layer1wallet(self):
        return self._layer1wallet

    @layer1wallet.setter
    def layer1wallet(self, w):
        self._layer1wallet = w

    @property
    def layer2wallet(self):
        return self._layer2wallet

    @layer2wallet.setter
    def layer2wallet(self, w):
        self._layer2wallet = w

    def l1WalletBalance(self):
        return self._provider.l1.eth.getBalance(self._layer1wallet.address)

    def l2WalletBalance(self):
        return self._provider.l2.eth.getBalance(self._layer2wallet.address)

    def approveL1BridgetoUseUSDC(self):
        
        TetherTokenAbi = json.loads(pkgutil.get_data(__name__,"abi/TetherToken.json"))
        UsdcAddr = self.meta.getL1ExtContractAddress("usdc")
        layer1BridgeAddr = self.meta.getL1ContractAddress("RootBridge")
        layer1Usdc = self._provider.l1.eth.contract(address=UsdcAddr, abi=TetherTokenAbi)
        nonce = self._provider.l1.eth.get_transaction_count(self._layer1wallet.address)
        approveTx = layer1Usdc.functions.approve(layer1BridgeAddr, constants.MaxUInt256).buildTransaction({
            'nonce':nonce,
            'gas': 1000000,
            'gasPrice': self._provider.l1.eth.gasPrice,
        })
        signed_tx = self._provider.l1.eth.account.sign_transaction(approveTx, private_key=self._layer1wallet.key)
        
        approveTxHash = self._provider.l1.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = self._provider.l1.eth.wait_for_transaction_receipt(approveTxHash)
        return receipt

    def depositUsdcToxDai(self, amount):
        TetherTokenAbi = json.loads(pkgutil.get_data(__name__,"abi/TetherToken.json"))
        RootBridgeAbi = json.loads(pkgutil.get_data(__name__,"abi/RootBridge.json"))
        UsdcAddr = self.meta.getL1ExtContractAddress("usdc")
        layer1BridgeAddr = self.meta.getL1ContractAddress("RootBridge")
        layer1Usdc = self._provider.l1.eth.contract(address=UsdcAddr, abi=TetherTokenAbi)
        layer1Bridge = self._provider.l1.eth.contract(address=layer1BridgeAddr, abi=RootBridgeAbi)
        nonce = self._provider.l1.eth.get_transaction_count(self._layer1wallet.address)
        #gasEstimate = layer1Bridge.functions.erc20Transfer(UsdcAddr, self._layer1wallet.address, {'d':parseUnits(amount,18)}).estimateGas() 
        transferTx = layer1Bridge.functions.erc20Transfer(UsdcAddr, self._layer1wallet.address, {'d':parseUnits(amount,18)}).buildTransaction({
            'nonce':nonce,
            'gas': 1000000,
            'gasPrice': self._provider.l1.eth.gasPrice,
        })
        signed_tx = self._provider.l1.eth.account.sign_transaction(transferTx, private_key=self._layer1wallet.key)
        transferTxHash = self._provider.l1.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = self._provider.l1.eth.wait_for_transaction_receipt(transferTxHash)
        return receipt
        
    def approveL2BridgeToUseUSDC(self):
        TetherTokenAbi = json.loads(pkgutil.get_data(__name__,"abi/TetherToken.json"))
        UsdcAddr = self.meta.getL2ExtContractAddress("usdc")
        layer2BridgeAddr = self.meta.getL2ContractAddress("ClientBridge")
        layer2Usdc = self._provider.l2.eth.contract(address=UsdcAddr, abi=TetherTokenAbi)
        nonce = self._provider.l2.eth.get_transaction_count(self._layer2wallet.address)
        #gasEstimate = layer2Usdc.functions.approve(layer2BridgeAddr, constants.MaxUInt256).estimateGas()
        approveTx = layer2Usdc.functions.approve(layer2BridgeAddr, constants.MaxUInt256).buildTransaction({
            'nonce':nonce,
            'gas': 1000000,
            'gasPrice': self._provider.l2.eth.gasPrice,
        })
        signed_tx = self._provider.l2.eth.account.sign_transaction(approveTx, private_key=self._layer2wallet.key)
        
        approveTxHash = self._provider.l2.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = self._provider.l2.eth.wait_for_transaction_receipt(approveTxHash)
        return receipt
    
    def withdrawUsdcToEthereum(self, amount):
        
        TetherTokenAbi = json.loads(pkgutil.get_data(__name__,"abi/TetherToken.json"))
        ClientBridgeAbi = json.loads(pkgutil.get_data(__name__,"abi/ClientBridge.json"))
        UsdcAddr = self.meta.getL2ExtContractAddress("usdc")
        layer2BridgeAddr = self.meta.getL2ContractAddress("ClientBridge")
        layer2Usdc = self._provider.l2.eth.contract(address=UsdcAddr, abi=TetherTokenAbi)
        layer2Bridge = self._provider.l2.eth.contract(address=layer2BridgeAddr, abi=ClientBridgeAbi)
        nonce = self._provider.l2.eth.get_transaction_count(self._layer2wallet.address)
        #gasEstimate = layer2Bridge.functions.erc20Transfer(layer2Usdc.address, self._layer2wallet.address,{'d':parseUnits(amount,constants.DEFAULT_DECIMALS)}).esimateGas()
        transferTx = layer2Bridge.functions.erc20Transfer(layer2Usdc.address, self._layer2wallet.address,{'d':parseUnits(amount,constants.DEFAULT_DECIMALS)}).buildTransaction({
            'nonce':nonce,
            'gas': 1000000,
            'gasPrice':self._provider.l2.eth.gasPrice
        })
        signed_tx = self._provider.l2.eth.account.sign_transaction(transferTx, private_key=self._layer2wallet.key)
        transferTxHash = self._provider.l2.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = self._provider.l2.eth.wait_for_transaction_receipt(transferTxHash)
        return receipt

    def approveClearingHouseToUseUSDC(self):
        
        TetherTokenAbi = json.loads(pkgutil.get_data(__name__,"abi/TetherToken.json"))
        UsdcAddr = self.meta.getL2ExtContractAddress("usdc")
        ClearingHouseAddr = self.meta.getL2ContractAddress("ClearingHouse")
        layer2Usdc = self._provider.l2.eth.contract(address=UsdcAddr, abi=TetherTokenAbi)
        nonce = self._provider.l2.eth.get_transaction_count(self._layer2wallet.address)
        #gasEstimate = layer2Usdc.functions.approve(ClearingHouseAddr, constants.MaxUInt256).estimateGas()
        tx = layer2Usdc.functions.approve(ClearingHouseAddr, constants.MaxUInt256).buildTransaction({
            'nonce':nonce,
            'gas': 1000000,
            'gasPrice':self._provider.l2.eth.gasPrice
        })
        signed_tx = self._provider.l2.eth.account.sign_transaction(tx,private_key=self._layer2wallet.key)
        txHash = self._provider.l2.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = self._provider.l2.eth.wait_for_transaction_receipt(txHash)
        return receipt
    
    def openPosition(self, pair, side, quoteAssetAmount, leverage, baseAssetAmountLimit):
        
        if side!=0 and side!=1:
            raise ValueError("side must be either 0 or 1")

        if quoteAssetAmount <= 0:
            raise ValueError("quoteAssetAmount must be greater than 0")

        if leverage <= 0 or leverage > 10:
            raise ValueError("leverage must be in the range (0,10]")

        Amm = getAmm(pair,self._provider)

        nonce = self._provider.l2.eth.get_transaction_count(self._layer2wallet.address)
        #gasEstimate = self.clearingHouse.functions.openPosition(Amm.address, side, {'d': parseUnits(quoteAssetAmount,18)}, {'d':parseUnits(leverage,18)}, {'d':parseUnits(baseAssetAmountLimit,18)}).estimateGas() 
        tx = self.clearingHouse.functions.openPosition(Amm.address, side, {'d': parseUnits(quoteAssetAmount,18)}, {'d':parseUnits(leverage,18)}, {'d':parseUnits(baseAssetAmountLimit,18)}).buildTransaction({
            'nonce':nonce,
            'gas': 1000000,
            'gasPrice':self._provider.l2.eth.gasPrice
        })
        signed_tx = self._provider.l2.eth.account.sign_transaction(tx,private_key=self._layer2wallet.key)
        txHash = self._provider.l2.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = self._provider.l2.eth.wait_for_transaction_receipt(txHash)
        return receipt

    def closePosition(self, pair, quoteAssetAmountLimit):
        
        Amm = getAmm(pair,self._provider)
        
        nonce = self._provider.l2.eth.get_transaction_count(self._layer2wallet.address)
        #gasEstimate = self.clearingHouse.functions.closePosition(Amm.address, {"d":parseUnits(quoteAssetAmountLimit,constants.DEFAULT_DECIMALS)}).estimateGas()
        tx  = self.clearingHouse.functions.closePosition(Amm.address, {"d":parseUnits(quoteAssetAmountLimit,constants.DEFAULT_DECIMALS)}).buildTransaction({
            'nonce':nonce,
            'gas': 300000,
            'gasPrice':self._provider.l2.eth.gasPrice
        })
        signed_tx = self._provider.l2.eth.account.sign_transaction(tx,private_key=self._layer2wallet.key)
        txHash = self._provider.l2.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = self._provider.l2.eth.wait_for_transaction_receipt(txHash)
        return receipt

    def getPersonalPositionWithFundingPayment(self, pair, trader=None):
        #note: return for all open positions
        Amm = getAmm(pair,self._provider)

        if trader is None:
            trader = self._layer2wallet.address

        position = self.clearingHouseViewer.functions.getPersonalPositionWithFundingPayment(Amm.address,trader).call()        
        return {
            'size': position[0][0],
            'margin': position[1][0],
            'openNotional': position[2][0],
            'lastUpdatedCumulativePremiumFraction': position[3][0],
            'liquidityHistoryIndex': position[4],
            'blockNumber': position[5]
        }

    def getUnrealizedPnl(self, pair, pnlCalcOption, trader = None):
        #note: return for all open positions
        Amm = getAmm(pair,self._provider)
        if trader is None:
            trader = self._layer2wallet.address

        return self.clearingHouseViewer.functions.getUnrealizedPnl(Amm.address,trader,pnlCalcOption.value).call()[0]

    def getEntryPrice(self, pair):

        position = self.getPersonalPositionWithFundingPayment(pair)
        openNotional = formatUnits(position["openNotional"], constants.DEFAULT_DECIMALS)
        size  = formatUnits(position["size"], constants.DEFAULT_DECIMALS)

        entryPrice = abs(openNotional/size)
        return entryPrice

    def addMargin(self, pair, margin):

        Amm = getAmm(pair,self._provider)

        nonce = self._provider.l2.eth.get_transaction_count(self._layer2wallet.address)
        #gasEstimate = self.clearingHouse.functions.addMargin(Amm.address,{'d':parseUnits(margin,18)}).estimateGas()
        tx = self.clearingHouse.functions.addMargin(Amm.address,{'d':parseUnits(margin,18)}).buildTransaction({
            'nonce':nonce,
            'gas': 300000,
            'gasPrice':self._provider.l2.eth.gasPrice
        })
        signed_tx = self._provider.l2.eth.account.sign_transaction(tx,private_key=self._layer2wallet.key)
        txHash = self._provider.l2.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = self._provider.l2.eth.wait_for_transaction_receipt(txHash)
        return receipt

    def removeMargin(self, pair, margin):

        Amm = getAmm(pair,self._provider)

        nonce = self._provider.l2.eth.get_transaction_count(self._layer2wallet.address)
        #gasEstimate = self.clearingHouse.functions.removeMargin(Amm.address,{'d':parseUnits(margin,18)}).estimateGas()
        tx = self.clearingHouse.functions.removeMargin(Amm.address,{'d':parseUnits(margin,18)}).buildTransaction({
            'nonce':nonce,
            'gas': 300000,
            'gasPrice':self._provider.l2.eth.gasPrice
        })
        signed_tx = self._provider.l2.eth.account.sign_transaction(tx,private_key=self._layer2wallet.key)
        txHash = self._provider.l2.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = self._provider.l2.eth.wait_for_transaction_receipt(txHash)
        return receipt

    def settlePosition(self, pair):

        Amm = getAmm(pair, self._provider)

        nonce = self._provider.l2.eth.get_transaction_count(self._layer2wallet.address)
        #gasEstimate = self.clearingHouse.functions.removeMargin(Amm.address).estimateGas()
        tx = self.clearingHouse.functions.settlePosition(Amm.address).buildTransaction({
            'nonce':nonce,
            'gas': 300000,
            'gasPrice':self._provider.l2.eth.gasPrice
        })
        signed_tx = self._provider.l2.eth.account.sign_transaction(tx,private_key=self._layer2wallet.key)
        txHash = self._provider.l2.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = self._provider.l2.eth.wait_for_transaction_receipt(txHash)
        return receipt

    def liquidate(self, pair):

        Amm = getAmm(pair, self._provider)
        
        nonce = self._provider.l2.eth.get_transaction_count(self._layer2wallet.address)
        #gasEstimate = self.clearingHouse.functions.removeMargin(Amm.address, self._layer2wallet.address).estimateGas()
        tx = self.clearingHouse.functions.liquidate(Amm.address, self._layer2wallet.address).buildTransaction({
            'nonce':nonce,
            'gas': 300000,
            'gasPrice':self._provider.l2.eth.gasPrice
        })
        signed_tx = self._provider.l2.eth.account.sign_transaction(tx,private_key=self._layer2wallet.key)
        txHash = self._provider.l2.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = self._provider.l2.eth.wait_for_transaction_receipt                           (txHash)
        return receipt

    
