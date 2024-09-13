
# eSPI is the enhanced version of SPI used by the Nordli project

import threading
import time
from typing import Any, Callable, List
from control.contrib.sensors.device import AbstractDevice

import board
import digitalio
from control.utils.bytequeue import ByteQueue

WAIT_GPIO = 0.000_001 # 1 micro seconds = about 700 cycles of cpu, the time to give back the hand to the kernel
BUFR_SIZE = 1024
MIN_QSIZE = 1023

# Used for intellisense
class _GPIO:
    @property
    def direction (self) -> Any: ...
    @direction.setter
    def direction (self, value: Any): ...
    @property
    def value (self) -> bool: ...
    @value.setter
    def value (self, value: bool): ...

class _SPI:
    def try_lock (self): ...
    def write_readinto (self, tx: List[int], rx: List[int]): ...
    def unlock(self): ...

class ESpiDevice(AbstractDevice):
    master_request: _GPIO

    slave_request0 : _GPIO
    slave_request1 : _GPIO

    request_offset : int

    spi: _SPI

    on_recv: Callable[[bytes], Any]

    def __init_slave (self):
        if self.request_offset == -1:
            if self.slave_request0.value:
                self.request_offset = 0
            elif self.slave_request1.value:
                self.request_offset = 1

            return self.request_offset != -1
        return True
    @property
    def slave_request (self):
        if not self.__init_slave(): return False
        
        if self.request_offset == 0:
            return self.slave_request0.value
        else:
            return self.slave_request1.value

    def init_device(self):
        self.spi = board.SPI()

        self.tx_queue = ByteQueue()

        # The transfer event is forwarded to the transfer thread
        # It can happen in 3 cases :
        #  - Either the queue contains at least 1023 bytes (a SPI packet being 1024)
        #  - Either the slave has requested to send data
        #  - Either the thread has been closed
        self.tx_event = threading.Event()
        self.gp_lock  = threading.Lock ()

        self.slave_request0 = digitalio.DigitalInOut(board.D4)
        self.slave_request1 = digitalio.DigitalInOut(board.D17)
        
        self.master_request = digitalio.DigitalInOut(board.D27)
        self.master_request.direction = digitalio.Direction.OUTPUT

        self.request_offset = -1

        self.tx_buffer = [0] * BUFR_SIZE
        self.rx_buffer = [0] * BUFR_SIZE

        self.running = False
        return 

    def get_name (self):
        return "eSPI Device"

    def start_transfer (self, buffer: bytes):
        self.tx_queue.put(buffer)

        if len(self.tx_queue) >= MIN_QSIZE:
            self.tx_event.set()
    
    def start_tx_thread (self):
        while True:
            self.tx_event.wait()
            if not self.running: break

            with self.gp_lock:
                if len(self.tx_queue) >= MIN_QSIZE:
                    self.tx_buffer[0] = 1
                    self.master_request.value = True

                    buffer = self.tx_queue.pop(MIN_QSIZE)
                    for index in range(len(buffer)):
                        self.tx_buffer[index + 1] = buffer[index]
                
                while not self.slave_request:
                    time.sleep(WAIT_GPIO)

                self.master_request.value = False
                self.spi.try_lock()
                self.spi.write_readinto(self.tx_buffer, self.rx_buffer)
                self.spi.unlock()

                if self.rx_buffer[0] != 0:
                    self.on_recv( bytes(self.rx_buffer[1:]) )
                self.request_offset = (self.request_offset + 1) & 1

                self.tx_buffer[0] = 0
                self.tx_event.clear()
    def start_watch_thread (self):
        while self.running:
            with self.gp_lock:
                if self.slave_request:
                    self.tx_event.set()
            time.sleep(WAIT_GPIO)

    def stop_thread (self):
        self.running = False
        self.tx_event.set()

        self.wt_thread.join()
        self.tx_thread.join()
    def start_thread (self, on_receive_end):
        def run_tx_thread ():
            self.start_tx_thread()
        def run_watch_thread ():
            self.start_watch_thread()
        self.running   = True
        self.on_recv   = on_receive_end
        self.tx_thread = threading.Thread( target=run_tx_thread )
        self.wt_thread = threading.Thread( target=run_watch_thread )

        self.tx_thread.start()
        self.wt_thread.start()