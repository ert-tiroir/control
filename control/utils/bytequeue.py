
from threading import Lock


class ByteQueue:
    def __init__(self, threshold = 128_000) -> None:
        self._buffer = bytearray()
        self.offset  = 0
        self.threshold = threshold

        self.lock = Lock()
    
    def put (self, bytes):
        self.lock.acquire()
        self._buffer.extend(bytes)
        self.lock.release()
    def peek (self, size: int):
        self.lock.acquire()
        result = self._buffer[self.offset:self.offset + size]
        self.lock.release()
        return result
    def pop (self, size: int):
        self.lock.acquire()
        data = self._buffer[self.offset:self.offset + size]
        self.offset += size

        if self.offset >= self.threshold:
            self._buffer[:self.offset] = b''
            self.offset = 0
        if self.offset >= len(self._buffer):
            self._buffer.clear()
            self.offset = 0
        self.lock.release()
        return data
    def __len__(self):
        return len(self._buffer) - self.offset
