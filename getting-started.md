# Getting Started

### Installation

The pyperp package  can be installed using pip:

```bash
pip install pyperp
```

### **Using PyPerp**

All of the trades in Perpetual Protocol are done on Layer 2 \(xDai\). More than often, a trader is required to deposit USDC to xDai from Layer 1 and withdraw USDC back to Layer 1. For this reason, 4 parameters are necessary to use the core functionalities of PyPerp:

1. Layer 1 wallet
2. Layer 2 wallet
3. Layer 1 Node \(Ethereum/Rinkeby\)
4. Layer 2 Node \(xDai\)

These 4 parameters will be used to create a Trader object

Here is an example code that creates a Trader object on testnet \(Rinkeby/xDai\)

```python
from web3 import Web3
from web3.middleware import geth_poa_middleware
from pyperp import Trader, Providers

l2provider = Web3(Web3.HTTPProvider("https://rpc.xdaichain.com/"))
l1provider = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/YOUR_PROJECT_ID_HERE"))
l1provider.middleware_onion.inject(geth_poa_middleware, layer=0) #rinkeby used poa
provider = Providers(l1provider,l2provider,True) #The third argument specifies whether the providers are in testnet or mainnet. True means testnet, False means Mainnet

l1wallet = provider.l1.eth.account.privateKeyToAccount("PRIVATE_KEY_HERE")
l2wallet = provider.l2.eth.account.privateKeyToAccount("PRIVATE_KEY_HERE")

trader = Trader(provider, l1wallet, l2wallet)

```

The Perpetual Protocol team has hosted a test USDC faucet to enable testing their platform using the testnet. You may acquire some USDC from this faucet by calling `pyperp.Faucets.getUsdcL1(address)`function

```python
from pyperp import Faucets

response = Faucets.getUsdcL1(trader.layer1wallet.address)
print(response)
```

In order to move USDC from L1 to L2, you need to approve the Layer 1 Bridge \([`RootBridge`](https://github.com/perpetual-protocol/perpetual-protocol/blob/master/src/bridge/ethereum/RootBridge.sol)\)  to use the USDC from your layer 1 wallet. This can be done by calling `Trader.approveL1BridgeToUseUSDC()`

```python
receipt = trader.approveL1BridgetoUseUSDC()
print(receipt)
```

Then, to move your USDC from Layer1 to Layer2, call `Trader.depositUsdcToxDai(amount)`

```python
receipt = trader.depositUsdcToxDai(100) #move 100 USDC to xDai 
```

The [`ClearingHouse`](https://github.com/perpetual-protocol/perpetual-protocol/blob/master/src/ClearingHouse.sol) contract houses all the functions required to trade on Perpetual Protocol. In order to begin trading, you have to approve the `ClearingHouse` contract to use the USDC in your Layer 2 wallet. This can be done by calling `Trader.approveClearingHouseToUseUSDC()`

```python
receipt = trader.approveClearingHouseToUseUSDC()
print(receipt)
```

A position can be opened with a pair of your using `Trader.openPosition()`. For example, A position with ETH/USDC can be opened as follows:

```python
from pyperp import constants

receipt = trader.openPosition("ETHUSDC",constants.Side.SHORT.value,100,2,0)
print(receipt)

#Trader.openPosition(pair, side, quoteAssetAmount, leverage, baseAssetAmountLimit)
#pair : Can be any of the available pairs in Perpetual Protocol
#side : O(for long) or 1(for short)
#quoteAssetAmount : A non-zero number
#leverage : must be in the range (0,10]
```

`pyperp.constants.Side` is an Enum class that contains two values: `LONG` \(equals to 0\) is the side value for opening a long position and `SHORT` \(equals to 1\) is the side value for opening a short position. 

The [`ClearingHouseViewer`](https://github.com/perpetual-protocol/perpetual-protocol/blob/master/src/ClearingHouseViewer.sol) contract provides functions to query position data for a trader address\(`clearingHouseViewer.getPersonalPositionWithFundingPayment()` and `clearingHouseViewer.getUnrealizedPnl()`\). The `Trader` class houses two high level functions\(`Trader.getPersonalPositionWithFundingPayment()` and `Trader.getUnrealizedPnl()`\) to get position data by calling the functions in `ClearingHouseViewer`

```python
print(trader.getPersonalPositionWithFundingPayment("ETHUSDC"))
print(trader.getUnrealizedPnl("ETHUSDC",constants.PnlCalcOption.SPOT_PRICE))
```

The `PnlCalcOption` is an Enum class in `constants` that contains the following values:

1. `SPOT_PRICE` : 0
2. `TWAP`: 1
3. `ORACLE`: 2

Margin can be added to an existing position using `Trader.addMargin(pair, margin)` 

```python
receipt = trader.addMargin("ETHUSDC", 10)
print(receipt)
```

Similarly, margin can be removed from an existing position using `Trader.removeMargin(pair, margin)`

```python
receipt = trader.removeMargin("ETHUSDC", 10)
print(receipt)
```

An existing position can be closed using `Trader.closePosition(pair, quoteAssetAmountLimit)`

```python
receipt = trader.closePosition("ETHUSDC",0) #the second parameter is quote asset amount limit
print(receipt)
```

In order to withdraw USDC from layer 2 to layer 1, approve the Layer 2 bridge \([`ClientBridge`](https://github.com/perpetual-protocol/perpetual-protocol/blob/master/src/bridge/xDai/ClientBridge.sol)\) to use USDC in your layer 2 wallet

```python
reciept = trader.approveL2BridgeToUseUSDC()
print(receipt)
```

Then, withdraw  USDC to Layer 1 using `Trader.withdrawUsdcToEthereum(amount)`

```python
receipt = trader.withdrawUsdcToEthereum(100)
print(receipt)
```

