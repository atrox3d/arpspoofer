from scapy.all import *
from scapy.layers.l2 import Ether

broadcast = Ether(dst='ff:ff:ff:ff')
