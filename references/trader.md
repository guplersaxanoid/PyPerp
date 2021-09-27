# Trader



### `Class pyperp.Trader(provider, l1wallet, l2wallet)`

1.  `provider`:  A `pyperp.Providers` object. 
2.  `l1wallet`: The layer 1 wallet.  It can be created using `web3.eth.account`
3. `l2wallet`: The layer 2 wallet. It can be created using `web3.eth.account`

### Attributes

1. `Trader.layer1wallet` : The layer 1 wallet
2. `Trader.layer2wallet` : The layer 2 wallet

### **Methods**

#### **`Trader.approveL1BridgeToUseUDSC()`** 

Approves `RootBridge` contract to use USDC from Layer 1 wallet by calling `approve()` function of USDC contract in Layer 1.

**Parameters:** None

**Return Value:** The transaction receipt for the approval transaction

#### **`Trader.depositUsdcToxDai()`**

Deposits USDC from layer 1 wallet to layer 2 wallet by the `erc20Transfer()`function of `RootBridge` ****contract **.**

**Parameters:**

1. `amount` : The value of USDC to be deposited to layer 2

**Return Value:** The transaction receipt for the token transfer transaction

#### **`Trader.approveL2BridgeToUseUSDC()`**

Approves `ClientBridge` contract to use USDC from Layer 2 wallet by calling `approve()` function of USDC contract in Layer 2.

**Parameters:** None

**Return Value:** The transaction receipt for the approval transaction

#### `Trader.withdrawUsdcToEthereum()`

Withdraws USDC from layer 2 wallet to layer 1 wallet by the `erc20Transfer()`function of `ClientBridge` ****contract **.**

**Parameters:**

1. `amount` : The value of USDC to be withdrawn to layer 1

**Return Value:** The transaction receipt for the token transfer transaction

#### `Trader.approveClearingHouseToUseUSDC()`

Approves `ClearingHouse` contract to use USDC from Layer 2 wallet by calling `approve()` function of USDC contract in Layer 2.

**Parameters:** None

**Return Value:** The transaction receipt for the approval transaction

#### `Trader.openPosition()`

Opens a position by calling the `openPosition()` function of `ClearingHouse` contract

**Parameters:**

1. `pair` : A pair from any of the available pairs in [`constants.AvailableAmms`](https://github.com/DeveloperInProgress/PyPerp/blob/49c1dc7d44a15f2d4377d41d6b480e49a0d11a9f/pyperp/constants.py#L5)\`\`
2. `side`: 0 for opening long position and 1 for opening short positions. To avoid confusion, [`constants.Side.SHORT.value`](https://github.com/DeveloperInProgress/PyPerp/blob/49c1dc7d44a15f2d4377d41d6b480e49a0d11a9f/pyperp/constants.py#L26) ``and [`constants.Side.LONG.value`](https://github.com/DeveloperInProgress/PyPerp/blob/49c1dc7d44a15f2d4377d41d6b480e49a0d11a9f/pyperp/constants.py#L26) can be used.
3. `quoteAssetAmount` : A non-zero value to be used as the [`_quoteAssetAmount`](https://github.com/perpetual-protocol/perpetual-protocol/blob/d9e65f740ecfec16909eb749820de2284e0baf5d/src/ClearingHouse.sol#L421). It does not have to be 18 digits, that conversion is handled inside the function
4. `leverage` : A non-zero value to be used as the [`_leverage`](https://github.com/perpetual-protocol/perpetual-protocol/blob/d9e65f740ecfec16909eb749820de2284e0baf5d/src/ClearingHouse.sol#L422). It does not have to be 18 digits, that conversion is handled inside the function
5. `baseAssetAmountLimit` : A value to be used as the [`_baseAssetAmountLimit`](https://github.com/perpetual-protocol/perpetual-protocol/blob/d9e65f740ecfec16909eb749820de2284e0baf5d/src/ClearingHouse.sol#L423). It does not have to be 18 digits, that conversion is handled inside the function

**Returns:** The transaction receipt of the contract transaction

#### `Trader.closePosition()`

Closes a position by calling the `closePosition()` function of `ClearingHouse` contract

**Parameters:**

1. `pair`: A pair from any of the available pairs in [`constants.AvailableAmms`](https://github.com/DeveloperInProgress/PyPerp/blob/49c1dc7d44a15f2d4377d41d6b480e49a0d11a9f/pyperp/constants.py#L5)\`\`
2. `quoteAssetAmountLimit` :  A value to be used as the [`_quoteAssetAmountLimit`](https://github.com/perpetual-protocol/perpetual-protocol/blob/d9e65f740ecfec16909eb749820de2284e0baf5d/src/ClearingHouse.sol#L531). It does not have to be 18 digits, that conversion is handled inside the function

**Returns:** The transaction receipt of the contract transaction

#### `Trader.getPersonalPositionWithFundingPayment()`

Returns position data for a pair by calling `getPersonalPositionWithFundingPayment()` function of `ClearingHouseViewer` contract

**Parameters:**

1. `pair`**:** A pair from any of the available pairs in [`constants.AvailableAmms`](https://github.com/DeveloperInProgress/PyPerp/blob/49c1dc7d44a15f2d4377d41d6b480e49a0d11a9f/pyperp/constants.py#L5)\`\`
2. `trader` : \(Optional\) The public of the layer 2 wallet of the trader. If provided, the position details of the given trader is queries. Otherwise, layer 2 wallet address of the calling `Trader` object is used for querying.

**Returns:** A `dict`with the following keys : \['size', 'margin', 'openNotional', 'lastUpdatedCumulativePremiumFraction', 'liquidityHistoryIndex', 'blockNumber'\]

#### `Trader.getUnrealizedPnl()`

Returns unrealized Pnl value by calling the `getUnrealizedPnl()` function of `ClearingHouseViewer` contract.

**Parameters:**

1. `pair`**:** A pair from any of the available pairs in [`constants.AvailableAmms`](https://github.com/DeveloperInProgress/PyPerp/blob/49c1dc7d44a15f2d4377d41d6b480e49a0d11a9f/pyperp/constants.py#L5)\`\`
2. `pnlCalcOption` : It can be either`constants.PnlCalcOption.SPOT_PRICE` or `constants.PnlCalcOption.TWAP`
3. `trader` : \(Optional\) The public of the layer 2 wallet of the trader. If provided, the unrealized pnl value of the given trader is queries. Otherwise, layer 2 wallet address of the calling `Trader` object is used for querying.

**Returns:** The unrealized pnl value for the given pair

#### `Trader.getEntryPrice()`

Returns the entry price for given pair.

**Parameters:**

1. `pair`:  ****A pair from any of the available pairs in [`constants.AvailableAmms`](https://github.com/DeveloperInProgress/PyPerp/blob/49c1dc7d44a15f2d4377d41d6b480e49a0d11a9f/pyperp/constants.py#L5)\`\`

**Returns:** The entry price for given pair

#### **`Trader.addMargin():`**

Adds margin to the position in the given pair by calling `addMargin()` function of `ClearingHouse` contract.

**Parameters:**

1. `pair`**:** A pair from any of the available pairs in [`constants.AvailableAmms`](https://github.com/DeveloperInProgress/PyPerp/blob/49c1dc7d44a15f2d4377d41d6b480e49a0d11a9f/pyperp/constants.py#L5)\`\`
2. `margin`:A non-zero value to be added as margin. It does not have to be 18 digits, that conversion is handled inside the function

**Returns:** The transaction receipt of the contract transaction

#### **`Trader.removeMargin()`**

Removes margin from the position in the given pair by calling `removeMargin()` function of `ClearingHouse` contract.

**Parameters:**

1. `pair`**:** A pair from any of the available pairs in [`constants.AvailableAmms`](https://github.com/DeveloperInProgress/PyPerp/blob/49c1dc7d44a15f2d4377d41d6b480e49a0d11a9f/pyperp/constants.py#L5)\`\`
2. `margin`:A non-zero value to be removed as margin. It does not have to be 18 digits, that conversion is handled inside the function

**Returns:** The transaction receipt of the contract transaction

#### **`Trader.settlePosition()`**

Settles a position by calling `settlePosition()` function of `ClearingHouse` contract.

**Parameters:**

1. `pair`**:** A pair from any of the available pairs in [`constants.AvailableAmms`](https://github.com/DeveloperInProgress/PyPerp/blob/49c1dc7d44a15f2d4377d41d6b480e49a0d11a9f/pyperp/constants.py#L5)\`\`

**Returns:** The transaction receipt of the contract transaction

#### **`Trader.liquidate()`**

liquidates a position by calling `liquidate()` function of `ClearingHouse` contract.

**Parameters:**

1. `pair`**:** A pair from any of the available pairs in [`constants.AvailableAmms`](https://github.com/DeveloperInProgress/PyPerp/blob/49c1dc7d44a15f2d4377d41d6b480e49a0d11a9f/pyperp/constants.py#L5)\`\`

**Returns:** The transaction receipt of the contract transaction

