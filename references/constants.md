# constants

#### `MaxUINT256` 

It is maximum value of an Unsigned uint256 datatype. Equals  2^256 - 1

#### `AvailableAmms`

Contains list of available pairs for mainnet and testnet seperately inside a `dict`

```text
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
```

**`DEFAULT_DECIMALS`**

It is the default number of decimal units used while parsing and formatting a value. It is equal to 18

**`Side`**

It is an Enum class that contains two values:

1. `LONG` \(value = 0\)
2. `SHORT` \(value = 1\)

It is used while opening a position

**`PnlCalcOptions`**

It is an Enum class that contains three values:

1. `SPOT_PRICE` \(value = 0\)
2. `TWAP` \(value = 1\)
3. `ORACLE`  \(value = 2\)

It is used while calculating unrealized pnl value.

