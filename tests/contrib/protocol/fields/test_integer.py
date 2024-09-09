
from io import BytesIO
import random
from control.contrib.protocol.fields.integer import IntegerField
from tests.decorator import wrap_test

def custom_int_encoding (value: int, length: int) -> bytes:
    if length <= 0: return b''

    result = []
    while length > 0:
        result.append(value % 256)
        length -= 1
        value //= 256
    result.reverse()
    return bytes(result)

@wrap_test
def test_integer_field ():
    for size in range (1, 10):
        mxv = 2 ** (size * 8 - 1) - 1
        mnv = - 2 ** (size * 8 - 1)

        for enc in [ 'big', 'little' ]:
            field1 = IntegerField(size, enc)
            field2 = IntegerField(size, enc)

            for _t in range(100):
                val = random.randint(mnv, mxv)
                
                wrt = BytesIO()
                field1.put( val, wrt )
                rst = wrt.getvalue()

                assert len(rst) == size

                exp = custom_int_encoding((val + 2 ** (size * 8)) % (2 ** (size * 8)), size)
                if enc == "little": exp = bytes(reversed(list(exp)))
                assert rst == exp
                
                res = field2.parse( BytesIO(rst) )
                assert val == res
