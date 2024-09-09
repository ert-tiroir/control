
from io import BytesIO
import random

from control.contrib.protocol.fields.number import DoubleField, FloatField
from tests.decorator import wrap_test

@wrap_test
def test_float ():
    field1 = FloatField()
    field2 = FloatField()
    for _t in range(500_000):
        x = (-1) ** (random.randint(0, 1)) * (1 + random.random()) * ( 2 ** random.randint( -128, 127 ) )

        wrt = BytesIO()
        field1.put(x, wrt)

        bts = wrt.getvalue()

        res = field2.parse(BytesIO(bts))

        assert abs((res - x) / x) <= (2 ** -22)

@wrap_test
def test_double ():
    field1 = DoubleField()
    field2 = DoubleField()
    for _t in range(500_000):
        x = (-1) ** (random.randint(0, 1)) * (1 + random.random()) * ( 2 ** random.randint( -1024, 1023 ) )

        wrt = BytesIO()
        field1.put(x, wrt)

        bts = wrt.getvalue()

        res = field2.parse(BytesIO(bts))

        assert abs((res - x) / x) <= (2 ** -52)
