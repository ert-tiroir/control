
from control.contrib.protocol.fields.packet import MultiField
from control.contrib.protocol.fields.string import StringField


class EchoPacket(MultiField):
    content = StringField()

def handle_echo (packet: EchoPacket):
    from control.contrib.netc.app import NetControllerApplication
    packet.content += " Properly Received !"
    NetControllerApplication().send( packet )

net = [
    ("/echo", EchoPacket, handle_echo)
]
