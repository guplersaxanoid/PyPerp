import constants
import json
import MetaData from MetaData

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
    transferTxHash = layer1Bridge.functions.erc20Transfer(layer1Usdc.address, account.layer1WalletAddress,json.dumps(f"{{d:{amount}}}")).transact()
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
    transferTxHash = layer2Brige.functions.erc20Transfer(layer2Usdc.address,account.layer2WalletAddres,json.dumps(f"{{d:{amount}}}")).transact()
    receipt = provider.l2.eth.wait_for_transaction_receipt(transferTxHash)

def confirmTransferToLayer2(self, receipt):
    layer2Amb = None 
    methodId = "0x482515ce"
    for r in receipt:
        log = r["logs"]
        if log.topics[0][:10]==methodId:
            break
    fromMsgId = log.topics[1]
    confirmationFilter = layer2Amb.events.AffirmationCompleted.createFilter(fromBlock="latest",argument_filters={'toMsgId':fromMsgId})  
    while True:
        for c in confirmationFilter:
            print("Transfer completed")
            return 

def confirmTransferToLayer1(self, reciept):
    layer1Amb = None
    methodId = "0x520d2afd"
    for r in receipt:
        log = r["logs"]
        if log.topics[0][:10]==methodId:
            break
    fromMsgId = log.topics[1]
    confirmationFilter = layer1Amb.events.RelayedMessage.createFilter(fromBlock="latest",argument_filters={'toMsgId':fromMsgId})  
    while True:
        for c in confirmationFilter:
            print("Transfer completed")
            return 