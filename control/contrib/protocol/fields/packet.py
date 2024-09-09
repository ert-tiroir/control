
from io import BytesIO
from typing import Self
from control.contrib.protocol.fields.field import Field

class MultiField(Field):
    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        cls.__meta_fields__ = []

        for key in dir(cls):
            fld = getattr(cls, key)

            if isinstance(fld, Field):
                cls.__meta_fields__.append( ( key, fld ) )
        
        cls.__meta_fields__.sort()
    def parse(self, reader: "BytesIO"):
        cls = type(self)
        res = cls()

        for key, field in cls.__meta_fields__:
            setattr(res, key, field.parse( reader ))
        
        return res
    def put(self, value: "Self", writer: "BytesIO"):
        cls = type(self)
        
        for key, field in cls.__meta_fields__:
            field.put( getattr(value, key), writer )
