
import socketserver
import threading
import time
from typing import Tuple
from control.contrib.phyc.devices.device import PhysicalDevice

import socket

from control.utils.bytequeue import ByteQueue

class AbstractSocketDevice(PhysicalDevice):
    def init_channel (self):
        self.tx_buffer = ByteQueue()

        self.running = True
    def get_name (self):
        assert False, "Not implemented"

    def start_transfer (self, buffer: bytes):
        self.tx_buffer.put(buffer)
    
    def get_stream_stats(self) -> Tuple[int, int]:
        return (0, 0, 0) # Not implemented
    def clear_stream_stats(self):
        return # Not implemented
    def init_thread (self):
        pass
    def deinit_thread (self):
        pass
    def set_socket (self, sock: socket.socket):
        self.sock = sock
        self.sock.settimeout(0.1)

    def stop_thread (self):
        self.running = False

        self.thread.join()
    def start_thread (self, on_receive_end):
        def run_thread ():
            self.init_thread()

            while self.running:
                try:
                    res = self.sock.recv(1024)

                    on_receive_end(res)
                except socket.timeout:
                    pass
                
                start = time.time()
                while len(self.tx_buffer) > 0 and time.time() - start <= 0.1:
                    try:
                        sze = self.sock.send( self.tx_buffer.peek(1024) )
                        
                        self.tx_buffer.pop(sze)
                    except socket.timeout:
                        break
            
            self.deinit_thread()

        self.thread = threading.Thread(target=run_thread)
        self.thread.start()

class ServerSocketDevice (AbstractSocketDevice):
    def __init__(self, allow: str, port: int) -> None:
        super().__init__()

        self.allow = allow
        self.port  = port
    def init_thread(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.allow, self.port))
        self.server.listen(5)

        self.client, self.address = self.server.accept()

        self.set_socket(self.client)
    def deinit_thread(self):
        self.client.close()
        self.server.close()
    def get_name(self):
        return "Socket.Server"

class SimpleSocketDevice (AbstractSocketDevice):
    def __init__(self, host: str, port: int) -> None:
        super().__init__()

        self.host = host
        self.port = port
    def get_name(self):
        return "Socket.Client"
    def init_thread(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.host, self.port))

        self.set_socket(self.client)
    def deinit_thread(self):
        self.client.close()

