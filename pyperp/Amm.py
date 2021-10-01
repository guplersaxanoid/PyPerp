"""Contains amm related methods and data."""

import json
from pyperp import MetaData
from pyperp.utils import estimatedFundingRate, formatUnits
import pkgutil


def getAmmInfo(provider, pair=None):
    """
    Return Amm information for all amms or a particular amm.

    Arguments:
    providers -- a Providers object
    pair -- A string value representing a pair. Choose from AvailableAmms in constants.py
    """
    insuranceFundAbi = json.loads(pkgutil.get_data(__name__, "abi/InsuranceFund.json"))
    clearingHouseAbi = json.loads(pkgutil.get_data(__name__, "abi/ClearingHouse.json"))
    ammAbi = json.loads(pkgutil.get_data(__name__, "abi/Amm.json"))

    meta = MetaData(provider.testnet)
    insuranceFundAddr = meta.getL2ContractAddress("InsuranceFund")
    clearingHouseAddr = meta.getL2ContractAddress("ClearingHouse")

    insuranceFund = provider.l2.eth.contract(address=insuranceFundAddr, abi=insuranceFundAbi)
    clearingHouse = provider.l2.eth.contract(address=clearingHouseAddr, abi=clearingHouseAbi)

    data = []

    ammAddressList = insuranceFund.functions.getAllAmms().call()

    for addr in ammAddressList:
        amm = provider.l2.eth.contract(address=addr, abi=ammAbi)
        priceFeedKey = amm.functions.priceFeedKey().call().decode("utf-8", "ignore")
        if pair is not None and pair != priceFeedKey:
            continue

        openInterestNotionalCap = amm.functions.getOpenInterestNotionalCap().call()
        openInterestNotional = clearingHouse.functions.openInterestNotionalMap(addr).call()
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
            "pair": f"{priceFeedKey}/USDC",
            "Proxy Address": addr,
            "Index Price": f"{formatUnits(indexPrice[0])} USDC",
            "Market Price": f"{formatUnits(marketPrice[0])} USDC",
            "OpenInterestNotionalCap": f"{formatUnits(openInterestNotionalCap[0])} USDC",
            "OpenInterestNotional": f"{formatUnits(openInterestNotional)} USDC",
            "MaxHoldingBaseAsset": f"{formatUnits(maxHoldingBaseAsset[0])} USDC",
            "QuoteAssetReserve": f"{formatUnits(quoteAssetReserve[0])} USDC",
            "BaseAssetReserve": f"{formatUnits(baseAssetReserve[0])} {priceFeedKey}USDC",
            "PriceFeed": priceFeedName,
            "est.funding rate": f"{estFundingRate} %"
        })

    return data
