
from io import BytesIO
from typing import Literal
from control.contrib.protocol.fields.field import Field

class IntegerField (Field):
    def __init__(self, length: int = 4, encoding: Literal["big"] | Literal["little"] = "big") -> None:
        self.length   = length
        self.encoding = encoding

        self.mxv: int = 2 ** (length * 8 - 1) - 1
        self.mnv: int = - 2 ** (length * 8 - 1)
        self.rng: int = 2 ** (length * 8)
    def parse(self, reader: BytesIO):
        value = reader.read( self.length )

        res = int.from_bytes(value, self.encoding)
        if res > self.mxv:
            res -= self.rng
        return res
    def put(self, value: int, writer: BytesIO):
        writer.write( (value % self.rng).to_bytes( self.length, self.encoding ) )