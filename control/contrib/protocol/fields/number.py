
from io import BytesIO
import struct
from typing import Any
from control.contrib.protocol.fields.field import Field

class _StructField (Field):
    def __init__(self, target: str, size: int) -> None:
        self.target = target
        self.size   = size
    def parse(self, reader: BytesIO):
        value: bytes = reader.read(self.size)

        return struct.unpack( self.target, value )[0]
    def put(self, value: Any, writer: BytesIO):
        value = struct.pack( self.target, value )

        writer.write(value)

class FloatField(_StructField):
    def __init__(self) -> None:
        super().__init__("f", 4)

class DoubleField(_StructField):
    def __init__(self) -> None:
        super().__init__("d", 8)
