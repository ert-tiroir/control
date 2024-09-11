
from io import BytesIO
from control.contrib.protocol.fields.bytes import BytesField
from control.contrib.protocol.fields.field import Field

class StringField(Field):
    def __init__(self, encoding = "utf-8", max_bsize = 2 ** 31 - 1):
        self.subfield = BytesField(max_bsize)
        self.encoding = encoding
    
    def parse(self, reader: BytesIO):
        bytes = self.subfield.parse( reader )

        return bytes.decode( self.encoding )
    def put(self, value: str, writer: BytesIO):
        bts = bytes(value, encoding=self.encoding)

        self.subfield.put(bts, writer)
    def manifest(self):
        return {
            "type": "string",
            "encoding": self.encoding,
            "subbytes": self.subfield.manifest()
        }