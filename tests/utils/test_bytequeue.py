
from control.utils.bytequeue import ByteQueue
from tests.decorator import should_be_fast, wrap_test

import random

@wrap_test
@should_be_fast(5) # About 1s per adding 128 times 1M buffer
def test_fast_insertion():
    queue = ByteQueue()
    F = bytes(
        [ random.randint(0, 255) for _ in range(1_000_000) ]
    )

    for _t in range(128):
        queue.put ( F )

    assert len(queue) == 128_000_000

@wrap_test
@should_be_fast(5) # About 0.5s per 1_000_000 grab on 128M buffer
def test_fast_single_deletion ():
    queue = ByteQueue()
    F = bytes(
        [ random.randint(0, 255) for _ in range(1_000_000) ]
    )
    
    for _t in range(128):
        queue.put ( F )
    
    _v = 0
    for _t in range (1_000_000):
        assert queue.pop(1)[0] == F[_v]
        assert len(queue) == 128_000_000 - 1 - _t
        _v += 1
        if _v == len(F): _v = 0

@wrap_test
@should_be_fast(5) # Took 0.8s so more or less really fast
def test_fast_1K_chunk_deletion ():
    queue = ByteQueue()
    F = bytes(
        [ random.randint(0, 255) for _ in range(1_000_000) ]
    )

    for _t in range(128):
        queue.put ( F )

    for _t in range(1_000):
        assert list(queue.pop(1000)) == list(F[_t * 1000: _t * 1000 + 1000])
        assert len(queue) == 128_000_000 - _t * 1000 - 1000

@wrap_test
@should_be_fast(5) # About 60K packets (of size 293) / second
def test_when_data_is_added ():
    queue = ByteQueue()
    F = bytes([0] * 1024)

    status = False

    for _t in range(25_000):
        queue.put(F)
        
        while True:
            if not status and len(queue) >= 8:
                _size = queue.pop(8)
                status = True
            elif status and len(queue) >= 293:
                _val = queue.pop(293)
                res = 0
                for x in _val:
                    res = (res + x + 3) ^ 7
                status = False
            else:
                break