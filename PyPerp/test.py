from web3 import Web3
from web3.middleware import geth_poa_middleware
from Providers import Providers
from Trader import Trader
from Faucets import getUsdcL1
import constants
import Amm

l2provider = Web3(Web3.HTTPProvider("https://rpc.xdaichain.com/"))
l1provider = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/8649cd5402194cab8949b3eabe21d6ff"))
#l1provider.middleware_onion.inject(geth_poa_middleware, layer=0)
provider = Providers(l1provider,l2provider,True)

l1wallet = provider.l1.eth.account.privateKeyToAccount("bfdad91bad521586103aea91601e95a8a87428b9a61db9d8cf31c7c3d45f3025")
l2wallet = provider.l2.eth.account.privateKeyToAccount("bfdad91bad521586103aea91601e95a8a87428b9a61db9d8cf31c7c3d45f3025")

trader = Trader(provider, l1wallet, l2wallet)

#receipt = trader.approveL1BridgetoUseUSDC()
#receipt = trader.depositUsdcToxDai(100)
#print(trader.approveClearingHouseToUseUSDC())
#print(trader.openPosition("ETHUSDC",constants.Side.SHORT.value,100,2,0))
#print(trader.getPersonalPositionWithFundingPayment("ETHUSDC"))
#print(trader.getUnrealizedPnl("ETHUSDC",constants.PnlCalcOption.SPOT_PRICE))
#print(trader.getEntryPrice("ETHUSDC"))
#print(trader.closePosition("ETHUSDC",0))
#print(trader.approveL2BridgeToUseUSDC())
#print(trader.withdrawUsdcToEthereum(100))
#print(Amm.getAmmInfo(provider))
#print(trader.l1WalletBalance())
#print(trader.l2WalletBalance())
#print(trader.addMargin("ETHUSDC", 10))
#print(trader.getPersonalPositionWithFundingPayment("ETHUSDC"))
#print(trader.removeMargin("ETHUSDC", 10))
#print(trader.getPersonalPositionWithFundingPayment("ETHUSDC"))
print(trader.closePosition("ETHUSDC",0))
print(trader.getPersonalPositionWithFundingPayment("ETHUSDC"))

#todo: 
#1.) addMargin()
#2.) removeMargin()
#3.) settlePosition()
#4.)  liquidate()
#5.) better gas strategy
#6.) get amm info
#7.) write tests
