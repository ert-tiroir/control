
from io import BytesIO
from typing import Self


class Field:
    def parse (self, reader: "BytesIO"):
        raise NotImplementedError()
    def put (self, value: "Self", writer: "BytesIO"):
        raise NotImplementedError()
