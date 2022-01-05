from dataclasses import dataclass
from hexbytes import HexBytes


@dataclass
class OpenPositionParams:
    base_token: str
    is_base_to_quote: bool
    is_exact_input: bool
    amount: int
    opposite_amount_bound: int
    deadline: int
    sqrt_price_limit_x96: int
    referral_code: HexBytes = HexBytes(0)

    def to_dict(self):
        return {
            'baseToken': self.base_token,
            'isBaseToQuote': self.is_base_to_quote,
            'isExactInput': self.is_exact_input,
            'amount': self.amount,
            'oppositeAmountBound': self.opposite_amount_bound,
            'deadline': self.deadline,
            'sqrtPriceLimitX96': self.sqrt_price_limit_x96,
            'referralCode': self.referral_code
        }


@dataclass
class ClosePositionParams:
    base_token: str
    sqrt_price_limit_x96: int
    opposite_amount_bound: int
    deadline: int
    referral_code: HexBytes = HexBytes(0)

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
            'lowerTick': self.lower_tick,
            'upperTick': self.upper_tick,
            'minBase': self.min_base,
            'minQuote': self.min_quote,
            'useTakerBalance': self.use_taker_balance,
            'deadline': self.deadline
        }


@dataclass
class RemoveLiquidityParams:
    base_token: str
    lower_tick: int
    upper_tick: int
    liquidity: int
    min_base: int
    min_quote: int
    deadline: int

    def to_dict(self):
        return {
            'baseToken': self.base_token,
            'lowerTick': self.lower_tick,
            'upperTick': self.upper_tick,
            'liquidity': self.liquidity,
            'minBase': self.min_base,
            'minQuote': self.min_quote,
            'deadline': self.deadline
        }


@dataclass
class MarketInfo:
    pool: str
    exchange_fee_ratio: int
    uniswap_fee_ratio: int
    insurance_fund_fee_ratio: int

    def to_dict(self):
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
        # TODO: implement field looping
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
            'baseDebt': self.base_debt,
            'quoteDebt': self.quote_debt
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


@dataclass
class AccountMarketInfo:
    taker_position_size: int
    taker_open_notional: int
    last_tw_premium_growth_global_x96: int
