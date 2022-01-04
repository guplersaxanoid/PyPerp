# PyPerp

A python SDK for Perpetual Protocol. 

## Installation

From PyPi: 

`pip install pyperp`

## Documentation

The complete documentation will be added soon

## Example Code

This example code is written to demonstrate simple trading on Optimism Kovan.

### Create an ApiProvider object

```
from eth_account import Account
from pyperp.providers import OptimismKovanProvider

account = Account.from_key('<PRIVATE_KEY_HERE>')
provider = OptimismKovanProvider(
  '<RPC_ENDPOINT_URL>',
  account
)
```

### Approve Vault to use USDC

```
from pyperp.contracts import Vault
from pyperp.common.types import GasParams

gas_params = GasParams(
  gas=1000000,
  gas_price=100000
)

vault = Vault(provider)

receipt = vault.approve_vault_to_use_usdc(
  gas_params
)
```

### deposit USDC to vault


```
receipt = vault.deposit(
  vault.usdc.address,
  10000000000,
  gas_params
)
```

Vault.deposit() takes the following positional arguments:

token: contract address of collateral token

amount: amount of token to deposit

gas_params: GasParams object denoting gas paramateres.

### check how much collateral can be withdrawn

```
print(
  vault.get_free_collateral(
    account.address
  )
)
```

### withdraw from vault

```
receipt = vault.withdraw(
  vault.usdc.address,
  <AMOUNT_HERE>,
  gas_params
)
```

### open a position 


You can open a position for either vBTC or vETH. In this example we will open a position for vBTC

```
from pyperp.contracts import ClearingHouse
from pyperp.contracts.types import OpenPositionParams
from pyperp.commom.utils import getDeadline

clearing_house = ClearingHouse(provider)

params = OpenPositionParams(
  base_token = clearing_house.vbtc.address,
  is_base_to_quote = True,
  is_exact_input = True,
  amount = int(0.002*10**18),
  opposite_amount_bound = 0,
  deadline = getDeadline(120), #deadline is 120 secs from now
  sqrt_price_limit_x96 = 0
)

receipt = clearing_house.open_position(
  params, gas_params
)
```

### get account value 

```
print(
  clearing_house.get_account_value(account.address)
)
```

### Close Position 

```
from pyperp.contract.types import ClosePositionParams

params = ClosePositionParams(
  base_token=clearing_house.vbtc.address,
  sqrt_price_limit_x96=0,
  oppposite_amount_bound=0,
  deadline=getDeadline(120)
)

receipt = clearing_house.close_position(
  params, gas_params
)
```
