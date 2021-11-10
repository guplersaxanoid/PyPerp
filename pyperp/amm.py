"""Contains amm related methods and data."""

import json
from pyperp import MetaData, Providers, utils
import pkgutil
from pyperp.constants import Dir

def get_amm_info(provider, pair=None):
    """
    Return Amm information for all amms or a particular amm.

    Arguments:
    providers -- a Providers object
    pair -- A string value representing a pair.
    """
    insurance_fund_abi = json.loads(
        pkgutil.get_data(__name__, "abi/InsuranceFund.json")
    )
    clearing_house_abi = json.loads(
        pkgutil.get_data(__name__, "abi/ClearingHouse.json")
    )
    amm_abi = json.loads(pkgutil.get_data(__name__, "abi/Amm.json"))

    meta = MetaData(provider.testnet)
    insurance_fund_addr = meta.getL2ContractAddress("InsuranceFund")
    clearing_house_addr = meta.getL2ContractAddress("ClearingHouse")

    insurance_fund = provider.l2.eth.contract(
        address=insurance_fund_addr, abi=insurance_fund_abi
    )
    clearing_house = provider.l2.eth.contract(
        address=clearing_house_addr, abi=clearing_house_abi
    )

    data = []

    amm_address_list = insurance_fund.functions.getAllAmms().call()

    for addr in amm_address_list:
        amm = provider.l2.eth.contract(address=addr, abi=amm_abi)
        price_feed_key = amm.functions.priceFeedKey().call().decode(
            "utf-8", "ignore"
        )
        if pair is not None and pair != price_feed_key:
            continue

        open_interest_notional_cap = amm.functions.getOpenInterestNotionalCap(
        ).call()
        open_interest_notional = clearing_house.functions.openInterestNotionalMap(
            addr
        ).call()
        max_holding_base_asset = amm.functions.getMaxHoldingBaseAsset().call()
        index_price = amm.functions.getUnderlyingPrice().call()
        market_price = amm.functions.getSpotPrice().call()
        reserve = amm.functions.getReserve().call()
        quote_asset_reserve = reserve[0]
        base_asset_reserve = reserve[1]
        price_feed = amm.functions.priceFeed().call()
        est_funding_rate = (utils.estimated_funding_rate(amm) / 1e18) * 100

        if price_feed == meta.getL2ContractAddress("L2PriceFeed"):
            price_feed_name = "L2PriceFeed"
        elif price_feed == meta.getL2ContractAddress("ChainlinkPriceFeed"):
            price_feed_name = "ChainlinkPriceFeed"
        else:
            ValueError(
                "PriceFeed is not L2PriceFeed or ChainlinkPriceFeed, address: "
                + price_feed
            )

        data.append(
            {
                "pair": f"{price_feed_key}/USDC",
                "Proxy Address": addr,
                "Index Price": f"{utils.format_units(index_price[0])} USDC",
                "Market Price": f"{utils.format_units(market_price[0])} USDC",
                "OpenInterestNotionalCap": f"{utils.format_units(open_interest_notional_cap[0])}\
                 USDC",
                "OpenInterestNotional": f"{utils.format_units(open_interest_notional)}\
                 USDC",
                "MaxHoldingBaseAsset": f"{utils.format_units(max_holding_base_asset[0])}\
                 USDC",
                "QuoteAssetReserve": f"{utils.format_units(quote_asset_reserve[0])}\
                 USDC",
                "BaseAssetReserve": f"{utils.format_units(base_asset_reserve[0])}\
                {price_feed_key}USDC",
                "PriceFeed": price_feed_name,
                "est.funding rate": f"{est_funding_rate} %",
            }
        )

    return data

def get_input_twap_amount(
    provider: Providers,
    pair: str,
    dir_of_quote: Dir,
    quote_asset_amount: float
):
    """
    Returns input twap amount.

    Arguments:
    provider -- A Providers object
    pair -- A string representing an amm pair
    dir_of_quote -- Dir.ADD_TO_AMM or Dir.REMOVE_FROM_AMM
    quote_asset_amount -- quote asset amount
    """
    amm = utils.get_amm(pair, provider)
    input_twap = amm.functions.getInputTwap(
        dir_of_quote.value, 
        {'d': utils.parse_units(quote_asset_amount)}
        ).call()
    return input_twap[0]

def get_output_twap_amount(
    provider: Providers,
    pair: str,
    dir_of_quote: Dir,
    base_asset_amount: float
):
    """
    Returns output twap amount.

    Arguments:
    provider -- A Providers object
    pair -- A string representing an amm pair
    dir_of_quote -- Dir.ADD_TO_AMM or Dir.REMOVE_FROM_AMM
    base_asset_amount -- base asset amount
    """
    amm = utils.get_amm(pair, provider)
    output_twap = amm.functions.getOutputTwap(
        dir_of_quote.value,
        {'d': utils.parse_units(base_asset_amount)}
    ).call()
    return output_twap[0]

def get_input_price(
    provider: Providers,
    pair: str,
    dir_of_quote: Dir,
    quote_asset_amount: float
):
    """
    Returns input price.

    Arguments:
    provider -- A Providers object
    pair -- A string representing an amm pair
    dir_of_quote -- Dir.ADD_TO_AMM or Dir.REMOVE_FROM_AMM
    quote_asset_amount -- quote asset amount
    """
    amm = utils.get_amm(pair,provider)
    input_price = amm.functions.getInputPrice(
        dir_of_quote.value,
        {'d': utils.parse_units(quote_asset_amount)}
    ).call()
    return input_price[0]

def get_output_price(
    provider: Providers,
    pair: str,
    dir_of_quote: Dir,
    base_asset_amount: float
):
    """
    Returns output twap amount.

    Arguments:
    provider -- A Providers object
    pair -- A string representing an amm pair
    dir_of_quote -- Dir.ADD_TO_AMM or Dir.REMOVE_FROM_AMM
    base_asset_amount -- base asset amount
    """
    amm = utils.get_amm(pair, provider)
    output_price = amm.functions.getOutputPrice(
        dir_of_quote.value,
        {'d': utils.parse_units(base_asset_amount)}
    ).call()
    return output_price[0]

def get_underlying_price(
    provider: Providers,
    pair: str
):
    """
    Returns underlying price.

    Arguments:
    provider -- A Providers object
    pair -- A string representing an amm pair
    """
    amm = utils.get_amm(pair, provider)
    underlying_price = amm.functions.getUnderlyingPrice().call()
    return underlying_price[0]

def get_underlying_twap_price(
    provider: Providers,
    pair: str,
    interval_in_seconds: int
):
    """
    Returns underlying twap price.

    Arguments:
    provider -- A Providers object
    pair -- A string representing an amm pair
    interval_in_seconds -- interval in seconds 
    """
    amm = utils.get_amm(pair, provider)
    underlying_twap_price = amm.functions.getUnderlyingTwapPrice(
        interval_in_seconds
    ).call()
    return underlying_twap_price[0]

def get_spot_price(
    provider: Providers,
    pair: str
):
    """
    Returns spot price.

    Arguments:
    provider -- A Providers object
    pair -- A string representing an amm pair
    """
    amm = utils.get_amm(pair, provider)
    reserve = get_quote_and_base_asset_reserve(provider, pair)
    return reserve["quoteAssetReserve"]/reserve["baseAssetReserve"]
    
def get_twap_price(
    provider: Providers,
    pair: str,
    interval_in_seconds: int
):
    """
    Returns twap price.

    Arguments:
    provider -- A Providers object
    pair -- A string representing an amm pair
    interval_in_seconds -- interval in seconds 
    """
    amm = utils.get_amm(pair, provider)
    twap_price = amm.functions.getTwapPrice(
        interval_in_seconds
    ).call()
    return twap_price[0]

def get_quote_and_base_asset_reserve(
    provider: Providers,
    pair: str,
):
    """
    Returns quote asset and base asset reserve.

    Arguments:
    provider -- A Providers object
    pair -- A string representing an amm pair
    """
    amm = utils.get_amm(pair, provider)
    reserve = amm.functions.getReserve().call()
    return {
        "quoteAssetReserve": reserve[0][0],
        "baseAssetReserve": reserve[1][0]
    }

def calculate_toll_and_spread_fee(
    provider: Providers,
    pair: str,
    quote_asset_amount: float
):
    """
    Calculates toll and spread fee.

    Arguments:
    provider -- A Providers object
    pair -- A string representing an amm pair
    quote_asset_amount -- quote asset amount
    """
    amm = utils.get_amm(pair, provider)
    fee = amm.functions.calcFee(
        {'d': utils.parse_units(quote_asset_amount)}
    ).call()
    return {
        "tollRatio": fee[0][0],
        "spreadRatio": fee[1][0]
    }

def get_price_impact(
    provider: Providers,
    pair: str,
    entry_price: float
):
    """
    Returns price impact.

    Arguments:
    provider -- A Providers object
    pair -- A string representing an amm pair
    entry_price -- entry price for the trade
    """
    spot_price = get_spot_price(provider, pair)
    price_impact = (entry_price-spot_price)*100/spot_price
    return price_impact
