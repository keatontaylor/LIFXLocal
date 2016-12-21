'''
Test for LIFXLocal Library
'''

from lifxlocal import *

devices = []

def find_bulb(mac):
    """Search for bulbs."""
    bulb = None
    for device in devices:
        if device.mac == mac:
            bulb = device
            break
    return bulb

def power_callback(ipaddr, power_level):
	pass

def color_callback(ipaddr, label, hue, sat, bri, kel):
	pass

def service_callback(ipaddr, port, mac):
	bulb = find_bulb(mac)

	if bulb is None:
		print('New Bulb: {0} {1} {2}'.format(ipaddr, port, mac))
		bulb = LIFXLight(lifxlocal, ipaddr, port, mac)
		devices.append(bulb)

lifxlocal = LifxLocal(service_callback, power_callback, color_callback)



class LIFXLight(object):
    """Representation of a LIFX light."""

    def __init__(self, lifxlocal, ipaddr, port, mac):
        """Initialize the light."""
        self._lifxlocal = lifxlocal
        self._ip = ipaddr
        self._port = port
        self._mac = mac

    @property
    def should_poll(self):
        """No polling needed for LIFX light."""
        return False

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def ipaddr(self):
        """Return the IP address of the device."""
        return self._ip

    @property
    def port(self):
    	return self._port

    @property
    def mac(self):
    	"""Set mac of the light."""
    	return self._mac

    def set_name(self, name):
        """Set name of the light."""
        self._name = name

    def set_port(self, port):
    	"""Set port of the light."""
    	self._port = port

    def set_ipaddr(self, ipaddr):
    	"""Set ip of the light."""
    	self._ip = ipaddr



while True:
    pass