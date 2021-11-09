"""Trader class."""

from pyperp import constants
import json
from pyperp.MetaData import MetaData
from pyperp import utils
import pkgutil


class Trader:
    """Contains the trader wallets and functions for trading on perp."""

    def __init__(self, provider, l1wallet, l2wallet):
        """
        Arguments:
        provider: Provider object
        l1wallet: The layer 1 wallet of the trader
        l2wallet: The layer 2 wallet of the trader
        """
        self._layer1wallet = l1wallet
        self._layer2wallet = l2wallet
        self._provider = provider
        self.meta = MetaData(provider.testnet)

        clearing_house_addr = self.meta.get_l2_contract_address("ClearingHouse")
        clearing_house_abi = json.loads(
            pkgutil.get_data(__name__, "abi/ClearingHouse.json")
        )
        self.clearing_house = self._provider.l2.eth.contract(
            address=clearing_house_addr, abi=clearing_house_abi
        )

        clearing_house_viewer_addr = self.meta.get_l2_contract_address(
            "ClearingHouseViewer"
        )
        clearing_house_viewer_abi = json.loads(
            pkgutil.get_data(__name__, "abi/ClearingHouseViewer.json")
        )
        self.ch_viewer = self._provider.l2.eth.contract(
            address=clearing_house_viewer_addr, abi=clearing_house_viewer_abi
        )

    @property
    def layer1wallet(self):
        """Getter for layer 1 wallet."""
        return self._layer1wallet

    @layer1wallet.setter
    def layer1wallet(self, w):
        """Setter for layer 1 wallet."""
        self._layer1wallet = w

    @property
    def layer2wallet(self):
        """Getter for layer 2 wallet."""
        return self._layer2wallet

    @layer2wallet.setter
    def layer2wallet(self, w):
        """Setter for layer 2 wallet."""
        self._layer2wallet = w

    def l1_wallet_balance(self):
        """Return balance of layer 1 wallet."""
        return self._provider.l1.eth.getBalance(self._layer1wallet.address)

    def l2_wallet_balance(self):
        """Return balance of layer 2 wallet."""
        return self._provider.l2.eth.getBalance(self._layer2wallet.address)

    def l1_usdc_balance(self):
        """Return USDC token balance of layer 1 wallet"""
        tether_token_abi = json.loads(
            pkgutil.get_data(__name__, "abi/TetherToken.json")
        )
        usdc_addr = self.meta.get_l1_ext_contract_address("usdc")
        layer1_usdc = self._provider.l1.eth.contract(
            address=usdc_addr, abi=tether_token_abi
        )
        return layer1_usdc.functions.balanceOf(
            self._layer1wallet.address).call()

    def l2_usdc_balance(self):
        """Return USDC token balance of layer 2 wallet"""
        tether_token_abi = json.loads(
            pkgutil.get_data(__name__, "abi/TetherToken.json")
        )
        usdc_addr = self.meta.get_l2_ext_contract_address("usdc")
        layer2_usdc = self._provider.l2.eth.contract(
            address=usdc_addr, abi=tether_token_abi
        )
        return layer2_usdc.functions.balanceOf(
            self._layer2wallet.address).call()

    def approve_l1_bridge_to_use_usdc(self, gas_params):
        """
        Approve RootBridge to use USDC in layer 1 wallet.

        Arguments:
        gas_params -- a dict with GasPrice & GasLimit (GWEI)
        """
        tether_token_abi = json.loads(
            pkgutil.get_data(__name__, "abi/TetherToken.json")
        )
        usdc_addr = self.meta.get_l1_ext_contract_address("usdc")
        layer1_bridge_addr = self.meta.get_l1_contract_address("RootBridge")
        layer1_usdc = self._provider.l1.eth.contract(
            address=usdc_addr, abi=tether_token_abi
        )
        nonce = self._provider.l1.eth.get_transaction_count(
            self._layer1wallet.address
        )
        approve_tx = layer1_usdc.functions.approve(
            layer1_bridge_addr, constants.max_u_int256
        ).buildTransaction(
            {
                "nonce": nonce,
                "gas": gas_params["GasLimit"],
                "gasPrice": gas_params["GasPrice"],
            }
        )
        signed_tx = self._provider.l1.eth.account.sign_transaction(
            approve_tx, private_key=self._layer1wallet.key
        )

        approve_tx_hash = self._provider.l1.eth.send_raw_transaction(
            signed_tx.rawTransaction
        )
        receipt = self._provider.l1.eth.wait_for_transaction_receipt(
            approve_tx_hash
        )
        return receipt

    def deposit_usdc_to_xdai(self, amount, gas_params):
        """
        Move USDC from layer 1 to layer 2.

        Arguments:
        amount -- amount to be transferred in USDC
        gas_params -- a dict with GasPrice & GasLimit (GWEI)
        """
        root_bridge_abi = json.loads(
            pkgutil.get_data(__name__, "abi/RootBridge.json")
        )
        usdc_addr = self.meta.get_l1_ext_contract_address("usdc")
        layer1_bridge_addr = self.meta.get_l1_contract_address("RootBridge")
        layer1_bridge = self._provider.l1.eth.contract(
            address=layer1_bridge_addr, abi=root_bridge_abi
        )
        nonce = self._provider.l1.eth.get_transaction_count(
            self._layer1wallet.address
        )
        transfer_tx = layer1_bridge.functions.erc20Transfer(
            usdc_addr,
            self._layer1wallet.address,
            {"d": utils.parse_units(amount, 18)}
        ).buildTransaction(
            {
                "nonce": nonce,
                "gas": gas_params["GasLimit"],
                "gasPrice": gas_params["GasPrice"],
            }
        )
        signed_tx = self._provider.l1.eth.account.sign_transaction(
            transfer_tx, private_key=self._layer1wallet.key
        )
        transfer_tx_hash = self._provider.l1.eth.send_raw_transaction(
            signed_tx.rawTransaction
        )
        receipt = self._provider.l1.eth.wait_for_transaction_receipt(
            transfer_tx_hash
        )
        return receipt

    def approve_l2_bridge_to_use_usdc(self, gas_params):
        """
        Approve ClientBridge to use USDC in trader's layer 2 wallet.

        Arguments:
        gas_params -- a dict with GasPrice & GasLimit (GWEI)
        """
        tether_token_abi = json.loads(
            pkgutil.get_data(__name__, "abi/TetherToken.json")
        )
        usdc_addr = self.meta.get_l2_ext_contract_address("usdc")
        layer2_bridge_addr = self.meta.get_l2_contract_address("ClientBridge")
        layer2_usdc = self._provider.l2.eth.contract(
            address=usdc_addr, abi=tether_token_abi
        )
        nonce = self._provider.l2.eth.get_transaction_count(
            self._layer2wallet.address
        )
        approve_tx = layer2_usdc.functions.approve(
            layer2_bridge_addr, constants.max_u_int256
        ).buildTransaction(
            {
                "nonce": nonce,
                "gas": gas_params["GasLimit"],
                "gasPrice": gas_params["GasPrice"],
            }
        )
        signed_tx = self._provider.l2.eth.account.sign_transaction(
            approve_tx, private_key=self._layer2wallet.key
        )

        approve_tx_hash = self._provider.l2.eth.send_raw_transaction(
            signed_tx.rawTransaction
        )
        receipt = self._provider.l2.eth.wait_for_transaction_receipt(
            approve_tx_hash
        )
        return receipt

    def withdraw_usdc_to_ethereum(self, amount, gas_params):
        """
        Withdraw USDC from layer 2 to layer 1.

        Arguments:
        amount -- amount in USDC to be withdrawn
        gas_params -- a dict with GasPrice & GasLimit (GWEI)
        """
        tether_token_abi = json.loads(
            pkgutil.get_data(__name__, "abi/TetherToken.json")
        )
        client_bridge_abi = json.loads(
            pkgutil.get_data(__name__, "abi/ClientBridge.json")
        )
        usdc_addr = self.meta.get_l2_ext_contract_address("usdc")
        layer2_bridge_addr = self.meta.get_l2_contract_address("ClientBridge")
        layer2_usdc = self._provider.l2.eth.contract(
            address=usdc_addr, abi=tether_token_abi
        )
        layer2_bridge = self._provider.l2.eth.contract(
            address=layer2_bridge_addr, abi=client_bridge_abi
        )
        nonce = self._provider.l2.eth.get_transaction_count(
            self._layer2wallet.address
        )
        transfer_tx = layer2_bridge.functions.erc20Transfer(
            layer2_usdc.address,
            self._layer2wallet.address,
            {"d": utils.parse_units(amount, constants.DEFAULT_DECIMALS)},
        ).buildTransaction(
            {
                "nonce": nonce,
                "gas": gas_params["GasLimit"],
                "gasPrice": gas_params["GasPrice"]
            }
        )
        signed_tx = self._provider.l2.eth.account.sign_transaction(
            transfer_tx, private_key=self._layer2wallet.key
        )
        transfer_tx_hash = self._provider.l2.eth.send_raw_transaction(
            signed_tx.rawTransaction
        )
        receipt = self._provider.l2.eth.wait_for_transaction_receipt(
            transfer_tx_hash
        )
        return receipt

    def approve_clearing_house_to_use_usdc(self, gas_params):
        """
        Approve ClearingHouse to use USDC from trader layer 2 wallet.

        Arguments:
        gas_params -- a dict with GasPrice & GasLimit (GWEI)
        """
        tether_token_abi = json.loads(
            pkgutil.get_data(__name__, "abi/TetherToken.json")
        )
        usdc_addr = self.meta.get_l2_ext_contract_address("usdc")
        clearing_house_addr = self.meta.get_l2_contract_address("ClearingHouse")
        layer2_usdc = self._provider.l2.eth.contract(
            address=usdc_addr, abi=tether_token_abi
        )
        nonce = self._provider.l2.eth.get_transaction_count(
            self._layer2wallet.address
        )
        tx = layer2_usdc.functions.approve(
            clearing_house_addr, constants.max_u_int256
        ).buildTransaction(
            {
                "nonce": nonce,
                "gas": gas_params["GasLimit"],
                "gasPrice": gas_params["GasPrice"]
            }
        )
        signed_tx = self._provider.l2.eth.account.sign_transaction(
            tx, private_key=self._layer2wallet.key
        )
        tx_hash = self._provider.l2.eth.send_raw_transaction(
            signed_tx.rawTransaction
        )
        receipt = self._provider.l2.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

    def open_position(
        self, pair, side, quote_asset_amount,
        leverage, base_asset_amount_limit, gas_params
    ):
        """Open a positions in the given pair.

        Arguments:
        pair -- A string value representing a pair
        side -- 1 for short position or 0 for long position
        quote_asset_amount -- A non-zero quote asset amount value
        leverage -- A leverage value between 0 and 10
        base_asset_amount_limit -- base asset amount limit after slippage
        gas_params -- a dict with GasPrice & GasLimit (GWEI)
        """
        if side != 0 and side != 1:
            raise ValueError("side must be either 0 or 1")

        if quote_asset_amount <= 0:
            raise ValueError("quote_asset_amount must be greater than 0")

        if leverage <= 0 or leverage > 10:
            raise ValueError("leverage must be in the range (0,10]")

        amm = utils.get_amm(pair, self._provider)

        nonce = self._provider.l2.eth.get_transaction_count(
            self._layer2wallet.address
        )
        tx = self.clearing_house.functions.openPosition(
            amm.address,
            side,
            {"d": utils.parse_units(quote_asset_amount, 18)},
            {"d": utils.parse_units(leverage, 18)},
            {"d": base_asset_amount_limit},
        ).buildTransaction(
            {
                "nonce": nonce,
                "gas": gas_params["GasLimit"],
                "gasPrice": gas_params["GasPrice"]
            }
        )
        signed_tx = self._provider.l2.eth.account.sign_transaction(
            tx, private_key=self._layer2wallet.key
        )
        tx_hash = self._provider.l2.eth.send_raw_transaction(
            signed_tx.rawTransaction
        )
        receipt = self._provider.l2.eth.wait_for_transaction_receipt(tx_hash)
        return receipt

    def close_position(self, pair, quote_asset_amount_limit, gas_params):
        """
        Close a position in the given pair.

        Arguments:
        pair -- A string value representing a pair.
        quote_asset_amount_limit -- quote asset amount limit after slippage
        gas_params -- a dict with GasPrice & GasLimit (GWEI)
        """
        amm = utils.get_amm(pair, self._provider)

        nonce = self._provider.l2.eth.get_transaction_count(
            self._layer2wallet.address
        )


        tx = self.clearing_house.functions.closePosition(
            amm.address,
            {"d": utils.parse_units(quote_asset_amount_limit)},
        ).buildTransaction(
            {
                "nonce": nonce,
                "gas": gas_params["GasLimit"],
                "gasPrice": gas_params["GasPrice"]
            }
        )
        signed_tx = self._provider.l2.eth.account.sign_transaction(
            tx, private_key=self._layer2wallet.key
        )
        tx_hash = self._provider.l2.eth.send_raw_transaction(
            signed_tx.rawTransaction
        )
        receipt = self._provider.l2.eth.wait_for_transaction_receipt(
            tx_hash
        )
        return receipt

    def get_personal_position_with_funding_payment(self, pair, trader=None):
        """
        Return Position data.

        Arguments:
        pair -- A string value representing a pair.
        trader -- wallet address of the trader.
        """
        amm = utils.get_amm(pair, self._provider)

        if trader is None:
            trader = self._layer2wallet.address

        position = (
            self.ch_viewer.functions.getPersonalPositionWithFundingPayment(
                amm.address, trader
            ).call()
        )
        return {
            "size": position[0][0],
            "margin": position[1][0],
            "openNotional": position[2][0],
            "lastUpdatedCumulativePremiumFraction": position[3][0],
            "liquidityHistoryIndex": position[4],
            "blockNumber": position[5],
        }

    def get_unrealized_pnl(self, pair, pnl_calc_option, trader=None):
        """
        Return unrealized pnl value for a position.

        Arguments:
        pair -- A string value representing a pair.
        pnl_calc_option -- PnlCalcOption.SPOT_PRICE or PnlCalcOption.TWAP
        trader -- wallet address of the trader.
        """
        amm = utils.get_amm(pair, self._provider)
        if trader is None:
            trader = self._layer2wallet.address

        return self.ch_viewer.functions.getUnrealizedPnl(
            amm.address, trader, pnl_calc_option.value
        ).call()[0]

    def get_entry_price(self, pair):
        """
        Return the entry price for the given amm.

        Arguments:
        pair -- A string value representing a pair.
        """
        position = self.get_personal_position_with_funding_payment(pair)
        open_notional = utils.format_units(position["open_notional"])
        size = utils.format_units(position["size"])

        entry_price = abs(open_notional / size)
        return entry_price

    def add_margin(self, pair, margin, gas_params):
        """
        Add margin to an existing position.

        Arguments:
        pair -- A string value representing a pair.
        margin -- Margin amount to be added
        gas_params -- a dict with GasPrice & GasLimit (GWEI)
        """
        amm = utils.get_amm(pair, self._provider)

        nonce = self._provider.l2.eth.get_transaction_count(
            self._layer2wallet.address
        )
        tx = self.clearing_house.functions.addMargin(
            amm.address, {"d": utils.parse_units(margin, 18)}
        ).buildTransaction(
            {
                "nonce": nonce,
                "gas": gas_params["GasLimit"],
                "gasPrice": gas_params["GasPrice"]
            }
        )
        signed_tx = self._provider.l2.eth.account.sign_transaction(
            tx, private_key=self._layer2wallet.key
        )
        tx_hash = self._provider.l2.eth.send_raw_transaction(
            signed_tx.rawTransaction
        )
        receipt = self._provider.l2.eth.wait_for_transaction_receipt(
            tx_hash
        )
        return receipt

    def remove_margin(self, pair, margin, gas_params):
        """
        Remove margin from an existing position.

        Arguments:
        pair -- A string value representing a pair.
        margin -- Margin amouunt to be removed
        gas_params -- a dict with GasPrice & GasLimit (GWEI)
        """
        amm = utils.get_amm(pair, self._provider)

        nonce = self._provider.l2.eth.get_transaction_count(
            self._layer2wallet.address
        )
        tx = self.clearing_house.functions.removeMargin(
            amm.address, {"d": utils.parse_units(margin, 18)}
        ).buildTransaction(
            {
                "nonce": nonce,
                "gas": gas_params["GasLimit"],
                "gasPrice": gas_params["GasPrice"]
            }
        )
        signed_tx = self._provider.l2.eth.account.sign_transaction(
            tx, private_key=self._layer2wallet.key
        )
        tx_hash = self._provider.l2.eth.send_raw_transaction(
            signed_tx.rawTransaction
        )
        receipt = self._provider.l2.eth.wait_for_transaction_receipt(
            tx_hash
        )
        return receipt

    def settle_position(self, pair, gas_params):
        """
        Settle all positions for an amm.

        Arguments:
        pair -- A string value representing a pair.
        gas_params -- a dict with GasPrice & GasLimit (GWEI)
        """
        amm = utils.get_amm(pair, self._provider)

        nonce = self._provider.l2.eth.get_transaction_count(
            self._layer2wallet.address
        )
        tx = self.clearing_house.functions.settlePosition(
            amm.address
        ).buildTransaction(
            {
                "nonce": nonce,
                "gas": gas_params["GasLimit"],
                "gasPrice": gas_params["GasPrice"]
            }
        )
        signed_tx = self._provider.l2.eth.account.sign_transaction(
            tx, private_key=self._layer2wallet.key
        )
        tx_hash = self._provider.l2.eth.send_raw_transaction(
            signed_tx.rawTransaction
        )
        receipt = self._provider.l2.eth.wait_for_transaction_receipt(
            tx_hash
        )
        return receipt

    def liquidate(self, pair, gas_params):
        """
        Liquidate a position.

        Arguments:
        pair -- A string value representing a pair.
        gas_params -- a dict with GasPrice & GasLimit (GWEI)
        """
        amm = utils.get_amm(pair, self._provider)

        nonce = self._provider.l2.eth.get_transaction_count(
            self._layer2wallet.address
        )
        tx = self.clearing_house.functions.liquidate(
            amm.address, self._layer2wallet.address
        ).buildTransaction(
            {
                "nonce": nonce,
                "gas": gas_params["GasLimit"],
                "gasPrice": gas_params["GasPrice"]
            }
        )
        signed_tx = self._provider.l2.eth.account.sign_transaction(
            tx, private_key=self._layer2wallet.key
        )
        tx_hash = self._provider.l2.eth.send_raw_transaction(
            signed_tx.rawTransaction
        )
        receipt = self._provider.l2.eth.wait_for_transaction_receipt(
            tx_hash
        )
        return receipt
