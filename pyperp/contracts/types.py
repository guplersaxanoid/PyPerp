from dataclasses import dataclass

@dataclass
class OpenPositionParams:
    base_token: str
    is_base_to_quote: bool
    is_exact_amount: bool
    amount: int
    opposite_amount_bound: int
    deadline: int
    sqrt_price_limit_x96: int
    referral_code: str

    def __post__init__(self):
        if referral_code is None:
            referral_code = 0

    def to_dict(self):
        return {
            'base_token': self.baseToken,
            'isBaseToQuote': self.is_base_to_quote,
            'isExactAmount': self.is_exact_amount,
            'amount': self.amount,
            'oppositeAmountBound': self.opposite_amount_bound,
            'deadline': self.deadline,
            'sqrtPriceLimitX96': self.sqrt_price_limit_x96,
            'referral_code': seld.referral_code
        }

@dataclass
class ClosePositionParams:
    base_token: str
    sqrt_price_limit_x96: int
    opposite_amount_bound: int
    deadline: int
    referral_code: str

    def __post__init__(self):
        if self.referral_code is None:
            self.referral_code = 0

    def to_dict(self):
        return {
            "baseToken": self.base_token,
            "sqrtPriceLimitX96": self.sqrt_price_limit_x96,
            "oppositeAmountBound": self.opposite_amount_bound,
            "deadline": self.deadline,
            "referralCode": self.referral_code
        }

@dataclass
class AddLiquidityParams:
    base_token: str
    base: int
    quote: int
    lower_tick: int
    upper_tick: int
    min_base: int
    min_quote: int
    use_taker_balance: bool
    deadline: bool

    def to_dict(self):
        return {
            'baseToken': self.base_token,
            'base': self.base,
            'quote': self.quote,
            'lowerTick': self.lowerTick,
            'upperTick': self.upperTick,
            'minBase': self.min_base,
            'minQuote': self.minQuote,
            'useTakerBalance': self.useTakerBalance,
            'deadline': self.deadline
        }

@dataclass
class RemoveLiquidityParams:
    base_token: str,
    lower_tick: int,
    upper_tick: int,
    liquidity: int,
    min_base: int,
    min_quote: int,
    deadline: int

    def to_dict(self):
        return {
            'baseToken': self.base_token,
            'lowerTick': self.lowerTick,
            'upperTick': self.upperTick,
            'liquidity': self.liquidity,
            'minBase': self.min_base,
            'minQuote': self.minQuote,
            'deadline': self.deadline
        }

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
