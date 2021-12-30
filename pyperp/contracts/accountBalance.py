from pyperp.providers import ApiProvider
from pyperp.contracts.types import AccountMarketInfo
from web3 import Web3
import logging 

class AccountBalance:
    def __init__(self, provider: ApiProvider):
        self._provider = provider
        self.logger = logging.getLogger("AccountBalance")

        self.logger.info("Loading AccountBalance contract")
        _account_balance_meta = self._provider.load_meta("AccountBalance")
        self._account_balance = self._provider._api.eth.contract(
            address=_account_balance_meta["address"],
            abi=_account_balance_meta["abi"]
        )
        self.logger.info("AccountBalance contract loaded")

    def get_base_tokens(
        self,
        trader: str
    ):
        assert(
            Web3.isAddress(trader),
            f"Trader address {trader} must be a valid address"
        )
        return self._account_balance.functions.getBaseTokens(
            trader
        ).call()

    def get_account_info(
        self,
        trader: str,
        base_token: str
    ):
        assert(
            Web3.isAddress(trader),
            f"Trader address {trader} must be a valid address"
        )
        assert(
            Web3.isAddress(base_token),
            f"Base Token address {base_token} must be a valid address"
        )
        resp = self._account_balance.functions.getAccountInfo(
            trader,
            base_token
        ).call()

        return AccountMarketInfo(*resp)

    def get_taker_open_notional(
        self,
        trader: str,
        base_token: str
    ):
        assert(
            Web3.isAddress(trader),
            f"Trader address {trader} must be a valid address"
        )
        assert(
            Web3.isAddress(base_token),
            f"Base Token address {base_token} must be a valid address"
        )
        return self._account_balance.functions.getTakerOpenNotional(
            trader,
            base_token
        ).call()
        
    def get_total_open_notional(
        self,
        trader: str,
        base_token: str
    ):
        assert(
            Web3.isAddress(trader),
            f"Trader address {trader} must be a valid address"
        )
        assert(
            Web3.isAddress(base_token),
            f"Base Token address {base_token} must be a valid address"
        )
        return self._account_balance.functions.getTotalOpenNotional(
            trader,
            base_token
        ).call()

    def get_total_debt_value(
        self,
        trader: str,
    ):
        assert(
            Web3.isAddress(trader),
            f"Trader address {trader} must be a valid address"
        )
        return self._account_balance.functions.getTotalDebtValue(
            trader
        ).call()

    def get_marginal_requirement_for_liquidation(
        self,
        trader: str
    ):
        assert(
            Web3.isAddress(trader),
            f"Trader address {trader} must be a valid address"
        )
        return self._account_balance.functions.getMarginRequirementForLiquidation(
            trader,
        ).call()

    def get_pnl_and_pending_fee(
        self,
        trader: str,
    ):
        assert(
            Web3.isAddress(trader),
            f"Trader address {trader} must be a valid address"
        )
        resp = self._account_balance.functions.getPnlAndPendingFee(
            trader
        ).call()
        return {
            'owed_realized_pnl': resp[0],
            'unrealized_pnl': resp[1],
            'pending_fee': resp[2]
        }

    def has_order(
        self,
        trader: str
    ):
        assert(
            Web3.isAddress(trader),
            f"Trader address {trader} must be a valid address"
        )
        return self._account_balance.functions.hasOrder(
            trader
        ).call()

    #TODO: update ABI
    def has_order_in_open_or_closed_market(
        self,
        trader: str
    ):
        assert(
            Web3.isAddress(trader),
            f"Trader address {trader} must be a valid address"
        )
        return self._account_balance.functions.hasOrderInOpenOrClosedMarket(
            trader
        ).call()

    def get_base(
        self,
        trader: str,
        base_token: str
    ):
        assert(
            Web3.isAddress(trader),
            f"Trader address {trader} must be a valid address"
        )
        assert(
            Web3.isAddress(base_token),
            f"Base Token address {base_token} must be a valid address"
        )
        return self._account_balance.functions.getBase(
            trader,
            base_token
        ).call()

    def get_quote(
        self,
        trader: str,
        base_token: str
    ):
        assert(
            Web3.isAddress(trader),
            f"Trader address {trader} must be a valid address"
        )
        assert(
            Web3.isAddress(base_token),
            f"Base Token address {base_token} must be a valid address"
        )
        return self._account_balance.functions.getQuote(
            trader,
            base_token
        ).call()

    def get_taker_position_size(
        self,
        trader: str,
        base_token: str
    ):
        assert(
            Web3.isAddress(trader),
            f"Trader address {trader} must be a valid address"
        )
        assert(
            Web3.isAddress(base_token),
            f"Base Token address {base_token} must be a valid address"
        )
        return self._account_balance.functions.getTakerPositionSize(
            trader,
            base_token
        ).call()

    def get_total_position_size(
        self,
        trader: str,
        base_token: str
    ):
        assert(
            Web3.isAddress(trader),
            f"Trader address {trader} must be a valid address"
        )
        assert(
            Web3.isAddress(base_token),
            f"Base Token address {base_token} must be a valid address"
        )
        return self._account_balance.functions.getTotalPositionSize(
            trader,
            base_token
        ).call()

    def get_total_position_value(
        self,
        trader: str,
        base_token: str
    ):
        assert(
            Web3.isAddress(trader),
            f"Trader address {trader} must be a valid address"
        )
        assert(
            Web3.isAddress(base_token),
            f"Base Token address {base_token} must be a valid address"
        )
        return self._account_balance.functions.getTotalPositionValue(
            trader,
            base_token
        ).call()

    def get_total_abs_position_value(
        self,
        trader: str
    ):
        assert(
            Web3.isAddress(trader),
            f"Trader address {trader} must be a valid address"
        )
        return self._account_balance.functions.getTotalAbsPositionValue(
            trader
        ).call()

    #TODO: update ABI
    def settle_pnl_in_closed_market(
        self,
        trader: str,
        base_token: str
    ):
        assert(
            Web3.isAddress(trader),
            f"Trader address {trader} must be a valid address"
        )
        assert(
            Web3.isAddress(base_token),
            f"Base Token address {base_token} must be a valid address"
        )
        return self._account_balance.functions.settlePnlInClosedMarket(
            trader,
            base_token
        ).call()