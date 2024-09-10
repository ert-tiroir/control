
from io import BytesIO
from control.contrib.protocol.fields.integer import IntegerField
from control.contrib.protocol.fields.packet import MultiField
from control.core.app import ApplicationManager
from control.utils.bytequeue import ByteQueue


class AbstractProtocolApp:
    def __init__(self, module: str, varname: str, indexname: str):
        self.__module_name__ = module
        self.__var_name__    = varname
        self.__index_name__  = indexname
    def init_protocol (self):
        manager = ApplicationManager()

        self.send_buffer = ByteQueue()
        self.recv_buffer = ByteQueue()

        protocol = []

        for application in manager.applications:
            prt_module = application.load_module(self.__module_name__)
            if prt_module is None: continue 

            if not hasattr(prt_module, self.__var_name__):
                print(f"WARNING could not find {self.__var_name__} in {application.path}.protocol")
                continue

            protocol.extend(getattr(prt_module, self.__var_name__))

        self.protocol = protocol
        if len(protocol) == 0:
            print(f"WARNING No packets found project-wide")
            return
        self.protocol.sort()
        
        for index, (name, cls, handler) in enumerate(protocol):
            setattr(cls, self.__index_name__, index)
        self.pid_field = IntegerField(len(protocol))
        self.sze_field = IntegerField(8)

    def send (self, packet: MultiField):
        if not hasattr(type(packet), self.__index_name__):
            raise TypeError("The packet has no packet index, maybe you forgot to register it in the according module of your app")
        _packet_index = getattr(type(packet), self.__index_name__)

        if not isinstance(_packet_index, int) \
        or _packet_index < 0 or _packet_index >= len(self.protocol) \
        or self.protocol[_packet_index][1] != type(packet):
            raise TypeError("The packet has a packet index object, but is either not an int, too big, negative, or does not link to the same registered class")
        bytes = BytesIO()

        packet.put(packet, bytes)
        data = bytes.getvalue()

        header = BytesIO()

        self.sze_field.put(len(data) + self.pid_field.length, header)
        self.pid_field.put(_packet_index, header)

        buffer = header.getvalue() + data
        print("Sending ", buffer)
        self.send_buffer.put(buffer)
    def check_receive (self):
        while True:
            print(self.recv_buffer.peek(8))
            sze_buffer = BytesIO(self.recv_buffer.peek(8))

            sze = self.sze_field.parse(sze_buffer)
            print(sze)
            if sze + 8 > len(self.recv_buffer): return # There is no more data

            self.recv_buffer.pop(8)
            sze -= self.pid_field.length
            header = BytesIO( self.recv_buffer.pop( self.pid_field.length ) )
            
            pid = self.pid_field.parse( header )
            print(pid)
            
            data = BytesIO( self.recv_buffer.pop( sze ) )
            print(data)

            name, packet_type, handler = self.protocol[pid]
            try:
                packet = packet_type().parse( data )
            except Exception as e:
                break
            handler(packet)

    def stop_protocol (self):
        pass
