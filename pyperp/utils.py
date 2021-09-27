import json
from pyperp import MetaData, constants
import datetime 
import pkgutil 

def confirmTransferToLayer2(receipt, provider):
    meta = MetaData(provider.testnet)
    layer2AmbAbi = json.loads(pkgutil.get_data(__name__,"abi/AmbL2.json"))
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
    layer1AmbAbi = json.loads(pkgutil.get_data(__name__,"abi/AmbL1.json"))
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
            Amms = constants.AvailableAmms["testnet"]
    else:
        Amms = constants.AvailableAmms["mainnet"]

    if amm not in Amms:
        raise ValueError(f"Unknown pair: {pair}")

    meta = MetaData.MetaData(provider.testnet)
    AmmAddr = meta.getL2ContractAddress(amm)
    AmmAbi = json.loads(pkgutil.get_data(__name__,"abi/Amm.json"))

    Amm = provider.l2.eth.contract(address=AmmAddr, abi=AmmAbi)
    return Amm

def estimateLiquidationPrice(position, amm, clearingHouse):
    spotPrice = amm.functions.getSpotPricer.call().d
    realCloseQuoteAmount = amm.functions.getOutputPrice(
        0 if position.size.d > 0 else 1,
        json.dumps(f"d: {abs(position.size.d)}")
    ).call().d
    maintanenceMarginRatio = clearingHouse.functions.maintanenceMarginRatio().call()
    openNotional = position.openNotional.d
    positionSizeAbs = abs(position.size.d)
    margin = position.margin.d
    entryPrice = openNotional/positionSizeAbs
    reverseLeverage = margin/openNotional
    spotCloseQuoteAmount = spotPrice*positionSizeAbs
    closePosPriceSlippage = (realCloseQuoteAmount - spotCloseQuoteAmount)/spotCloseQuoteAmount
    if position.size.d > 0:
        liquidationPrice =  entryPrice*(1-reverseLeverage-closePosPriceSlippage+maintanenceMarginRatio)
    else:
        liquidationPrice = entryPrice*(1+reverseLeverage-closePosPriceSlippage-maintanenceMarginRatio)
    return liquidationPrice

def parseUnits(amount, decimal=constants.DEFAULT_DECIMALS):
    return amount*(10**decimal)

def formatUnits(amount, decimal=constants.DEFAULT_DECIMALS):
    return amount/(10**decimal)

def estimatedFundingRate(amm):
    durationFromSharp = DateTime.local().minute * 60
    twapPrice = amm.functions.getTwapPrice(durationFromSharp).call()
    underlyingTwapPrice = amm.functions.getUnderlyingTwapPrice(durationFromSharp).call()
    fundingPeriod = amm.functions.fundingPeriod().call()
    
    oneDayInSec = 60*60*24
    marketTwapPrice = formatUnits(twapPrice[0])
    indexTwapPrice = formatUnits(underlyingTwapPrice[0])
    premium = marketTwapPrice - indexTwapPrice
    premiumFraction = premium*fundingPeriod/oneDayInSec
    return parseUnits(premiumFraction/indexTwapPrice)
