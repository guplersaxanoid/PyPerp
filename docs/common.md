# common

Contains types and utility functions

## types

### GasParams

This is a dataclass used to define gas parameters in transactions

#### Importing

```
from pyperp.common.types import GasParams
```

#### Fields

`gas`: gas value. Defaults to None
`gas_price`: gasPrice. Defaults to None
`maxFeePerGas`: maxFeePerGas. Defaults to None
`maxPriorityFeePerGas`: maxProrityFeePerGas. Defaults to None

## utils

### getDeadline

#### Importing

```
from pyperp.common.utils import getDeadline
```

A function to get dealine in UNIX time. It takes number of seconds as argument and returns UNIX time at given number of seconds later from the time of function call

**Arguments:**

`expiry_seconds`: Number of seconds to add to the deadline from the time of function call
