# Providers

Providers are objects that encapsulates trader account, RPC endpoints, contract ABIs and metadata.

V2 Curie is deployed in three different chains:

1. Arbitrum Rinkeby
2. Optimism Kovan
3. Optimism

A Provider class is defined for each of the chains

## ArbiturmRinkebyProvider

The provider class for Arbiturm Rinkeby chain

### Import 

```
from pyperp.providers import ArbitrumRinkebyProvider
```

### Properites

1. `api` : The `Web3.HTTPProvider` or `Web3.WebsocketProvider` object that interfaces with an RPC endpoint
2. `account`: The `eth_account.Account` object that manages keypair of trader wallet

### Methods

1. `load_meta` : 
    This function loads metadata of given contract. 

    **Arguments:**
    `contract_name`: The name of the contract whose metadata is to be loaded. Contract names are case-sensitive

    **Returns:**
    A dict object of the following format:
    ```
    {
        address: <CONTRACT_ADDRESS>
        abi: <CONTRACT_ABI>
    }
    ```

## OptimismKovanProvider

The provider class for Optimism Kovan chain

### Import 

```
from pyperp.providers import OptimismKovanProvider
```

### Properites

1. `api` : The `Web3.HTTPProvider` or `Web3.WebsocketProvider` object that interfaces with an RPC endpoint
2. `account`: The `eth_account.Account` object that manages keypair of trader wallet

### Methods

1. `load_meta` : 
    This function loads metadata of given contract. 

    **Arguments:**
    `contract_name`: The name of the contract whose metadata is to be loaded. Contract names are case-sensitive

    **Returns:**
    A dict object of the following format:
    ```
    {
        address: <CONTRACT_ADDRESS>
        abi: <CONTRACT_ABI>
    }
    ```

## Optimism

The provider class for Optimism chain

### Import 

```
from pyperp.providers import OptimismProvider
```

### Properites

1. `api` : The `Web3.HTTPProvider` or `Web3.WebsocketProvider` object that interfaces with an RPC endpoint
2. `account`: The `eth_account.Account` object that manages keypair of trader wallet

### Methods

1. `load_meta` : 
    This function loads metadata of given contract. 

    **Arguments:**
    `contract_name`: The name of the contract whose metadata is to be loaded. Contract names are case-sensitive

    **Returns:**
    A dict object of the following format:
    ```
    {
        address: <CONTRACT_ADDRESS>
        abi: <CONTRACT_ABI>
    }
    ```

