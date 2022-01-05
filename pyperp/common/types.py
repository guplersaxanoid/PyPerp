from dataclasses import dataclass


@dataclass
class GasParams:
    gas: int = None
    gas_price: int = None
    max_fee_per_gas: int = None
    max_priority_fee_per_gas: int = None

    def to_dict(self):
        gas_params = {}
        if self.gas is not None:
            gas_params["gas"] = self.gas
        if self.gas_price is not None:
            gas_params["gasPrice"] = self.gas_price
        if self.max_fee_per_gas is not None:
            gas_params["maxFeePerGas"] = self.max_fee_per_gas
        if self.max_priority_fee_per_gas is not None:
            gas_params["maxPriorityFeePerGas"] = self.max_priority_fee_per_gas
        return gas_params
