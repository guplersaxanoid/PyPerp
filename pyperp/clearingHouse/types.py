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
            "deadline": 
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