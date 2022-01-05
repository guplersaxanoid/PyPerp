# Contracts

Contract classes interfaces with smart contracts of v2 curie

## AccountBalance

The AccountBalance class interfaces with the AccountBalance contract

### Importing

```
from pyperp.contracts import AccountBalance
```

### Properties

`account_balance`: Web3.eth.contract() object for AccountBalance contract

### Methods

#### get_base_tokens

Returns a list of base tokens owned by trader

**Arguments:**

`trader`: Wallet address of trader

#### get_account_info

Returns account info of trader with respect to a base token

**Arguments:**

`trader`: wallet address of trader

`base_token`: contract address of base token

**Return Value:**
Returns `pyperp.contracts.types.AccountMarketInfo` object

#### get_taker_open_notional

Returns taker open notional of trader with respect to a base token

**Arguments:**

`trader`: wallet address of trader

`base_token`: contract address of base token

#### get_total_open_notional

Returns total open notional of trader with respect to a base token

**Arguments:**

`trader`: wallet address of trader

`base_token`: contract address of base token

#### get_total_debt_value

Returns total debt value of a trader

**Arguments:**

`trader`: wallet address of trader

#### get_marginal_requirement_for_liquidation

Returns marginal requirement for liquidation

**Arguments:**

`trader`: wallet address of trader

#### get_pnl_and_pending_fee

Returns PNL and Pending fee for a trader

**Arguments:**

`trader`: wallet address of trader

**Return Value:**

Returns a dict of the following format:

```
{
    'owed_realized_pnl': <INT_VALUE>,
    'unrealized_pnl': <INT_VALUE>,
    'pending_fee':<INT_VALUE>
}
```

#### has_order

Checks if a trader has an open order

**Arguments:**

`trader`: wallet address of trader

**Return Value:**

`True`: If there are open orders
`False`: If there are no open orders

#### has_order_in_open_or_closed_market

Checks if a trader has orders in open or closed market

**Arguments:**

`trader`: wallet address of trader

**Return Value:**

`True`: If there are orders
`False`: If there are no orders

#### get_base

Return amount of base token owned in terms of base

**Arguments:**

`trader`: wallet address of trader

`base_token`: contract address of base token

#### get_quote

Return amount of base token owned in terms of quote

**Arguments:**

`trader`: wallet address of trader

`base_token`: contract address of base token

#### get_taker_position_size

Returns taker position size

**Arguments:**

`trader`: wallet address of trader

`base_token`: contract address of base token

#### get_total_position_size

Returns total position size

**Arguments:**

`trader`: wallet address of trader

`base_token`: contract address of base token

#### get_total_position_value

Returns total position value

**Arguments:**

`trader`: wallet address of trader

`base_token`: contract address of base token

#### get_total_abs_positon_value

Returns total absolute position value

**Arguments:**

`trader`: wallet address of trader

#### settle_pnl_closed_market

Settle PNL in closed market

**Arguments:**

`trader`: wallet address of trader

`base_token`: contract address of base token

## ClearingHouse

This class interfaces with the ClearingHouse contract

### Importing

```
from pyperp.contracts import ClearingHouse
```

### Properties

`clearing_house`: `Web3.eth.contract()` object for ClearingHouse contract

`usdc`: `Web3.eth.contract()` object for USDC contract

`vbtc`: `Web3.eth.contract()` object for vBTC contract

`veth`: `Web3.eth.contract()` object for vETH contract

### Methods

#### add_liquidity

Add liquidity to a token

**Arguments:**

`params`: `AddLiquidityParams` object

`gas_params`: `GasParams` object

#### remove_liquidity

Remove liquidity from a token

**Arguments:**

`params`: `RemoveLiquidityParams` object

`gas_params`: `GasParams` object

#### settle_all_funding

Settle all funding

**Arguments:**

`trader`: wallet address of trader

`gas_params`: `GasParams` object\

#### open_position

Open Position

**Arguments:**

`params`: `OpenPositionParams` object

`gas_params`: `GasParams` object

#### close_position

Close position

**Arguments:**

`params`: `ClosePosition` object

`gas_params`: `GasParams` object

#### liquidate

Liquidate

**Arguments:**

`trader`: wallet address of trader

`base_token`: contract address of base token

`gas_params`: `GasParams` object

#### cancel_all_excess_order

Cancel all excess orders

**Arguments:**

`maker`: wallet address of maker

`base_token`: contract address of base token

`gas_params`: `GasParams` object

#### close_position_in_closed_market

Close position in closed market

**Arguments:**

`trader`: wallet address of trader

`base_token`: contract address of base token

`gas_params`: `GasParams` object

#### uniswap_v3_mint_callback

Uniswap V3 mint callback

**Arguments:**

`amount0Owed`: integer
`amount1owed`: integer
`data`: string
`gas_parmas`: A GasParams object

#### uniswap_v3_swap_callback

Uniswap V3 swap callback

**Arguments:**

`amount0Delta`: integer
`amount1Delta`: integer
`data`: string
`gas_params`: `GasParams` object

#### get_quote_token

Returns quote token contract address

#### get_uniswap_v3_factory

Returns UniswapV3Factory contract address

#### get_clearing_house_config

Return ClearingHouseConfig contract adderss

#### get_vault

Return Vault contract address

#### get_exchange

Return Exchange contract address

#### get_order_book

Return OrderBook contract address

#### get_account_balance

Return AccountBalance contract address

#### get_insurance_fund

Return InsuranceFund contract address

#### get_account_value

Return account value of a trader

**Arguments:**

`trader`: wallet address of trader

## MarketRegistry

This class interfaces with the MarketRegistry smart contract

### Importing

```
from pyperp.contracts import MarketRegistry
```

### Properties

`market_registry`: `Web3.eth.contract` object for MarketRegistry contract

### Methods

#### get_quote_token

Returns quote token contract address

#### get_uniswap_v3_factory

Returns UniswapV3Factory contract address

#### get_max_order_per_market

Returns maximum orders per market

#### get_pool

Returns pool address of a base token

**Arguments:**

`base_token`: contract address of base token

#### get_insurance_fund_fee_ratio

Returns insurance fund fee ratio for a base token

**Arguments:**

`base_token`: contract address of base token

#### get_market_info

Returns market info for a base token

**Arguments:**

`base_token`: contract address of base token

**Return Value:**

A `pyperp.contracts.types.MarketInfo` object

## OrderBook

This class interfaces with the OrderBook smart contract

### Importing

```
from pyperp.contracts import OrderBook
```

### Properties

`order_book`: `Web3.eth.contract` object for OrderBook contract

### Methods

#### get_exchange

Returns Exchange contract address

#### get_open_order_ids

Returns open order ids of a trader with respect to a base token

**Arguments:**

`trader`: wallet address of trader

`base_token`: contract address of base token

#### get_open_order_by_id

Returns open order info

**Arguments:**

`order_id`: HexBytes object representing order id

**Return Value":**

Returns `pyperp.contracts.types.OpenOrderInfo` object

#### get_open_order

Returns open order

**Arguments:**

`trader`: wallet address of a trader
`base_token`: contract address of a base token
`lower_tick`: lower tick
`upper_tick`: upper tick"

**Return Value:**

Returns `pyperp.contracts.types.OpenOrderInfo` object

#### has_order

Checks if a trader has any open order

**Arguments:**

`trader`: wallet address of a trader
`tokens`: list of token addresses

#### get_total_quote_balance_and_pending_fee

Returns total quote balance and pending fee
        
**Arguments:**

`trader`: wallet address of trader
`base_token`: contract address of token

**Return Value:**

Returns a dict of following format:

```
{
    'total_quote_amount_in_pools': <INT_VALUE>,
    'total_pending_fee': <INT_VALUE>
}
```

#### get_total_token_amount_in_pool_and_pending_fee

Returns total token amount and pending fee.
        
**Arguments:**
    
`trader`: wallet address of trader
`base_token`: contract address of base token
`fetch_base`: fetch base

**Return Value:**

Returns a dict of following format:

```
{
    'token_amount': <INT_VALUE>,
    'pending_fee': <INT_VALUE>
}
```

#### get_liquidity_coefficient_in_funding_payment

Returns liquidity coefficient in funding payment
       
**Arguments:**
        
`trader`: wallet address of trader
`base_token`: contract address of base token
`funding_growth_global`: FundingGrowth object"

#### get_pending_fee

Returns pending fee.
        
**Arguments:**
        
`trader`: wallet address of trader
`base_token`: contract address of base token
`lower_tick`: lower tick
`upper_tick`: upper tick

#### get_total_order_debt

Returns total order debt.
        
**Arguments:**
        
`trader`: wallet address of trader
`base_token`: contract address of base token
`fetch_base`: fetch base

## Vault

This class interfaces with the Vault contract

### Importing

```
from pyperp.contracts.vault import Vault
```

### Properties

`vault`: `Web3.eth.contract` object of Vault contract

`usdc`: `Web3.eth.contract` object of USDC contract

### Methods

#### approve_vault_to_use_usdc

Approves Vault contract to use USDC from trader's wallet

**Arguments:**

`gas_params`: A `pyperp.common.types.GasParams` object

#### deposit

Deposit collateral amount.
        
**Arguments:**
        
`token`: Token address
`amount_x10_D`: amount to deposit
`gas_params`: A `pyperp.common.types.GasParams` object

#### deposit_for

Deposit collateral for a different address.
        
**Arguments:**
        
`to`: wallet address to deposit to
`token`: contract address of token
`amount_x10_D`: amount to deposit
`gas_params`: A `pyperp.common.types.GasParams` object

#### withdraw

Withdraw collateral amount.
        
**Arguments:**

`token`: Token address
`amount_x10_D`: amount to withdraw
`gas_params`: GasParams object

#### get_settlement_token

Returns settlement token address.

#### decimals

Returns number of decimals.

#### get_total_debt

Returns total debt.

#### get_clearing_house_config

Returns contract address of ClearingHouseConfig.

#### get_account_balance

Returns contract address of AccountBalance

#### get_insurance_fund

Returns contract address of InsuranceFund

#### get_exchange

Returns contract address of Exchange

#### get_clearing_house

Returns contract address of ClearingHouse

#### get_free_collateral

Check how much collateral a trader can withdraw.
        
**Arguments:**
        
`trader`: wallet adderss of trader

#### get_balance

Returns vault balance of trader.
        
**Arguments:**

`trader`: wallet address of trader

#### get_free_collateral_by_ratio

Returns free collateral by ratio.
        
**Arguments:**
        
`trader`: wallet address of trader
`ratio`: ratio

## types

Contains dataclasses for use in parameters and return types

### OpenPositionParams

Used as parameter in `pyperp.contracts.ClearingHouse.open_position()` function

#### Importing

```
from pyperp.contracts.types import OpenPositionParams
```

#### Fields

`base_token`: base token address

`is_base_to_quote`: Boolean. Takes `True` or `False`.

`is_exact_input`: Boolean. Takes `True` or `False`.

`amount`: integer amount value.

`opposite_amount_bound`: integer `OppositeAmountBound` value

`deadline`: UNIX time to be used as deadline for trade

`sqrt_price_limit_x96`: integer `sqrtPriceLimitX96` value

`referral_code`: HexBytes representing `ReferralCode`. Defaults to 0.

### ClosePositionParams

Used as parameter in `pyperp.contracts.ClearingHouse.close_position()` function

#### Importing

```
from pyperp.contracts.types import ClosePositionParams
```

#### Fields

`base_token`: base token address

`sqrt_price_limit_x96`: integer `sqrtPriceLimitX96` value

`opposite_amount_bound`: integer `OppositeAmountBound` value

`deadline`: UNIX time to be used as deadline for trade

`referral_code`: HexBytes representing `ReferralCode`. Defaults to 0.

### AddLiquidityParams

Used as parameter in `pyperp.contracts.ClearingHouse.add_liquidity()` function

#### Importing

```
from pyperp.contracts.types import AddLiquidityParams
```

#### Fields

`base_token`: Contract address of base token

`base`: base amount to add

`quote`: quote amount to add

`lower_tick`: `lowerTick` value

`upper_tick`: `upperTick` value

`min_base`: `minBase` value

`min_quote`: `minQuote` value

`deadline`: UNIX time to be used as deadline for trade

### RemoveLiquidityParams

Used as parameter in `pyperp.contracts.ClearingHouse.remove_liquidity()` function

#### Importing

```
from pyperp.contracts.types import RemoveLiquidityParams
```

#### Fields

`base_token`: Contract address of base token

`lower_tick`: `lowerTick` value

`upper_tick`: `upperTick` value

`liquidity`: integer liquidity value

`min_base`: `minBase` value

`min_quote`: `minQuote` value

`deadline`: UNIX time to be used as deadline for trade

### MarketInfo

Used as return type in `pyperp.contracts.MarketRegistry.get_market_info()`

#### Importing

```
from pyperp.contracts.types import MarketInfo
```

#### Fields

`pool`: Pool address
`exchange_fee_ratio`: Exchange Fee ratio
`uniswap_fee_ratio`: Uniswap Fee ratio
`insurance_fund_fee_ratio`: Insurance Fund Fee Ratio

### OpenOrderInfo

Used as return type in `pyperp.contracts.OrderBook.get_open_order()` and `pyperp.contracts.OrderBook.get_open_order_by_id()`

#### Importing

```
from pyperp.contracts.types import OpenOrderInfo
```

#### Fields

`liquidity`: Integer liquidity value

`lower_tick`: `lowerTick` value

`upper_tick`: `upperTick` value

`last_fee_growth_inside_x96`: `lastFeeGrowthInsideX96` value

`last_tw_premium_growth_inside_x96`: `lastTwPremiumGrowthInsideX96` value

`last_tw_premium_div_by_sqrt_price_growth_inside_x96`: `lastTwPremiumDivBySqrtPriceGrowthInsideX96` value

`base_debt`: Base debt value

`quote_debt`: Quote debt value
