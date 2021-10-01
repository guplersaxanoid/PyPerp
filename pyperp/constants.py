from enum import Enum

MaxUInt256 = 2**256-1

AvailableAmms = {
    "mainnet": [
        "ETHUSDC", "BTCUSDC", "YFIUSDC",
        "DOTUSDC", "SNXUSDC", "LINKUSDC",
        "AAVEUSDC", "SUSHIUSDC", "COMPUSDC",
        "RENUSDC", "PERPUSDC", "UNIUSDC",
        "CRVUSDC", "MKRUSDC", "CREAMUSDC",
        "GRTUSDC", "ALPHAUSDC", "FTTUSDC"
    ],
    "testnet": [
        "ETHUSDC", "BTCUSDC", "SNXUSDC",
        "LINKUSDC", "SDEFIUSDC", "TRXUSDC",
        "SCEXUSDC", "SUSHIUSDC", "XAGUSDC",
        "AUDUSDC", "PERPUSDC", "UNIUSDC",
        "CRVUSDC", "MKRUSDC", "CREAMUSDC",
        "GRTUSDC", "ALPHAUSDX", "FTTUSDC"
    ]
}

DEFAULT_DECIMALS = 18


class Side(Enum):
    LONG = 0
    SHORT = 1


class PnlCalcOption(Enum):
    SPOT_PRICE = 0
    TWAP = 1
    ORACLE = 2
