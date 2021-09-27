# Faucets

This file contains functions related to testnet faucets

### Methods:

#### `getUsdcL1()`

Uses the [test USDC faucet ](https://docs.perp.fi/sdk-documentation/smart-contract-javascript-dev-guide#set-up-test-usdc)deployed by the Perpetual Protocol team to deposit USDC into given testnet layer 1 wallet address. 

**Parameters:**

1. `address`**:** The public address of layer 1 testnet wallet

**Returns:** The response from the faucet

{% hint style="info" %}
Note: This faucet can be used only once per address
{% endhint %}

