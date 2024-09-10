
from io import BytesIO
from control.contrib.netc.socket import NetControllerSocket
from control.core import start_control, stop_control
from tests.contrib.netc.sample.echo_app.protocol import EchoPacket
from tests.decorator import wrap_test


@wrap_test
def test_echo_app ():
    start_control( "tests.contrib.netc.sample.echo_project__config", True )

    from control.contrib.netc.app import NetControllerApplication

    socket = NetControllerSocket()
    socket.connect('127.0.0.1', 5042)

    def send (content):
        app = NetControllerApplication()
        packet = EchoPacket()
        packet.content = content

        buffer = BytesIO()
        app.protocol.pid_field.put(0, buffer)
        EchoPacket.put( packet, packet, buffer )

        buffer = buffer.getvalue()
        header = BytesIO()
        app.protocol.sze_field.put( len(buffer), header )

        socket.send(header.getvalue() + buffer)
        return packet
    def receive (initial: EchoPacket):
        app = NetControllerApplication()
        data = socket.receive(app.protocol)
        print(data)

        sze = app.protocol.sze_field.parse(BytesIO(data[:8]))
        pid = app.protocol.pid_field.parse(BytesIO(data[8:9]))
        assert pid == 0

        packet = EchoPacket().parse( BytesIO(data[9:]) )
        print(packet, packet.content, initial.content)

        assert packet.content == initial.content + " Properly Received !"
    
    receive( send("Hello, Server !") )

    socket.close()

    stop_control()

