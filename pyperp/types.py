from typing import Optional

@dataclass
class GasParams:
    gas: int
    gas_price: Optional[int]
    max_fee_per_gas: Optional[int]
    max_priority_fee_per_gas: Optional[int]

    def toDict(self):
        return {
            'gas': self.gas,
            'gasPrice': self.gasPrice,
            'maxFeePerGas': self.max_fee_per_gas,
            'maxPriorityFeePerGas': self.max_priority_fee_per_gas
        }