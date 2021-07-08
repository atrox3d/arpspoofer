import sys
import os
import time

display = os.environ.get("DISPLAY")
if display:
    print(f"{display}")
else:
    print("DISPLAY not set, setting...")
    os.environ["DISPLAY"] = ":0.0"
import scapy.all as scapy

if len(sys.argv) < 3:
    target_ip = input("[+] Enter target ip address: ")
    router_ip = input("[+] Enter router ip address: ")
elif len(sys.argv) == 3:
    target_ip, router_ip = sys.argv[1:]
else:
    print(f"syntax {sys.argv[0]} target_ip router_ip")
    exit()

print(f"target ip: {target_ip}")
print(f"router ip: {router_ip}")

BROADCAST_MAC = "ff:ff:ff:ff:ff:ff"

KALI_IP = "192.168.1.195"
KALI_MAC = "08:00:27:80:a4:72"

W10_IP = "192.168.1.10"
W10_MAC = "90:E6:BA:46:95:5E"

ROUTER_IP = "192.168.1.254"
ROUTER_MAC = "84:26:15:f9:16:44"


def get_mac_address(ip_address):
    broadcast_layer = scapy.Ether(dst=BROADCAST_MAC)
    arp_layer = scapy.ARP(pdst=ip_address)
    get_mac_packet = broadcast_layer/arp_layer
    answer, unanswer = scapy.srp(get_mac_packet, timeout=2, verbose=False)
    sent, received = answer[0]
    return received.hwsrc


target_mac = get_mac_address(target_ip)
router_mac = get_mac_address(router_ip)

print(f"target: ip={target_ip}, mac={target_mac}")
print(f"router: ip={router_ip}, mac={router_mac}")
