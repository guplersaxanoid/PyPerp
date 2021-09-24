import json
import MetaData
from utils import estimatedFundingRate, formatUnits

def getAmmInfo(provider,pair=None):
    with open("abi/InsuranceFund.json") as f:
        insuranceFundAbi = json.load(f)
    with open("abi/ClearingHouse.json") as f:
        clearingHouseAbi = json.load(f)
    with open("abi/Amm.json") as f:
        ammAbi = json.load(f)

    meta = MetaData.MetaData(provider.testnet)
    insuranceFundAddr = meta.getL2ContractAddress("InsuranceFund")
    clearingHouseAddr = meta.getL2ContractAddress("ClearingHouse")

    insuranceFund = provider.l2.eth.contract(address=insuranceFundAddr, abi=insuranceFundAbi)
    clearingHouse = provider.l2.eth.contract(address=clearingHouseAddr, abi=clearingHouseAbi)

    data = []

    ammAddressList = insuranceFund.functions.getAllAmms().call()

    for addr in ammAddressList:
        amm = provider.l2.eth.contract(address=addr, abi=ammAbi)
        print(ammAbi)
        priceFeedKey = amm.functions.priceFeedKey().call().decode("utf-8","ignore")
        if pair is not None and pair != priceFeedKey:
            continue
        
        openInterestNotionalCap = amm.functions.getOpenInterestNotionalCap().call()
        openInterestNotional = clearingHouse.functions.openInterestNotinalMap(addr).call()
        maxHoldingBaseAsset = amm.functions.getMaxHoldingBaseAsset().call()
        indexPrice = amm.functions.getUnderlyingPrice().call()
        marketPrice = amm.functions.getSpotPrice().call()
        reserve = amm.functions.getReserve().call()
        quoteAssetAddress = amm.functions.quoteAsset().call()
        quoteAssetReserve = reserve[0]
        baseAssetReserve = reserve[1]
        priceFeed = amm.functions.priceFeed().call()
        estFundingRate = (estimatedFundingRate(amm)/1e18) * 100
        
        if priceFeed == meta.getL2ContractAddress("L2PriceFeed"):
            priceFeedName = "L2PriceFeed"
        elif priceFeed == meta.getL2ContractAddress("ChainlinkPriceFeed"):
            priceFeedName = "ChainlinkPriceFeed"
        else:
            ValueError("PriceFeed is not L2PriceFeed or ChainlinkPriceFeed, check it immediately!! address: " + priceFeed)

        data.append({
            "pair":f"{priceFeedKey}/USDC",
            "Proxy Address": addr,
            "Index Price": f"{formatUnits(indexPrice)} USDC",
            "Market Price": f"{formatUnits(marketPrice)} USDC",
            "OpenInterestNotionalCap": f"{formatUnits(openInterestNotionalCap)} USDC",
            "OpenInterestNotional": f"{formatUnits(openInterestNotinal)} USDC",
            "MaxHoldingBaseAsset": f"{formatUnits(maxHoldingBaseAsset)} USDC",
            "QuoteAssetReserve": f"{formatUnits(quoteAssetReserve)} USDC",
            "BaseAssetReserve": f"{formatUnits(baseAssetReserve)} {priceFeedKey}USDC",
            "PriceFeed": priceFeedName,
            "est.funding rate": f"{estFundingRate} %"
        })

    return data