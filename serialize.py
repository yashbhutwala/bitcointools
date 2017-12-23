#!/usr/bin/env python3
#
# Copyright (c) 2017 John Newbery
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

from io import BufferedReader
import struct

class BCBytesStream():
    """A class that provides additional serialization and deserialization methods
    over a base BufferedReader class.

    The BufferedReader object is class member _br and all unknown method
    calls are passed to _br"""

    def __init__(self, br):
        """Must be initialized with a BufferedReader."""
        assert type(br) == BufferedReader
        self._br = br

    def __getattr__(self, name):
        return getattr(self._br, name)

    def __enter__(self, *args, **kwargs):
        self._br.__enter__(*args, **kwargs)
        return self

    def __exit__(self, *args, **kwargs):
        return self._br.__exit__(*args, **kwargs)

    def deser_boolean(self):
        return struct.unpack("?", self.read(1))[0]

    def ser_boolean(self, val):
        self.write(struct.pack("?", val))

    def deser_int8(self):
        return struct.unpack("<b", self.read(1))[0]

    def ser_int8(self, val):
        self.write(struct.pack("<b", val))

    def deser_uint8(self):
        return struct.unpack("<B", self.read(1))[0]

    def ser_uint8(self, val):
        self.write(struct.pack("<B", val))

    def deser_int16(self):
        return struct.unpack("<h", self.read(2))[0]

    def ser_int16(self, val):
        self.write(struct.pack("<h", val))

    def deser_uint16(self, big=False):
        fmt = ">" if big else "<"
        fmt += "H"
        return struct.unpack(fmt, self.read(2))[0]

    def ser_uint16(self, val):
        self.write(struct.pack("<H", val))

    def deser_int32(self):
        return struct.unpack("<i", self.read(4))[0]

    def ser_int32(self, val):
        self.write(struct.pack("<i", val))

    def deser_uint32(self):
        return struct.unpack("<I", self.read(4))[0]

    def ser_uint32(self, val):
        self.write(struct.pack("<I", val))

    def deser_int64(self):
        return struct.unpack("<q", self.read(8))[0]

    def ser_int64(self, val):
        self.write(struct.pack("<q", val))

    def deser_uint64(self):
        return struct.unpack("<Q", self.read(8))[0]

    def ser_uint64(self, val):
        self.write(struct.pack("<Q", val))

    def deser_uint256(self):
        r = 0
        for i in range(8):
            t = struct.unpack("<I", self.read(4))[0]
            r += t << (i * 32)
        return r

    def ser_uint256(self, val):
        rs = b""
        for i in range(8):
            rs += struct.pack("<I", val & 0xFFFFFFFF)
            val >>= 32
        self.write(rs)

    def deser_compact_size(self):
        nit = struct.unpack("<B", self.read(1))[0]
        if nit == 253:
            nit = struct.unpack("<H", self.read(2))[0]
        elif nit == 254:
            nit = struct.unpack("<I", self.read(4))[0]
        elif nit == 255:
            nit = struct.unpack("<Q", self.read(8))[0]
        return nit

    def ser_compact_size(self, val):
        r = b""
        if val < 253:
            r = struct.pack("B", val)
        elif val < 0x10000:
            r = struct.pack("<BH", 253, val)
        elif val < 0x100000000:
            r = struct.pack("<BI", 254, val)
        else:
            r = struct.pack("<BQ", 255, val)
        self.write(r)

def open_bs(path, mode):
    f = open(path, mode + 'b')
    return BCBytesStream(f)