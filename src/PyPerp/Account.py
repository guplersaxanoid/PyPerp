#TO-DO:
#1.) implement all the functions
#2.) look for all the ways to import a wallet
#3.) create a seperate abstraction for wallet if necessary

class Account:
    def __init__(self,l1provider,l2provider,l1wallet,l2wallet):
        #todo : validate l1provider
        self._layer1provider = l1provider
        #todo : validate l2provider
        self._layer2provider = l2provider 
        #todo : validate l1wallet
        self._layer1wallet = l1wallet
        #todo : validate l2wallet
        self._layer2wallet = l2wallet

    @property
    def layer1provider(self):
        return self._layer1provider

    @layer1provider.setter
    def layer1provider(self, p):
        #todo : validate argument
        self._layer1provider = p

    @property
    def layer2provider(self):
        return self._layer2provider

    @layer2provider.setter
    def layer2provider(self, p):
        #todo : validate argument
        self._layer2provider = p

    @property
    def layer1wallet(self):
        return self._layer1wallet

    @layer1wallet.setter
    def layer1wallet(self, w):
        #todo : validate argument
        self._layer1wallet = w

    @property
    def layer2wallet(self):
        return self._layer2wallet

    @layer2wallet.setter
    def layer2wallet(self, w):
        #todo : validate argument
        self._layer2wallet = w

    