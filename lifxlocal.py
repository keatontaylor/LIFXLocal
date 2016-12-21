'''
lifxlocal - LIFX LAn Protocol Python Library

https://github.com/keatontaylor/lifxlocal

Published under the MIT license - See LICENSE file for details.

Not associated with or endorsed by LiFi Labs, Inc. (http://www.lifx.com/)

Based on https://github.com/TangoAlpha/liffylights and https://https://github.com/mclarkk/lifxlan
'''

import threading
import time
import queue
import socket
import io
import ipaddress
import struct
from enum import IntEnum
import binascii


## Constants
HEADER_SIZE_BYTES = 36
BUFFER_SIZE = 1024
QUEUE_SIZE = 255
UDP_PORT = 56700


class LifxLocal(object):
	def __init__(self, service_callback, power_callback, color_callback, server_addr=None, broadcast_addr=None):

		self._service_callback = service_callback
		self._power_callback = power_callback
		self._color_callback = color_callback

		self._packet_lock = threading.Lock()
		self._packets = []

		self._queue = queue.Queue(maxsize=QUEUE_SIZE)

		if server_addr is None:
			listener_addr = "0.0.0.0"
		else:
			listener_addr = server_addr

	    # Setup socket to listen on supplied UPD port.
		self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		self._sock.bind((listener_addr, UDP_PORT))

	    # Threading for packet listener.
		self._listener = threading.Thread(target=self._packet_listener)
		self._listener.daemon = True
		self._listener.start()

	def _packet_listener(self):
		while True:
			datastream, (ipaddr, port) = self._sock.recvfrom(BUFFER_SIZE)
			ProcessMessage(ipaddr, port, datastream, self._service_callback, self._color_callback, self._power_callback)  # this needs to be fixed....

class PackMesssage(object):

		
class ProcessMessage(object):
	def __init__(self, ipaddr, port, packed_message, service_callback, color_callback, power_callback):
	    header_str = packed_message[0:HEADER_SIZE_BYTES]
	    payload_str = packed_message[HEADER_SIZE_BYTES:]

	    size = struct.unpack("H", header_str[0:2])[0]
	    flags = struct.unpack("H", header_str[2:4])[0]
	    origin = (flags >> 14) & 3
	    tagged = (flags >> 13) & 1
	    addressable = (flags >> 12) & 1
	    protocol = flags & 4095
	    source_id = struct.unpack("I", header_str[4:8])[0]
	    target_addr = ":".join([('%02x' % b) for b in struct.unpack("B"*6, header_str[8:14])])
	    response_flags = struct.unpack("B", header_str[22:23])[0]
	    ack_requested = response_flags & 2
	    response_requested = response_flags & 1
	    seq_num = struct.unpack("B", header_str[23:24])[0]
	    message_type = struct.unpack("H", header_str[32:34])[0]

	    if message_type == PayloadType.STATESERVICE:
	        service = struct.unpack("B", payload_str[0:1])[0]
	        port = struct.unpack("I", payload_str[1:5])[0]
	        service_callback(ipaddr, port, target_addr)
	        ## Future discovery code to follow proper LIFX workflow.

	    # elif message_type == PayloadType.STATEHOSTINFO:
	    #     signal = struct.unpack("f", payload_str[0:4])[0]
	    #     tx = struct.unpack("I", payload_str[4:8])[0]
	    #     rx = struct.unpack("I", payload_str[8:12])[0]
	    #     reserved1 = struct.unpack("h", payload_str[12:14])[0]
	    #     ## Future values to be used for sensor info based on LIFX lights.

	    # elif message_type == PayloadType.STATEHOSTFIRMWARE:
	    #     host_build = struct.unpack("Q", payload_str[0:8])[0]
	    #     reserved1 = struct.unpack("Q", payload_str[8:16])[0]
	    #     host_version = struct.unpack("I", payload_str[16:20])[0]
	    #     ## Future values to be used for sensor info based on LIFX lights.

	    # elif message_type == PayloadType.STATEWIFIINFO:
	    #     signal = struct.unpack("f", payload_str[0:4])[0]
	    #     tx = struct.unpack("I", payload_str[4:8])[0]
	    #     rx = struct.unpack("I", payload_str[8:12])[0]
	    #     reserved1 = struct.unpack("h", payload_str[12:14])[0]
	    #     ## Future values to be used for sensor info based on LIFX lights.

	    # elif message_type == PayloadType.STATEWIFIFIRMWARE:
	    #     wifi_build = struct.unpack("Q", payload_str[0:8])[0]
	    #     reserved1 = struct.unpack("Q", payload_str[8:16])[0]
	    #     wifi_version = struct.unpack("I", payload_str[16:20])[0]
	    #     ## Future values to be used for sensor info based on LIFX lights.

	    if message_type == PayloadType.STATEPOWER1:
	        power_level = struct.unpack("H", payload_str[0:2])[0]
	        power_callback(ipaddr, power_level)

	    # elif message_type == PayloadType.STATELABEL:
	    #     label = binascii.unhexlify("".join(["%2.2x" % (b & 0x000000ff) for b in struct.unpack("b"*32, payload_str[0:32])]))
	    #     ## Future values to be used for sensor info based on LIFX lights.

	    # elif message_type == PayloadType.STATELOCATION:
	    #     location = [b for b in struct.unpack("B"*16, payload_str[0:16])]
	    #     label = binascii.unhexlify("".join(["%2.2x" % (b & 0x000000ff) for b in struct.unpack("b"*32, payload_str[16:48])]))
	    #     updated_at = struct.unpack("Q", payload_str[48:56])[0]
	    #     ## Future values to be used for sensor info based on LIFX lights.

	    # elif message_type == PayloadType.STATEGROUP:
	    #     group = [b for b in struct.unpack("B"*16, payload_str[0:16])]
	    #     label = binascii.unhexlify("".join(["%2.2x" % (b & 0x000000ff) for b in struct.unpack("b"*32, payload_str[16:48])]))
	    #     updated_at = struct.unpack("Q", payload_str[48:56])[0]
	    #     ## Future values to be used for sensor info based on LIFX lights.

	    # elif message_type == PayloadType.STATEVERSION:
	    #     vendor = struct.unpack("I", payload_str[0:4])[0]
	    #     product = struct.unpack("I", payload_str[4:8])[0]
	    #     version = struct.unpack("I", payload_str[8:12])[0]
	    #     ## Future values to be used for sensor info based on LIFX lights.

	    # elif message_type == PayloadType.STATEINFO:
	    #     time = struct.unpack("Q", payload_str[0:8])[0]
	    #     uptime = struct.unpack("Q", payload_str[8:16])[0]
	    #     downtime = struct.unpack("Q", payload_str[16:24])[0]
	    #     ## Future values to be used for sensor info based on LIFX lights.

	    elif message_type == PayloadType.ACKNOWLEDGEMENT:
	    	# fix this
	    	pass

	    # elif message_type == PayloadType.ECHORESPONSE:
	    #     byte_array_len = len(payload_str)
	    #     byte_array = [b for b in struct.unpack("B"*byte_array_len, payload_str[0:byte_array_len])]
	    #     ## Future values to be used for sensor info based on LIFX lights.

	    elif message_type == PayloadType.STATE:
	        color = struct.unpack("H"*4, payload_str[0:8])
	        reserved1 = struct.unpack("H", payload_str[8:10])[0]
	        power_level = struct.unpack("H", payload_str[10:12])[0]
	        label = binascii.unhexlify("".join(["%2.2x" % (b & 0x000000ff) for b in struct.unpack("b"*32, payload_str[12:44])])).decode('ascii').replace("\x00", "")
	        reserved2 = struct.unpack("Q", payload_str[44:52])[0]

	        hue, sat, bri, kel = color
	        color_callback(ipaddr, label, hue, sat, bri, kel)

	    elif message_type == PayloadType.STATEPOWER2:
	        power_level = struct.unpack("H", payload_str[0:2])[0]
	        power_callback(ipaddr, power_level)

	    else:
	    	pass


class PayloadType(IntEnum):
    """ Message payload types. """
    GETSERVICE = 2
    STATESERVICE = 3
    GETHOSTINFO = 12
    STATEHOSTINFO = 13
    GETHOSTFIRMWARE = 14
    STATEHOSTFIRMWARE = 15
    GETWIFIINFO = 16
    STATEWIFIINFO = 17
    GETWIFIFIRMWARE = 18
    STATEWIFIFIRMWARE = 19
    GETPOWER1 = 20
    SETPOWER1 = 21
    STATEPOWER1 = 22
    GETLABEL = 23
    SETLABEL = 24
    STATELABEL = 25
    GETVERSION = 32
    STATEVERSION = 33
    GETINFO = 34
    STATEINFO = 35
    ACKNOWLEDGEMENT = 45
    GETLOCATION = 48
    STATELOCATION = 50
    GETGROUP = 51
    STATEGROUP = 53
    ECHOREQUEST = 58
    ECHORESPONSE = 59
    GET = 101
    SETCOLOR = 102
    STATE = 107
    GETPOWER2 = 116
    SETPOWER2 = 117
    STATEPOWER2 = 118


