from dataclasses import dataclass

@dataclass
class OpenPositionParam:
    base_token: str
    is_base_to_quote: bool
    is_exact_amount: bool
    amount: int
    opposite_amount_bound: int
    deadline: int
    sqrt_price_limit_x96: int
    referral_code: str

@dataclass
class ClosePositionParams:
    base_token: str
    sqrt_price_limit_x96: int
    opposite_amount_boundL: int
    deadline: int
    referral_code: str

