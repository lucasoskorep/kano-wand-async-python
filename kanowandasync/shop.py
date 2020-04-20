from bleak import discover
from .wand import Wand

class Shop(object):
    """
    A scanner class to connect to wands
    """
    def __init__(self, shop_loop, wand_class=Wand, debug=False):
        """
        Create a new scanner

        Keyword Arguments:
            wand_class {class} -- Class to use when connecting to wand (default: {Wand})
            debug {bool} -- Print debug messages (default: {False})
        """
        self.shop_loop = shop_loop
        self.wand_class = wand_class
        self.debug = debug
        self._name = None
        self._prefix = None
        self._mac = None

    async def scan(self, prefix="Kano-Wand", mac=None, timeout=2.0, connect=False):
        """
        Scan for devices

        Keyword Arguments:
            name {str} -- Name of the device to scan for (default: {None})
            prefix {str} -- Prefix of name of device to scan for (default: {"Kano-Wand"})
            mac {str} -- MAC Address of the device to scan for (default: {None})
            timeout {float} -- Timeout before returning from scan (default: {1.0})
            connect {bool} -- Connect to the wands automatically (default: {False})

        Returns {Wand[]} -- Array of wand objects
        """

        if self.debug:
            print("Scanning for {} seconds...".format(timeout))
        try:
            prefix_check = not (prefix is None)
            mac_check = not (mac is None)
            assert prefix_check or mac_check
        except AssertionError as e:
            print("Either a name, prefix, or mac address must be provided to find a wand")
            raise e
        if prefix is not None:
            self._prefix = prefix
        elif mac is not None:
            self._mac = mac
        self.wands = []
        devices = await discover(timeout= timeout)
        print(devices)
        if self._prefix:
            devices = list(filter(lambda x : x.name.startswith(self._prefix), devices))
        if self._mac:
            devices = list(filter(lambda x : x.address == self.mac, devices))
        print(devices)

        self.wands = [self.wand_class(d.address, d.name, self.shop_loop) for d in devices]
        print(self.wands)
        if connect:
            for wand in self.wands:
                await wand.connect()
        return self.wands
