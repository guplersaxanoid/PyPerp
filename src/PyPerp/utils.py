import json
import MetaData

def confirmTransferToLayer2(receipt, provider):
    meta = MetaData(provider.testnet)
    with open("abi/AmbL2.json") as f:
        layer2AmbAbi = json.load(f)
    layer2AmbAddr = meta.getL2ExtContractAddress("ambBrideOnXDai")
    layer2Amb =  provider.l2.eth.contract(address=layer2AmbAddr,abi=layer2AmbAbi)
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

def confirmTransferToLayer1(reciept, provider):
    meta = MetaData(provider.testnet)
    with open("abi/AmbL1.json") as f:
        layer1AmbAbi = json.load(f)
    lauer1AmbAddr = meta.getL1ExtContractAddress("ambBridgeOnEth")
    layer1Amb = provider.l1.eth.contract(address=layer1AmbAddr,abi=layer1AmbAbi)
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

def getAmm(amm, provider):
    if provider.testnet:
            Amms = constant.AvailableAmms["testnet"]
    else:
        Amms = constant.AvailableAmms["mainnet"]

    #todo: handle error
    if amm not in Amms:
        return None

    meta = MetaData(provider.testnet)
    AmmAddr = meta.getL2ContractAddress(amm)
    with open("abi/Amm.json") as f:
        AmmAbi = json.load(f)

    Amm = provider.l2.eth.contract(address=AmmAddr, abi=AmmAbi)
    return Amm