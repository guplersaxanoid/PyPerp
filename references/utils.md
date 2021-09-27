# utils

### **Methods:**

#### **`confirmTransferToLayer2()`**

Confirms the completion of token transfer from Layer 1 to Layer 2 that was initiated by the function call to `RootBridge.erc20Transfer()` by following the algorithm given [here](https://docs.perp.fi/sdk-documentation/smart-contract-javascript-dev-guide#deposit-and-withdraw-between-ethereum-and-xdai)

**Parameters :**

1. `receipt`**:** The transaction receipt of the token transfer
2. `provider`: A `pyperp.Providers` object 

**Returns:** None

#### **`confirmTransferToLayer1()`**

Confirms the completion of token transfer from Layer 2 to Layer 1 that was initiated by the function call to `ClientBridge.erc20Transfer()` by following the algorithm given [here](https://docs.perp.fi/sdk-documentation/smart-contract-javascript-dev-guide#deposit-and-withdraw-between-ethereum-and-xdai)

**Parameters :**

1. `receipt`**:** The transaction receipt of the token transfer
2. `provider`: A `pyperp.Providers` object 

**Returns:** None

#### `getAmm()`

Returns a contract object of the given Amm pair. 

**Parameters:**

1. `pair`**:**A pair from any of the available pairs in [`constants.AvailableAmms`](https://github.com/DeveloperInProgress/PyPerp/blob/49c1dc7d44a15f2d4377d41d6b480e49a0d11a9f/pyperp/constants.py#L5)\`\`
2. `provider`:A `pyperp.Providers` object 

**Returns:** A `web3.eth.contract` object of the Amm corresponding to the given pair

#### `parseUnits()`

Returns the given value parsed to given number of decimal places

**Parameters:**

1. `amount`: The value to be parsed
2. `decimal`:\(Optional\) Number of decimal places to parse the value. Defaults to 18

**Returns:** The parsed amount

#### `formatUnits()`

Returns the given value formatted to given number of decimal places

**Parameters:**

1. `amount`: The value to be parsed
2. `decimal`:\(Optional\) Number of decimal places to format the value. Defaults to 18

**Returns:** The formatted amount

#### **`estimatedFundingRate()`**

Returns the estimated funding rate for given amm.

**Parameters:**

1. `amm`:  A `web3.eth.contract` object for the amm contract for which funding rate is to be estimated

**Returns:**  The estimated funding rate.

