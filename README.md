# PyPerp

A python SDK for [Perpetual Protocol](https://github.com/perpetual-protocol/perpetual-protocol). 

## Installation

From PyPi: 

`pip install pyperp`

## Documentation

The complete documentation can be found [here](https://velnaveen99.gitbook.io/pyperp/)

## Example Code

This example code is written to demonstrate simple trading on the testnet.

1.) creating a Trader object

```
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

2.) using the USDC faucet in rinkeby

```
from pyperp import Faucets

response = Faucets.getUsdcL1(trader.layer1wallet.address)
print(response)
```

This USDC faucet is hosted by the Perpetual Protocol team, and it can be used only once per address. 

3.) moving USDC from layer1 to layer2

allow layer1 bridge to use your USDC funds if not done already

```
receipt = trader.approveL1BridgetoUseUSDC()
print(receipt)
```

Then, call `depositUsdcToXdai()`
```
receipt = trader.depositUsdcToxDai(100) #move 100 USDC to xDai 
```

4.) open a position 

allow ClearingHouse contract to use the USDC in your xDai if not done already. 

```
receipt = trader.approveClearingHouseToUseUSDC()
print(receipt)
```

Open a position with a pair of your choice using the openPosition() method in Trader class. Here, the ETH/USDC pair is used

```
from pyperp import constants

receipt = trader.openPosition("ETHUSDC",constants.Side.SHORT.value,100,2,0)
print(receipt)
```

the openPosition() function takes the following parameters:
1. The pair: the pair has to chosen from the available pairs in `AvailableAmms` dict in `constants.py` file
2. side: Has to be either constants.Side.LONG.value (0) or constants.Side.SHORT.value (1) 
3. quoteAssetAmount
4. leverage
5. baseAssetAmountLimit


5.) get position information 

```
print(trader.getPersonalPositionWithFundingPayment("ETHUSDC"))
print(trader.getUnrealizedPnl("ETHUSDC",constants.PnlCalcOption.SPOT_PRICE))
```

The second parameter of the getUnrealizedPnl function is the PnlCalcOption which can be any of these three values : constants.PnlCalcOption.SPOT_PRICE(0), constants.PnlCalcOption.TWAP(1), constants.PnlCalcOption.ORACLE(2)

6.) add margin to position:

```
receipt = trader.addMargin("ETHUSDC", 10)
print(receipt)
```

7.) remove margin:

```
receipt = trader.removeMargin("ETHUSDC", 10)
print(receipt)
```

8.) close a position:

```
receipt = trader.closePosition("ETHUSDC",0) #the second parameter is quote asset amount limit
print(receipt)
```

9.) withdrawing USDC to L1

allow Layer 2 Bridge to use the USDC if not done already

```
reciept = trader.approveL2BridgeToUseUSDC()
print(receipt)
```

then, withdraw USDC to L1 using `withdrawUsdcToEthereum()` function in `Trader` class

```
receipt = trader.withdrawUsdcToEthereum(100)
print(receipt)
```






