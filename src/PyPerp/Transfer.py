import constants
import json

def depositToxDai(self, account, provider, amount):
    layer1Usdc = None #todo: create contract object
    layer1Bridge = None  #todo: create contract object
    approveTx = layer1Usdc.functions.approve(layer1Bridge.address, constants.MaxUInt256).call()
    #approveTx.wait()
    transferTx = layer1Bridge.erc20Transfer(layer1Usdc.address, account.layer1WalletAddress,json.dumps(f"{{d:{amount}}}"))
    #receipt = transferTx.wait()

def withdrawToEthereum(self, account, provider, amount):
    layer2Usdc = None #todo: create contract object
    layer2Bridge = None #todo: create contract object
    approveTx = layer2Usdc.functions.approve(layer2Bridge.address, constants.MaxUInt256).call()
    #approveTx.wait()
    transferTx = layer2Brige.erc20Transfer(layer2Usdc.address,account.layer2WalletAddres,json.dumps(f"{{d:{amount}}}"))
    #receipt = transferTx.wait()

def confirmTransferToLayer1(self, ):
    pass 

def confirmTransferToLayer2(self):
    pass 