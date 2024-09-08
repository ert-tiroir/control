
class ByteQueue:
    def __init__(self, threshold = 128_000) -> None:
        self._buffer = bytearray()
        self.offset  = 0
        self.threshold = threshold
    
    def put (self, bytes):
        self._buffer.extend(bytes)
    def pop (self, size: int):
        data = self._buffer[self.offset:self.offset + size]
        self.offset += size

        if self.offset >= self.threshold:
            self._buffer[:self.offset] = b''
            self.offset = 0
        if self.offset >= len(self._buffer):
            self._buffer.clear()
            self.offset = 0
        return data
    def __len__(self):
        return len(self._buffer) - self.offset
