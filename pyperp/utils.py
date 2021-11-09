"""utility function to be used throughout the package."""

import json
from pyperp import Providers, Amm
from pyperp.MetaData import MetaData
from pyperp import constants
import datetime
import pkgutil


def confirm_transfer_to_layer2(receipt, provider):
    """
    Confirm transfer from layer 1 to layer2 through RootBrige.

    Arguments:
    receipt -- The transaction receipt of transaction
    provider -- A Provider object
    """
    meta = MetaData(provider.testnet)
    layer2_amb_abi = json.loads(pkgutil.get_data(__name__, "abi/AmbL2.json"))
    layer2_amb_addr = meta.get_l2_ext_contract_address("ambBrideOnXDai")
    layer2_amb = provider.l2.eth.contract(
        address=layer2_amb_addr,
        abi=layer2_amb_abi
    )
    method_id = "0x482515ce"
    for r in receipt:
        log = r["logs"]
        if log.topics[0][:10] == method_id:
            break
    from_msg_id = log.topics[1]
    confirmation_filter = layer2_amb.events.AffirmationCompleted.createFilter(
        fromBlock="latest", argument_filters={"toMsgId": from_msg_id}
    )
    while True:
        for c in confirmation_filter:
            print("Transfer completed")
            return


def confirm_transfer_to_layer1(reciept, provider):
    """
    Confirm transfer from layer 2 to layer 1 through ClientBridge.

    Arguments:
    receipt -- The transaction receipt of transaction
    provider -- A Providers object
    """
    meta = MetaData(provider.testnet)
    layer1_amb_abi = json.loads(pkgutil.get_data(__name__, "abi/AmbL1.json"))
    layer1_amb_addr = meta.get_l1_ext_contract_address("ambBridgeOnEth")
    layer1_amb = provider.l1.eth.contract(
        address=layer1_amb_addr,
        abi=layer1_amb_abi
    )
    method_id = "0x520d2afd"
    for r in reciept:
        log = r["logs"]
        if log.topics[0][:10] == method_id:
            break
    from_msg_id = log.topics[1]
    confirmation_filter = layer1_amb.events.RelayedMessage.createFilter(
        fromBlock="latest", argument_filters={"toMsgId": from_msg_id}
    )
    while True:
        for c in confirmation_filter:
            print("Transfer completed")
            return


def get_amm(pair, provider):
    """
    Return web3.eth.contract object for given amm.

    Arguments:
    pair -- A string representing the amm pair
    provider -- A Providers object
    """
    if provider.testnet:
        amms = constants.available_amms["testnet"]
    else:
        amms = constants.available_amms["mainnet"]

    if pair not in amms:
        raise ValueError(f"Unknown pair: {pair}")

    meta = MetaData(provider.testnet)
    amm_addr = meta.get_l2_contract_address(pair)
    amm_abi = json.loads(pkgutil.get_data(__name__, "abi/Amm.json"))

    amm = provider.l2.eth.contract(address=amm_addr, abi=amm_abi)
    return amm


def estimate_liquidation_price(position, amm, clearing_house):
    """
    Estimate liquidation price for a position.

    Arguments:
    position: The position data
    amm: web3.eth.contract object for the amm
    clearing_house: web3.eth.contract object for ClearingHouse
    """
    spot_price = amm.functions.getSpotPricer.call().d
    real_close_quote_amount = (
        amm.functions.getOutputPrice(
            0 if position.size.d > 0 else 1,
            json.dumps(f"d: {abs(position.size.d)}")
        )
        .call()
        .d
    )
    maintanence_margin_ratio = clearing_house.functions.maintanenceMarginRatio(
    ).call()
    open_notional = position.openNotional.d
    position_size_abs = abs(position.size.d)
    margin = position.margin.d
    entry_price = open_notional / position_size_abs
    reverse_leverage = margin / open_notional
    spot_close_quote_amount = spot_price * position_size_abs
    close_pos_price_slippage = (
        real_close_quote_amount - spot_close_quote_amount
    ) / spot_close_quote_amount
    if position.size.d > 0:
        liquidation_price = entry_price * (
            1 - reverse_leverage - close_pos_price_slippage
            + maintanence_margin_ratio
        )
    else:
        liquidation_price = entry_price * (
            1 + reverse_leverage - close_pos_price_slippage
            - maintanence_margin_ratio
        )
    return liquidation_price


def parse_units(amount, decimal=constants.DEFAULT_DECIMALS):
    """
    Return value parsed to given decimal units.

    Arguments:
    amount -- the value to be parsed
    decimal -- number of decimal units to parse the value to.
    """
    return int(amount * (10 ** decimal))


def format_units(amount, decimal=constants.DEFAULT_DECIMALS):
    """
    Return value formatted to given decimal units.

    Arguments:
    amount -- the value to be formatted
    decimal -- number of decimal units to format the value to.
    """
    return amount / (10 ** decimal)


def estimated_funding_rate(amm):
    """
    Return estimate funding rate for an amm.

    Arguments:
    amm -- web3.eth.contract object representing amm
    """
    duration_from_sharp = datetime.datetime.now().minute * 60
    twap_price = amm.functions.getTwapPrice(duration_from_sharp).call()
    underlying_twap_price = amm.functions.getUnderlyingTwapPrice(
        duration_from_sharp
    ).call()
    funding_period = amm.functions.fundingPeriod().call()
    one_day_in_sec = 60 * 60 * 24
    market_twap_price = format_units(twap_price[0])
    index_twap_price = format_units(underlying_twap_price[0])
    premium = market_twap_price - index_twap_price
    premium_fraction = premium * funding_period / one_day_in_sec
    return parse_units(premium_fraction / index_twap_price)

def get_base_asset_amount_limit(
    provider: Providers,
    pair: str,
    quote_asset_amount: float,
    slippage_tolerance: float,
    dir_of_quote: constants.Dir
):
    """
    Base asset amount limit for given slippage.

    Arguments:
    provider -- Providers object
    pair -- string representing amm pair
    quote_asset_amount -- The quote asset amount
    slippage_tolerance -- percentage of slippage tolerance
    dir_of_quote -- Dir.ADD_TO_AMM or Dir.REMOVE_FROM_AMM
    """
    base_asset_amount = Amm.get_input_price(
        provider, pair, dir_of_quote, quote_asset_amount
    )
    base_asset_amount_limit = base_asset_amount * (1-slippage_tolerance/100)
    return base_asset_amount_limit

def get_quote_asset_amount_limit(
    provider: Providers,
    pair: str,
    base_asset_amount: float,
    slippage_tolerance: float,
    dir_of_quote: constants.Dir
):
    """
    quote asset amount limit for given slippage.

    Arguments:
    provider -- Providers object
    pair -- string representing amm pair
    base_asset_amount -- The base asset amount
    slippage_tolerance -- percentage of slippage tolerance
    dir_of_quote -- Dir.ADD_TO_AMM or Dir.REMOVE_FROM_AMM
    """
    quote_asset_amount = Amm.get_output_price(
        provider, pair, dir_of_quote, base_asset_amount
    )
    quote_asset_amount_limit = quote_asset_amount * (1-slippage_tolerance/100)
    return quote_asset_amount_limit

def calc_entry_price(
    provider: Providers,
    pair: str,
    collateral: float,
    leverage: float,
    dir_of_quote: constants.Dir
):
    """
    calculates entry price for a trade.

    Arguments:
    provider -- Providers object
    pair -- string representing amm pair
    collateral -- collateral amount in usdc
    leverage -- leverage value between 1 and 10
    dir_of_quote -- Dir.ADD_TO_AMM or Dir.REMOVE_FROM_AMM
    """
    position_size = Amm.get_input_price(
        provider, pair, dir_of_quote, collateral
    )
    return collateral*leverage/format_units(position_size)