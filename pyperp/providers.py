"""Contain the Providers class."""


class Providers:
    """Pack layer 1 and layer 2 providers in a single object."""

    def __init__(self, l1, l2, testnet: bool):
        """
        Arguments:
        l1 -- Layer 1 provider. Can be HTTP or IPC provider
        l2 -- Layer 2 provider. Can be HTTP or IPC provider
        testnet -- True if testnet is being used. False Otherwise.
        """
        self.testnet = testnet
        self.l1 = l1
        self.l2 = l2
