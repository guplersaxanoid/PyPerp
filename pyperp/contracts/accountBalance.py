'''AccountBalance Class'''

from pyperp.providers import ApiProvider
from pyperp.contracts.types import AccountMarketInfo
from web3 import Web3
import logging 

class AccountBalance:
    '''
    Interface with AccountBalance contract.
    '''
    def __init__(self, provider: ApiProvider):
        '''
        Intialize Provider.
        Argument:
        provider - An object of class derived from ApiProvider.
        '''
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
        '''
        Get base tokens owned by trader.
        Arguments:
        trader - wallet address of trader
        Returns a list of base token addresses
        '''
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
        '''
        Get Account Info of trader for a base token;
        Arguments:
        trader - wallet address of trader
        base_token - contract address of base token
        Returns an AccountMarketInfo object
        '''
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
        '''
        Get Taker Open Notional value
        Arguments:
        trader - wallet address of trader
        base_token - contract address of base token
        Returns taker open notional value
        '''
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
        '''
        Get Total Open Notional value
        Arguments:
        trader - wallet address of trader
        base_token - contract address of base token
        Returns total open notional value
        '''
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
        '''
        Get total debt value
        Arguments:
        trader - wallet address of trader
        Returns total debt value
        '''
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
        '''
        Get marginal requirement for liquidation
        Arguments:
        trader - wallet address of trader
        Returns marginal requirement for liquidation
        '''
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
        '''
        Get Pnl value and Pending fee
        Arguments:
        trader - wallet address of trader
        Returns a dict with the followig keys:
        owed_realized_pnl - Owed Realized Pnl value
        unrealized_pnl - Unrealized pnl value
        pending_fee - Pending fee
        '''
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
        '''
        Check if a trader has any orders
        Arguments:
        trader - wallet address of trader
        Returns:
        True - if trader has order
        False - if trader doesn't have any order
        '''
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
        '''
        Check if a trader has any orders in open or closed markets
        Arguments:
        trader - wallet address of trader
        Returns:
        True - if trader has order
        False - if trader doesn't have any order
        '''
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
        '''
        Get position size of a base token in terms of base
        Arguments:
        trader - wallet address of trader
        base_token - address of base token
        '''
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
        '''
        Get position size of a base token in terms of quote
        Arguments:
        trader - wallet address of trader
        base_token - address of base token
        '''
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
        '''
        Get taker position size of a base token
        Arguments:
        trader - wallet address of trader
        base_token - address of base token
        '''
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
        '''
        Get total position size of a base token
        Arguments:
        trader - wallet address of trader
        base_token - address of base token
        '''
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
        '''
        Get total position value of a base token
        Arguments:
        trader - wallet address of trader
        base_token - address of base token
        '''
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
        '''
        Get total absolute position value
        Arguments:
        trader - wallet address of trader
        '''      
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
        '''
        Settle PNL in closed market
        Arguments:
        trader - wallet address of trader
        base_token - address of base token 
        '''
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