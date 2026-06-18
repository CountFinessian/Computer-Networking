#!/usr/bin/env python3

import asyncio
import json
import socket

NEIGHBOR_CHECK_INTERVAL = 3
DV_TABLE_SEND_INTERVAL = 1
DV_PORT = 5016

from cougarnet.sim.host import BaseHost

from prefix import *
from forwarding_table_native import ForwardingTableNative as ForwardingTable

class DVRouter(BaseHost):
    def __init__(self):
        super().__init__()

        self.my_dv = {}
        self.neighbor_dvs = {}

        self.forwarding_table = ForwardingTable()

        self._initialize_dv_sock()

        self.nameToIP = {}

        self.eventLoop = {}

        # Do any further initialization here

    def _initialize_dv_sock(self) -> None:
        '''Initialize the socket that will be used for sending and receiving DV
        communications to and from neighbors.
        '''

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind(('0.0.0.0', DV_PORT))

    def init_dv(self):
        '''Set up our instance to work with the event loop, initialize our DV,
        and schedule our regular updates to be sent to neighbors.
        '''

        interfaceHostName = self.hostname
        print(f"Interface: {interfaceHostName}")


        loop = asyncio.get_event_loop()

        # register our socket with the event loop, so we can handle datagrams
        # as they come in
        loop.add_reader(self.sock, self._handle_msg, self.sock)

        # Initialize our DV -- and optionally send our DV to our neighbors
        self.update_dv()

        # Schedule self.send_dv_next() to be called in 1 second and
        # self.update_dv_next() to be called in 0.5 seconds.
        loop.call_later(DV_TABLE_SEND_INTERVAL, self.send_dv_next)
        loop.call_later(DV_TABLE_SEND_INTERVAL - DV_TABLE_SEND_INTERVAL / 2,
                self.update_dv_next)

    def _handle_msg(self, sock: socket.socket) -> None:
        ''' Receive and handle a message received on the UDP socket that is
        being used for DV messages.
        '''

        data, addrinfo = sock.recvfrom(65536)
        self.handle_dv_message(data)

    def _send_msg(self, msg: bytes, dst: str) -> None:
        '''Send a DV message, msg, on our UDP socket to dst.'''

        self.sock.sendto(msg, (dst, DV_PORT))

    def handle_dv_message(self, msg: bytes) -> None:
        obj_str = msg.decode('utf-8')
        obj = json.loads(obj_str)

        ip = obj["ip"]
        name = obj["name"]
        dv = obj["dv"]

        print(f"hostname {self.hostname} and distance vector name {name}")
        if (self.hostname != name):
            self.nameToIP[name] = ip
            self.neighbor_dvs[name] = dv
            self.eventLoop[name] = 3
        else:
            print("the hostname matches the name of the distance vector")

        # if name in eventLoops:
        #     event = eventLoops[name]
        #     event.cancel()
        
        # event = loop.call_later(3, self.handle_down_link, name)
    def send_dv_next(self):
        '''Send DV to neighbors, and schedule this method to be called again in
        1 second (DV_TABLE_SEND_INTERVAL).
        '''
        self.send_dv()
        loop = asyncio.get_event_loop()
        loop.call_later(DV_TABLE_SEND_INTERVAL, self.send_dv_next)

    def update_dv_next(self):
        '''Update DV using neighbors' DVs.  Then schedule this method to be
        called again in 1 second (DV_TABLE_SEND_INTERVAL).
        '''

        self.update_dv()
        loop = asyncio.get_event_loop()
        loop.call_later(DV_TABLE_SEND_INTERVAL, self.update_dv_next)

    def handle_down_link(self, neighbor: str):
        self.log(f'Link down: {neighbor}')
        del self.neighbor_dvs[neighbor]

    def resolve_neighbor_dvs(self):
        '''Return a copy of the mapping of neighbors to distance vectors, with
        IP addresses replaced by names in every neighbor DV.
        '''

        neighbor_dvs = {}
        for neighbor in self.neighbor_dvs:
            neighbor_dvs[neighbor] = self.resolve_dv(self.neighbor_dvs[neighbor])
        return neighbor_dvs

    def resolve_dv(self, dv: dict) -> dict:
        '''Return a copy of distance vector dv with IP addresses replaced by
        names.
        '''
        resolved_dv = {}
        for dst, distance in dv.items():
            if '/' not in dst:
                try:
                    dst = socket.getnameinfo((dst, 0), 0)[0]
                except:
                    pass
            resolved_dv[dst] = distance
        return resolved_dv

    def update_dv(self) -> None:
        neighborDVs = self.neighbor_dvs
        myDV = self.my_dv
        eventLoop = self.eventLoop

        old_dv = self.my_dv.copy()

        # clear the contents within my distance vector
        myDV.clear()

        # update the distance vectors based on your own links
        physicalInterfaces = self.physical_interfaces()
        for interface in physicalInterfaces:
            prefix = self.prefix_for_int(interface)
            IPAddr = self.ipv4_address_info_single(interface)['address']
            myDV[prefix] = (0, IPAddr)

        # if a neighbor hasn't recieved a keep alive in more than 3 seconds, remove the DV
        if neighborDVs:

            # turn the nabor Names (keys) from dictionary into a list
            naborsKeys = list(neighborDVs)

            for naborName in naborsKeys:
                timeNaborBeenUpdated = eventLoop[naborName]
                timeNaborBeenUpdated -= 1 
                
                if (timeNaborBeenUpdated <= 0):
                    print(f'Removing Nabor {naborName} timeNaborBeenUpdated {timeNaborBeenUpdated}')
                    self.handle_down_link(naborName)
                else:
                    eventLoop[naborName] = timeNaborBeenUpdated

        # update the distance vectors based upon your neighbors
        if neighborDVs:
            for naborName in neighborDVs:
                naborDV = neighborDVs[naborName]
                naborIP = self.nameToIP[naborName]

                for prefix in naborDV:
                    naborDVTuple = naborDV[prefix]
                    print(f"naborDVTuple {naborDVTuple}")
                    naborDistance = naborDVTuple[0] + 1
                    print(f"naborDistance {naborDistance}")

                    # there is a already an existing prefix
                    if prefix in myDV:

                        # retrieve the existing distance
                        existingDistanceTuple = myDV[prefix]
                        
                        # complete the Bellman-Ford algorithm
                        if (naborDistance < existingDistanceTuple[0]):
                            myDV[prefix] = (naborDistance, naborIP)
                            # at this point, the forwarding table needs to be updated
                            # forwardingTable.remove_entry(prefix)
                            # forwardingTable.add_entry(prefix, None, naborIP)
                       
                    else:
                        # this is currently the only path we know of
                        myDV[prefix] = (naborDistance, naborIP)
                        # forwardingTable.add_entry(prefix, None, naborIP)

        if old_dv != self.my_dv:
            self.update_forwardingTable()

            # print(self.resolve_dv(neighborDVs))
            # print(forwardingTable.get_all_entries(resolve=False))

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

    def send_dv(self) -> None:
        interfaceHostName = self.hostname
        # print(f"Interface: {interfaceHostName}")

        # get all of your physical links to send out your DV over
        physicalInterfaces = self.physical_interfaces()

        for interface in physicalInterfaces:


            prefix = self.prefix_for_int(interface)
            broadcastAddr = self.bcast_for_int(interface)
            IPAddr = self.ipv4_address_info_single(interface)['address']

            obj = { 'ip': IPAddr, 'name': interfaceHostName, 'dv': self.my_dv }
            obj_str = json.dumps(obj)
            obj_bytes = obj_str.encode('utf-8')

            # print(f"Sending message interface: {interface} prefix: {prefix} broadcast: {broadcastAddr} IPAddr: {IPAddr}")
            self._send_msg(obj_bytes, broadcastAddr)

    def update_forwardingTable(self) -> None:
        my_dv = self.my_dv
        forwardingTable = self.forwarding_table

        forwardingTable.flush()

        for prefix in my_dv:
            my_dvTuple = my_dv[prefix]
            dist = my_dvTuple[0]
            ipAddr = my_dvTuple[1]
            if (dist > 0):
                forwardingTable.add_entry(prefix, None, ipAddr)

        # print(forwardingTable.get_all_entries(resolve=False))
        print(self.resolve_dv(my_dv))

def main():
    router = DVRouter()
    router.init_dv()
    router.run()

if __name__ == '__main__':
    main()
