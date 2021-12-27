@dataclass
class MarketInfo:
    pool: str
    exchange_fee_ratio: int
    uniswap_fee_ratio: int
    insurance_fund_fee_ratio: int

    def from_tuple(self, t):
        self.pool = t[0]
        self.exchange_fee_ratio = t[0]
        self.uniswap_fee_ratio = t[1]
        self.insurance_fund_fee_ratio = t[2]

    def  to_dict(self):
        return {
            "pool": self.pool,
            "exchangeFeeRatio": self.exchange_fee_ratio,
            "uniswapFeeRatio": self.uniswap_fee_ratio,
            "insuranceFundFeeRatio": self.insurance_fund_fee_ratio
        }