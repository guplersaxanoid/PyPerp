from enum import Enum 

MaxUInt256 = None

AvailableAmms = {
    "mainnet":[
        "ETHUSDC","BTCUSDC","YFIUSDC",
        "DOTUSDC","SNXUSDC","LINKUSDC",
        "AAVEUSDC","SUSHIUSDC","COMPUSDC",
        "RENUSDC","PERPUSDC","UNIUSDC",
        "CRVUSDC","MKRUSDC","CREAMUSDC",
        "GRTUSDC","ALPHAUSDC","FTTUSDC"
    ],
    "testnet":[
        "ETHUSDC","BTCUSDC","SNXUSDC",
        "LINKUSDC","SDEFIUSDC","TRXUSDC",
        "SCEXUSDC","SUSHIUSDC","XAGUSDC",
        "AUDUSDC","PERPUSDC","UNIUSDC",
        "CRVUSDC","MKRUSDC","CREAMUSDC",
        "GRTUSDC","ALPHAUSDX","FTTUSDC"
    ]
}

DEFAULT_DECIMALS = 18

class Side(Enum):
    LONG = 0
    SHORT = 1

