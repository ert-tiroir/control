
from io import BytesIO
from control.contrib.protocol.fields.field import Field
from control.contrib.protocol.fields.integer import IntegerField

def get_factor (size):
    factor = 1
    intsze = 0
    while factor < 2 * size + 3:
        factor *= 256
        intsze += 1
    return intsze
class BytesField (Field):
    def __init__(self, max_size = 2 ** 31 - 1):
        self.intsze = 0
        factor = 1
        while factor < max_size * 2 + 1: # Avoid sign issues
            factor *= 256
            self.intsze += 1
        self.max_size = max_size
        self.subint = IntegerField( self.intsze, "big" )
    def parse (self, reader: BytesIO):
        size = self.subint.parse( reader )

        return reader.read(size)
    def put(self, value: bytes, writer: BytesIO):
        assert len(value) < self.max_size
        self.subint.put(len(value), writer)

        writer.write( value )
    def manifest(self):
        return {
            "type": "bytes",
            "size": self.max_size,
            "subint": self.subint.manifest()
        }
