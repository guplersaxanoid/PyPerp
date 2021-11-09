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

response = Faucets.get_usdc_l1(trader.layer1wallet.address)
print(response)
```

This USDC faucet is hosted by the Perpetual Protocol team, and it can be used only once per address. 

3.) moving USDC from layer1 to layer2

allow layer1 bridge to use your USDC funds if not done already

```
receipt = trader.approve_l1_bridge_to_use_usdc({"GasPrice":<gas price>, "GasLimit":<gas limit>})
print(receipt)
```

Then, call `depositUsdcToXdai()`
```
receipt = trader.deposit_usdc_to_xdai(100,{"GasPrice":<gas price>, "GasLimit":<gas limit>}) #move 100 USDC to xDai 
```

4.) open a position 

allow ClearingHouse contract to use the USDC in your xDai if not done already. 

```
receipt = trader.approve_clearing_house_to_use_usdc({"GasPrice":<gas price>, "GasLimit":<gas limit>})
print(receipt)
```

Open a position with a pair of your choice using the openPosition() method in Trader class. Here, the ETH/USDC pair is used

```
from pyperp import constants

receipt = trader.open_position("ETHUSDC",constants.Side.SHORT.value,100,2,0,{"GasPrice":<gas price>, "GasLimit":<gas limit>})
print(receipt)
```

the open_position() function takes the following parameters:
1. The pair: the pair has to chosen from the available pairs in `AvailableAmms` dict in `constants.py` file
2. side: Has to be either constants.Side.LONG.value (0) or constants.Side.SHORT.value (1) 
3. quote_asset_amount
4. leverage
5. base_asset_amount_aimit


5.) get position information 

```
print(trader.get_personal_position_with_funding_payment("ETHUSDC"))
print(trader.get_unrealized_pnl("ETHUSDC",constants.PnlCalcOption.SPOT_PRICE))
```

The second parameter of the get_unrealized_pnl function is the PnlCalcOption which can be any of these three values : constants.PnlCalcOption.SPOT_PRICE(0), constants.PnlCalcOption.TWAP(1), constants.PnlCalcOption.ORACLE(2)

6.) add margin to position:

```
receipt = trader.add_margin("ETHUSDC", 10, {"GasPrice":<gas price>, "GasLimit":<gas limit>})
print(receipt)
```

7.) remove margin:

```
receipt = trader.remove_margin("ETHUSDC", 10, {"GasPrice":<gas price>, "GasLimit":<gas limit>})
print(receipt)
```

8.) close a position:

```
receipt = trader.close_position("ETHUSDC",0, {"GasPrice":<gas price>, "GasLimit":<gas limit>}) #the second parameter is quote asset amount limit
print(receipt)
```

9.) withdrawing USDC to L1

allow Layer 2 Bridge to use the USDC if not done already

```
reciept = trader.approve_l2_bridge_to_use_usdc({"GasPrice":<gas price>, "GasLimit":<gas limit>})
print(receipt)
```

then, withdraw USDC to L1 using `withdraw_usdc_to_ethereum()` function in `Trader` class

```
receipt = trader.withdraw_usdc_to_ethereum(100,{"GasPrice":<gas price>, "GasLimit":<gas limit>})
print(receipt)
```






