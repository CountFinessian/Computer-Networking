#!/usr/bin/python3

import asyncio
from cougarnet.sim.host import BaseHost
from datetime import datetime
import struct

class Switch(BaseHost):
    def __init__(self):
        super().__init__()
        self.switchingTable = {}
        # do any initialization here...

    def _handle_frame(self, frame: bytes, intf: str) -> None:

        sourceVlanType = self.int_to_vlan[intf]

        if sourceVlanType < 0:
            frame, sourceVlanType = self._unpack_frame(frame)

        destinationFrames = frame[:6]
        sourceFrames = frame[6:12]

        # Switching Table Logic
        self.handle_switching_table(sourceFrames, intf)
        switchingTable = self.switchingTable

        # unicast
        if destinationFrames in switchingTable:
            destinationIntf = switchingTable[destinationFrames][0]
            destinationVlanType = self.int_to_vlan[destinationIntf]

            if (sourceVlanType == destinationVlanType):
                self.send_frame(frame, destinationIntf)

            elif (destinationVlanType < 0):
                frameToPack = self._pack_up_frame(frame, sourceVlanType)
                self.send_frame(frameToPack, destinationIntf)
                
        # broadcast
        else:
            for selectedInterface in self.physical_interfaces():
                destinationVlanType = self.int_to_vlan[selectedInterface]

                if intf != selectedInterface:

                    if destinationVlanType == sourceVlanType:
                        self.send_frame(frame, selectedInterface)

                    elif(destinationVlanType < 0):
                        frameToPack = self._pack_up_frame(frame, sourceVlanType)
                        self.send_frame(frameToPack, selectedInterface)

    def _pack_up_frame(self, frameToPack, sourceVlanType):
        eight0two_frame = struct.pack('!H', 0x08100) + struct.pack('!H', sourceVlanType)
        trunk_frame = frameToPack[:12] + eight0two_frame + frameToPack[12:]
        return trunk_frame
    
    def _unpack_frame(self, packedFrame):
            sourceVlanType = struct.unpack('!H', packedFrame[14:16])[0]
            unpackedFrame = packedFrame[:12] + packedFrame[16:]
            return unpackedFrame, sourceVlanType


    def handle_switching_table(self, sourceFrames, intf):
        switchingTable = self.switchingTable
        currentTime = datetime.now()
        sourceTimestampTuple = (intf, currentTime)
        switchingTable[sourceFrames] = sourceTimestampTuple

        expiredKeys = []
        for currentSource in switchingTable:
            timestamp = switchingTable[currentSource][1]
            if((currentTime - timestamp).total_seconds() >= 8):
                    expiredKeys.append(currentSource)

        for expiredKey in expiredKeys:
            del switchingTable[expiredKey]

def main():
    Switch().run()

if __name__ == '__main__':
    main()
