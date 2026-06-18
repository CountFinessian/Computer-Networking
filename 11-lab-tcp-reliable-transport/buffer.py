class TCPSendBuffer(object):
    def __init__(self, seq: int):
        self.buffer = b''
        self.base_seq = seq
        self.next_seq = self.base_seq
        self.last_seq = self.base_seq

    def bytes_not_yet_sent(self) -> int:
        return self.last_seq - self.next_seq

    def bytes_outstanding(self) -> int:
        return self.next_seq - self.base_seq

    def put(self, data: bytes) -> int:
        self.buffer += data
        self.last_seq += len(data)

    def get(self, size: int) -> tuple[bytes, int]:
    
        oldNextSeq = self.next_seq
        startingSlice = self.next_seq - self.base_seq
        endingSlice = 0

        if (self.next_seq + size > self.last_seq):
            endingSlice = self.last_seq - self.base_seq
            self.next_seq = self.last_seq
        
        else:
             self.next_seq += size
             endingSlice = startingSlice + size

        bufferSlice = self.buffer[startingSlice: endingSlice]
        return (bufferSlice, oldNextSeq)
    

    def get_for_resend(self, size: int) -> tuple[bytes, int]:
        bufferSlice = b''
        endingSlice = size

        if(self.base_seq + size > self.last_seq):
            endingSlice = self.last_seq - self.base_seq

        bufferSlice = (self.buffer[:endingSlice])
        
        return(bufferSlice, self.base_seq)

    def slide(self, sequence: int) -> None:
        slideIndex = sequence - self.base_seq
        self.base_seq = sequence
        self.buffer = self.buffer[slideIndex:]

    def relativeSequence(self):
        return self.next_seq - self.base_seq,
class TCPReceiveBuffer(object):
    def __init__(self, seq: int):
        self.buffer = {}
        self.base_seq = seq

    def put(self, data: bytes, sequence: int) -> None:
        buffer = self.buffer
        baseSeq = self.base_seq

        if(sequence < baseSeq):
            if(sequence + len(data) <= baseSeq):
                return
            else:
                sliceIndex = baseSeq - sequence
                data = data[sliceIndex:]
                sequence = baseSeq

        if(sequence in buffer):
            previousData = buffer[sequence]

            if(len(data) < len(previousData)):
                return
        
        buffer[sequence] = data
        keyValue = (None, None)

        for nextSequence, nextData in sorted(buffer.items()):
            # first iteration should skip this if statement
            if keyValue != (None, None):
                sequence, data = keyValue
                endSequence = sequence + len(data)
                if (endSequence > nextSequence):
                    del buffer[nextSequence]
                    sliceIndex = endSequence - nextSequence
                    
                    nextSequence = nextSequence + sliceIndex
                    nextData = nextData[sliceIndex:]
                    buffer[nextSequence] = nextData
                    
            keyValue = (nextSequence, nextData)

    def get(self) -> tuple[bytes, int]:
        payload = b''
        initialBaseSeq = self.base_seq
        iterativeBaseSeq = self.base_seq
        buffer = self.buffer

        while (iterativeBaseSeq in buffer):
            data = buffer[iterativeBaseSeq]
            del buffer[iterativeBaseSeq]
            iterativeBaseSeq += len(data)
            payload += data
        
        self.base_seq = iterativeBaseSeq
        return(payload, initialBaseSeq)
