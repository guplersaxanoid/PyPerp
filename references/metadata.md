# MetaData

### `Class MetaData(testnet)`

1. `testnet` : It is `True` if [`testnet metadata`](https://metadata.perp.exchange/staging.json) is to be fetched and `False` if [`mainnet metadata`](https://metadata.perp.exchange/production.json)is to be fetched.

### Attributes:

1. `MetaData.metadataStore`:  Returns the metadata url used in this object
2. `MetaData.meta`: Returns the metadata  json fetched from `metadataStore` url

### **Methods:**

#### `MetaData.getL1ContractAddress()`

returns the Layer 1 contract address of the given contract

**Parameters:**

1. `name`: The name of the contract. The names of the contract are referenced from the official metadata at [https://metadata.perp.exchange/staging.json](https://metadata.perp.exchange/staging.json) and [https://metadata.perp.exchange/production.json](https://metadata.perp.exchange/production.json)

**Returns:** The address of the contract

#### `MetaData.getL2ContractAddress()`

returns the Layer 2 contract address of the given contract

**Parameters:**

1. `name`: The name of the contract. The names of the contract are referenced from the official metadata at [https://metadata.perp.exchange/staging.json](https://metadata.perp.exchange/staging.json) and [https://metadata.perp.exchange/production.json](https://metadata.perp.exchange/production.json)

**Returns:** The address of the contract

#### `MetaData.getL1ExtContractAddress()`

returns the address of an external contract from Layer 1. 

**Parameters:**

1. `name`: The name of the contract. The names of the contract are referenced from the official metadata at [https://metadata.perp.exchange/staging.json](https://metadata.perp.exchange/staging.json) and [https://metadata.perp.exchange/production.json](https://metadata.perp.exchange/production.json)

**Returns:** The address of the contract

#### `MetaData.getL2ExtContractAddress()`

returns the address of an external contract from Layer 2. 

**Parameters:**

1. `name`: The name of the contract. The names of the contract are referenced from the official metadata at [https://metadata.perp.exchange/staging.json](https://metadata.perp.exchange/staging.json) and [https://metadata.perp.exchange/production.json](https://metadata.perp.exchange/production.json)

**Returns:** The address of the contract





