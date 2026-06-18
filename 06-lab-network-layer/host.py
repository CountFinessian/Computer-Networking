#!/usr/bin/python3

import argparse
import asyncio
import os
import socket
import sys
import struct

import json
import os

import re

from cougarnet.sim.host import BaseHost
from cougarnet.util import \
        mac_str_to_binary, mac_binary_to_str, \
        ip_str_to_binary, ip_binary_to_str

from prefix import *
from forwarding_table import ForwardingTable

# From /usr/include/linux/if_ether.h:
ETH_P_IP = 0x0800 # Internet Protocol packet
ETH_P_ARP = 0x0806 # Address Resolution packet

# From /usr/include/net/if_arp.h:
ARPHRD_ETHER = 1 # Ethernet 10Mbps
ARPOP_REQUEST = 1 # ARP request
ARPOP_REPLY = 2 # ARP reply

# From /usr/include/linux/in.h:
IPPROTO_ICMP = 1 # Internet Control Message Protocol
IPPROTO_TCP = 6 # Transmission Control Protocol
IPPROTO_UDP = 17 # User Datagram Protocol

class Host(BaseHost):
    def __init__(self, ip_forward: bool):
        super().__init__()

        # initialize the forwarding table for every host
        self._ip_forward = ip_forward

        self.forwardingTable = ForwardingTable()

        # Add entries from scenario2.cfg
        routes = json.loads(os.environ['COUGARNET_ROUTES'])

        for route in routes:
            # table.add_entry('10.20.0.0/23', 'r1-c', '10.30.0.2')
            self.forwardingTable.add_entry(*route)

        # For each  phyiscal interface, update the forwarding table
        #!/usr/bin/python3
        VIRT_INT_RE = re.compile(r'\.vlan\d+$')
        phys_ints = [i for i in os.listdir('/sys/class/net/') \
            if not i.startswith('lo') and VIRT_INT_RE.search(i) is None]
        
        for physicalInterface in phys_ints:
            prefix = self.prefix_for_int(physicalInterface)
            self.forwardingTable.add_entry(prefix, physicalInterface, None)

        # key: str IP addy's, value: str MAC addy's
        self.arpTable = {}

        # key: str IP addy, value: list of packets to be sent
        self.packetQueue = {}


    def _handle_frame(self, frame: bytes, intf: str) -> None:
        destinationMAC_FRAME = frame[:6]
        sourceMAC_FRAME = frame[6:12]
        etherTYPE_FRAME = frame[12:14]
        packet_FRAME = frame[14:]

        unpackedEtherTypeFrame = struct.unpack('!H', etherTYPE_FRAME)[0]
        binary_source_MAC_address = self.retrieve_sender_MAC_address(intf)
        binary_source_IP_address = self.retrieve_sender_IP_address(intf)

        if (destinationMAC_FRAME == binary_source_MAC_address or destinationMAC_FRAME == bytes([0xff, 0xff, 0xff, 0xff, 0xff, 0xff])):
            
            # Extract the destination MAC address in the frame
            # If the destination MAC address matches the corresponding interface on which it was received, or it was the broadcast MAC address
            # # For type ETH_P_IP, call handle_ip, and for type ETH_P_ARP, call handle_arp

            if(unpackedEtherTypeFrame == ETH_P_ARP):
                self.handle_arp(packet_FRAME, intf)

            elif(unpackedEtherTypeFrame == ETH_P_IP):
                self.handle_ip(packet_FRAME, intf)

    def handle_ip(self, pkt: bytes, intf: str) -> None:
        print("inside of the hanlde IP frame")

        destAddr = pkt[16:20]
        if self.IPV4_Match(destAddr, intf):
            print("There is a UDP or TCP packet here")
            protocol, = struct.unpack('!B', pkt[9:10])
            if (protocol == IPPROTO_TCP):
                self.handle_tcp(pkt)
            elif (protocol == IPPROTO_UDP):
                self.handle_udp(pkt)
        else:
            self.not_my_packet(pkt, intf)

    def handle_tcp(self, pkt: bytes) -> None:
        pass

    def handle_udp(self, pkt: bytes) -> None:
        pass

    def handle_arp(self, pkt: bytes, intf: str) -> None:
        # determine if this is an ARP request or Response using the OPCode field.
        OPCode_field, = struct.unpack('!H', pkt[6:8])

        if(OPCode_field == ARPOP_REQUEST):
            self.handle_arp_request(pkt, intf)
        elif(OPCode_field == ARPOP_REPLY):
            self.handle_arp_response(pkt, intf)

    def handle_arp_response(self, pkt: bytes, intf: str, debug=False) -> None:
        arpTable = self.arpTable
        packetQueue = self.packetQueue

        SMAC, SIP, DMAC, DIP = self.retreive_arp_info(pkt)
        stringSIP = ip_binary_to_str(SIP)
        
        if debug:
            print("handling arp response")
            print(f"Source MAC {SMAC.hex(" ")}")
            print(f"Source IP {SIP.hex(" ")}")
            print(f"Destination MAC {DMAC.hex(" ")}")
            print(f"Destination IP {DIP.hex(" ")}")

        arpTable[stringSIP] = mac_binary_to_str(SMAC)

        if stringSIP in packetQueue:
            print("sending some packets from the packet queue")
            existingQueue = packetQueue[stringSIP]
            for pkt in existingQueue:
                self.send_ethernet_frame(SMAC, DMAC, struct.pack('!H', ETH_P_IP), pkt, intf, True)

            del packetQueue[stringSIP]

    def handle_arp_request(self, pkt: bytes, intf: str) -> None:
        arpTable = self.arpTable
        SMAC, SIP, DMAC, DIP = self.retreive_arp_info(pkt)

        if self.IPV4_Match(DIP, intf):
            arpTable[ip_binary_to_str(SIP)] = mac_binary_to_str(SMAC)

            # send an ARP response
            DMAC = self.retrieve_sender_MAC_address(intf)
            arpResponse = self.create_an_arp_response(DMAC, DIP, SMAC, SIP)
            self.send_ethernet_frame(SMAC, DMAC, struct.pack('!H', ETH_P_ARP), arpResponse, intf)


    def send_packet_on_int(self, pkt: bytes, intf: str, next_hop: str) -> None:
        # this is the first function which we are going to be implimenting from the lab
        arpTable = self.arpTable
        packetQueue = self.packetQueue

        binary_destination_IP_address = ip_str_to_binary(next_hop)
        binary_source_MAC_address = self.retrieve_sender_MAC_address(intf)
        binary_source_IP_address = self.retrieve_sender_IP_address(intf)

        if next_hop in arpTable:
            destionationMAC = mac_str_to_binary(arpTable[next_hop])
            self.send_ethernet_frame(destionationMAC, binary_source_MAC_address, struct.pack('!H', ETH_P_IP), pkt, intf, True)
        else:
            # sending off an ARP request
            binary_destination_MAC_address = bytes([0xff, 0xff, 0xff, 0xff, 0xff, 0xff])
            packetARP = self.create_an_arp_request(binary_source_MAC_address, binary_source_IP_address, binary_destination_IP_address, True)
            self.send_ethernet_frame(binary_destination_MAC_address, binary_source_MAC_address, struct.pack('!H', ETH_P_ARP), packetARP, intf)

            # adding the frame to the queue until we get a response
            if(next_hop in packetQueue):
                existingQueue = packetQueue[next_hop]
                existingQueue.append(pkt)
                packetQueue[next_hop] = existingQueue

            else:
                packetQueue[next_hop] = [pkt]

    def send_packet(self, pkt: bytes, debug=False) -> None:
        
        forwardingTable = self.forwardingTable
        destAddrStr = ip_binary_to_str(pkt[16:20])
        valueTuple = forwardingTable.get_entry(destAddrStr)

        outgoingIntf = valueTuple[0]
        nextHop = valueTuple[1]

        if debug:
            print(f"destination address {destAddrStr}")
            print(f"outgoingIntf {outgoingIntf}")
            print(f"Next hop {nextHop}")

        if (outgoingIntf != None):
            if (nextHop != None):
                self.send_packet_on_int(pkt, outgoingIntf, nextHop)
            else:
                self.send_packet_on_int(pkt, outgoingIntf, destAddrStr)

    def forward_packet(self, pkt: bytes) -> None:
        ttl, = struct.unpack('!B', pkt[8:9])
        ttl = ttl - 1
        
        if (ttl > 0):
           decrementedTTLPacket = pkt[:8] + struct.pack('!B', ttl) + pkt [9:]
           self.send_packet(decrementedTTLPacket)
           

    def not_my_frame(self, frame: bytes, intf: str) -> None:
        pass

    def not_my_packet(self, pkt: bytes, intf: str, debug=False) -> None:
        srcAddrStr = ip_binary_to_str(pkt[12:16])
        destAddrStr = ip_binary_to_str(pkt[16:20])

        if (self._ip_forward):
            
            if debug:
                print(f"not my packet {pkt}")
                print(f"received packet on intf {intf} from source address {srcAddrStr} with destination address {destAddrStr}")
            self.forward_packet(pkt)

    def prefix_for_int(self, intf: str) -> str:
        obj = self.ipv4_address_info_single(intf)
        ip_int = ip_str_to_int(obj['address'])
        ip_prefix_int = ip_prefix(ip_int, socket.AF_INET, obj['prefixlen'])
        first_addr = ip_int_to_str(ip_prefix_int, socket.AF_INET)
        return '%s/%d' % (first_addr, obj['prefixlen'])

    def bcast_for_int(self, intf: str) -> str:
        obj = self.ipv4_address_info_single(intf)
        ip_int = ip_str_to_int(obj['address'])
        ip_prefix_int = ip_prefix(ip_int, socket.AF_INET, obj['prefixlen'])
        ip_bcast_int = ip_prefix_last_address(ip_prefix_int, socket.AF_INET, obj['prefixlen'])
        bcast = ip_int_to_str(ip_bcast_int, socket.AF_INET)
        return bcast

    def retrieve_sender_MAC_address(self, intf: str):

        MAC_address = self.interface_info_single(intf)['address']
        binary_MAC_address = mac_str_to_binary(MAC_address)

        return binary_MAC_address
    
    def retrieve_sender_IP_address(self, intf: str):
        IP_address = self.ipv4_address_info_single(intf)['address']
        binary_IP_address = ip_str_to_binary(IP_address)

        return binary_IP_address

    def create_an_arp_request(self, SMAC: bytes, SIP: bytes, DIP: bytes, debug=False):

        first_part_of_ARP = struct.pack('!H', ARPHRD_ETHER) + struct.pack('!H', ETH_P_IP) + struct.pack('!B', 6) + struct.pack('!B', 4) + struct.pack('!H', ARPOP_REQUEST)
        second_part_of_ARP = SMAC + SIP + bytes(6) + DIP
        arpPacket = first_part_of_ARP + second_part_of_ARP

        if (debug):
            print('my arp packet binary: %s' % arpPacket.hex(' '))
        return arpPacket
    
    def create_an_arp_response(self, SMAC: bytes, SIP: bytes, DMAC: bytes, DIP: bytes, debug=False):

        first_part_of_ARP = struct.pack('!H', ARPHRD_ETHER) + struct.pack('!H', ETH_P_IP) + struct.pack('!B', 6) + struct.pack('!B', 4) + struct.pack('!H', ARPOP_REPLY)
        second_part_of_ARP = SMAC + SIP + DMAC + DIP
        arpPacket = first_part_of_ARP + second_part_of_ARP

        if (debug):
            print('my arp packet binary: %s' % arpPacket.hex(' '))
        return arpPacket
    
    def retreive_arp_info(self, pkt):
       hardwareAddressLength, = struct.unpack('!B', pkt[4:5])
       protocolAddressLength, = struct.unpack('!B', pkt[5:6])

       bufferIncrementer = 8
       SMAC = pkt[bufferIncrementer:(bufferIncrementer+hardwareAddressLength)]
       bufferIncrementer += hardwareAddressLength
       SIP = pkt[bufferIncrementer:(bufferIncrementer+protocolAddressLength)]
       bufferIncrementer += protocolAddressLength
       DMAC = pkt[bufferIncrementer:(bufferIncrementer+hardwareAddressLength)]
       bufferIncrementer += hardwareAddressLength
       DIP = pkt[bufferIncrementer:(bufferIncrementer+protocolAddressLength)]

       return SMAC, SIP, DMAC, DIP

    def IPV4_Match(self, IPV4: bytes, intf:str):

        strIPV4 = ip_binary_to_str(IPV4)
        list_of_IPV4s = self.ipv4_addresses_info(intf)
        for IPV4_ADDR in list_of_IPV4s:
            if (IPV4_ADDR == strIPV4):
                return True
        return False

    def send_ethernet_frame(self, dest_MAC_addr: bytes, source_MAC_addr: bytes, type: bytes, payload: bytes, intf: str, debug=False):

        ethernetFrame = dest_MAC_addr + source_MAC_addr + type + payload

        if debug:

            print(f"destination MAC address {dest_MAC_addr}")
            print(f"source MAC address {source_MAC_addr}")
            print(f"interface {intf}")
            # print('ethernetFrame in binary: %s' % ethernetFrame.hex(' '))
        
        self.send_frame(ethernetFrame, intf)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--router', '-r',
            action='store_const', const=True, default=False,
            help='Act as a router by forwarding IP packets')
    args = parser.parse_args(sys.argv[1:])

    Host(args.router).run()

if __name__ == '__main__':
    main()
