
from io import BytesIO
from control.contrib.protocol.fields.bytes import BytesField
from tests.contrib.protocol.fields.test_integer import custom_int_encoding
from tests.decorator import wrap_test

import random

@wrap_test
def test_byte_encoding ():
    for size in ( list(range(10, 100, 10)) + list(range(100, 1000, 100)) + [ 100_000 ] ):
        field = BytesField(100_001)
        
        value = bytes([ random.randint(0, 255) for _ in range(size) ])
        expected = custom_int_encoding(size, 3) + value

        wrt = BytesIO()
        field.put( value, wrt )
        rst = wrt.getvalue()

        assert rst == expected
    
    for x in range(1, 256 * 256 + 1):
        field = BytesField(x)

        y = 1
        if x >= 128:
            y = 2
        if x >= 256 * 128:
            y = 3
        assert field.subint.length == y