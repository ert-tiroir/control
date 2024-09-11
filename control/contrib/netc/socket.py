
from io import BytesIO
import socket
import threading

from control.contrib.protocol.abstract import AbstractProtocolApp


class NetControllerSocket:
    def __init__(self, sock=None) -> None:
        self.lock = threading.Lock()
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock
    
    def connect (self, host, port):
        self.sock.connect((host, port))
    def close (self):
        with self.lock:
            if self.sock is not None:
                self.sock.close()
                self.sock = None
    def is_closed (self):
        return self.sock is None
    
    def send (self, buffer: bytes):
        if self.is_closed(): return False

        totalsent = 0
        while totalsent < len(buffer):
            sent = self.sock.send(buffer[totalsent:])
            if sent == 0:
                self.close()
                return False
            totalsent += sent
        return True
    def receive_forced (self, size=8) -> bytes:
        chunks = []
        total  = 0
        while total < size:
            chunk = self.sock.recv( min( size - total, 2048 ) )
            if chunk == b'':
                self.close()
                return b''
            chunks.append(chunk)
            total += len(chunk)
        return b''.join(chunks)
    def receive (self, protocol: AbstractProtocolApp):
        sze_header = self.receive_forced( protocol.sze_field.length )
        if sze_header == b'': return b''

        size = protocol.sze_field.parse( BytesIO( sze_header ) )
        payload = self.receive_forced(size)
        if payload == b'': return b''

        return sze_header + payload