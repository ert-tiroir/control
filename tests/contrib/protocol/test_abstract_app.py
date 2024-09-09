
from control.contrib.protocol.abstract import AbstractProtocolApp
from control.contrib.protocol.fields.integer import IntegerField
from control.contrib.protocol.fields.packet import MultiField
from control.contrib.protocol.fields.string import StringField
from control.utils.bytequeue import ByteQueue
from tests.decorator import wrap_test


@wrap_test
def test_init_protocol ():
    global buffer
    class F(MultiField):
        a = IntegerField()
        b = StringField()

        def setup(self, a, b):
            self.a, self.b = a, b
            return self
    class G(MultiField):
        a = IntegerField()
        b = IntegerField()

        def setup(self, a, b):
            self.a, self.b = a, b
            return self
    app = AbstractProtocolApp( "", "", "_packet_index" )
    app.send_buffer = ByteQueue()
    app.recv_buffer = app.send_buffer

    buffer = []

    def handle (x):
        global buffer
        print(x)
        buffer.append(x)
    
    app.protocol = [
        ("simple",  F, handle),
        ("complex", G, handle)
    ]
    app.pid_field = IntegerField(len(app.protocol))
    app.sze_field = IntegerField(8)
    F._packet_index = 0
    G._packet_index = 1
    def send (packet):
        app.send(packet)

    def recv (packet, present=True):
        global buffer
        app.check_receive()

        if not present:
            assert len(buffer) == 0
            return

        assert len(buffer) != 0
        pR = buffer[0]
        buffer = buffer[1:]

        assert type(packet) == type(pR)
        assert packet.a == pR.a
        assert packet.b == pR.b

    p1 = F().setup(0, "2")
    p2 = G().setup(0, 1)
    p3 = F().setup(1, "abc")

    send(p1)
    send(p2)
    send(p3)
    recv(p1)
    recv(p2)
    recv(p3)
    
    send(p1)
    recv(p1)
    send(p2)
    recv(p2)
    send(p3)
    recv(p3)

    recv(p1, False)
    send(p1)
    recv(p1)