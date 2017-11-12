#####################################################################
#
# buffers.py
#
# Copyright (c) 2017, Eran Egozy
#
# Released under the MIT License (http://opensource.org/licenses/MIT)
#
#####################################################################

import numpy as np


# First-in First-out buffer used for buffering audio data
class FIFOBuffer(object):
    def __init__(self, buf_size = 4096, buf_type = np.float):
        super(FIFOBuffer, self).__init__()

        self.buf_type = buf_type
        self.buffer = np.zeros(buf_size, dtype=buf_type)
        self.write_ptr = 0

    # how much space is available for writing
    def get_write_available(self):
        return len(self.buffer) - self.write_ptr

    # how much data is available for reading
    def get_read_available(self):
        return self.write_ptr

    # write 'signal' into buffer
    def write(self, signal):
        amt = len(signal)
        L = len(self.buffer)
        assert(self.write_ptr + amt <= L)
        self.buffer[self.write_ptr:self.write_ptr+amt] = signal
        self.write_ptr += amt

    # read 'amt' values from buffer
    def read(self, amt):
        assert(amt <= self.write_ptr)
        out = self.buffer[:amt].copy()
        remaining = self.write_ptr - amt
        self.buffer[0:remaining] = self.buffer[amt:self.write_ptr]
        self.write_ptr = remaining
        return out



def test_audio_buffer():
    ab = FIFOBuffer(50)
    assert( ab.get_write_available() == 50)
    assert( ab.get_read_available() == 0)

    ab.write(np.arange(0,25))
    assert( ab.get_read_available() == 25 )
    assert( (ab.read(20) == np.arange(0, 20)).all() )
    assert( ab.get_read_available() == 5 )
    assert( (ab.read(5) == np.arange(20, 25)).all() )

    ab.write(np.arange(0,40))
    assert( ab.get_read_available() == 40 )
    assert( (ab.read(20) == np.arange(0, 20)).all() )
    assert( ab.get_read_available() == 20 )
    assert( (ab.read(20) == np.arange(20, 40)).all() )
    assert( ab.get_read_available() == 0 )

    ab = FIFOBuffer(50)
    ab.write(np.arange(0,50))
    assert( ab.get_read_available() == 50 )
    assert( (ab.read(20) == np.arange(0, 20)).all() )
    assert( ab.get_read_available() == 30 )

    ab.write(np.arange(50,60))
    assert( ab.get_read_available() == 40 )
    assert( (ab.read(40) == np.arange(20, 60)).all() )
    assert( ab.get_read_available() == 0 )
    assert( ab.get_write_available() == 50 )

    ab.write(np.arange(0,50))
    assert( ab.get_read_available() == 50 )
    assert( (ab.read(20) == np.arange(0, 20)).all() )
    assert( ab.get_read_available() == 30 )

    ab.write(np.arange(50,60))
    assert( ab.get_read_available() == 40 )
    assert( (ab.read(40) == np.arange(20, 60)).all() )
    assert( ab.get_read_available() == 0 )
    assert( ab.get_write_available() == 50 )


# testing
if __name__ == "__main__":
    test_audio_buffer()
