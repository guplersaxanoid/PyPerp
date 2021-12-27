
@dataclass
class OpenOrderInfo:
    liquidity: int
    lower_tick: int
    upper_tick: int
    last_fee_growth_inside_x96: int
    last_tw_premium_growth_inside_x96: int
    last_tw_premium_growth_below_x96: int
    last_tw_premium_div_by_sqrt_price_growth_inside_x96: int
    base_debt: int
    quote_debt: int

    def from_tuple(self, t):
        #TODO: implement field looping
        return
    
    def to_dict(self):
        return {
            'liquidity': self.liquidity,
            'lowerTick': self.lower_tick,
            'upperTick': self.upper_tick,
            'lastFeeGrowthInsideX96': self.last_fee_growth_inside_x96,
            'lastTwPremiumGrowthInsideX96': self.last_tw_premium_growth_inside_x96,
            'lastTwPremiumGrowthBelowX96': self.last_tw_premium_growth_below_x96,
            'lastTwPremiumDivBySqrtPriceGrowthInsideX96': self.last_tw_premium_div_by_sqrt_price_growth_inside_x96,
            'baseDebt': base_debt,
            'quoteDebt': quote_debt
        }

@dataclass
class FundingGrowth:
    tw_premium_x96: int
    tw_premium_div_by_sqrt_price_x96: int

    def to_dict(self):
        return {
            'twPremiumX96': self.tw_premium_x96,
            'twPremiumDivBySqrtPriceX96': self.tw_premium_div_by_sqrt_price_x96
        }
