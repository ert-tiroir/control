
import socket
import threading
from control.contrib.netc.socket import NetControllerSocket
from control.contrib.protocol.abstract import AbstractProtocolApp
from control.core.app import Application
from control.utils.logger import Logger

class NetControllerApplication (Application):
    def prepare_application(self):
        self.protocol = AbstractProtocolApp( "protocol", "net", "_packet_net_index" )
        self.protocol.init_protocol()

        self.closed = False

        self.logs = Logger("logs/netc/application.txt")

    def run_thread (self):
        try:
            self.logs.success("Succesfully created thread")
            self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.serversocket.bind(('', 5042))
            self.serversocket.listen(5)
            self.serversocket.settimeout(0.1)
            self.logs.success("Succesfully created server socket")

            while not self.closed:
                try:
                    client, address = self.serversocket.accept()
                    client.settimeout(0.1)
                    self.logs.success("New client connected to the network")
                except socket.timeout:
                    continue
                self.client = NetControllerSocket(client)

                while not self.closed:
                    if len(self.protocol.send_buffer) != 0:
                        if not self.client.send(
                            self.protocol.send_buffer.pop(
                                len(self.protocol.send_buffer)) ):
                            self.logs.error("NetControllerApplication: No data sent, connection will be reset")
                            break
                    try:
                        result = self.client.receive(self.protocol)
                    except socket.timeout:
                        continue
                    except OSError as error:
                        self.logs.error("NetControllerApplication:", str(error))
                        self.logs.error("Client connection will be reset")
                        if self.client is not None:
                            self.client.close()
                            self.client = None
                        break
                    if result == b'':
                        self.logs.error("NetControllerApplication: No data received, connection will be reset")
                        break

                    self.protocol.recv_buffer.put(result)
                    self.protocol.check_receive()

                if self.client is not None:
                    self.client.close()
                    self.client = None
        except OSError as error:
            self.logs.critical("NetControllerApplication: " + str(error))
            self.logs.critical("The server will be closed due to this error")
        self.logs.info("Thread has been stopped")
        
        self.serversocket.close()
    
    def send (self, packet):
        self.protocol.send(packet)
    def init_application(self):
        def run_thread ():
            NetControllerApplication().run_thread()
        self.thread = threading.Thread( target=run_thread )
        self.thread.start()
    def stop_application(self):
        self.logs.info("Asking for the thread to stop")
        self.closed = True
        if hasattr(self, "serversocket"):
            self.serversocket.close()
        if hasattr(self, "client") and self.client is not None:
            client = self.client
            self.client = None
            client.close()
        if hasattr(self, "thread") and self.thread.is_alive():
            self.thread.join()
