#HBR
# REC_LEN U*2 Bytes of data following header
# REC_TYP U*1 Record type (1)
# REC_SUB U*1 Record sub-type (40)
# HEAD_NUM U*1 Test head number See note
# SITE_NUM U*1 Test site number
# HBIN_NUM U*2 Hardware bin number
# HBIN_CNT U*4 Number of parts in bin
# HBIN_PF C*1 Pass/fail indication space
# HBIN_NAM C*n Name of hardware bin length byte = 0

import struct
from typing import Optional, Dict

class HBRDecoder:

    def __init__(self, data: bytes, endian: str = '<'):
        """
        :param data: Raw TSR record payload (after REC_LEN/REC_TYP/REC_SUB).
        :param endian: '<' for little-endian, '>' for big-endian (from FAR).
        """
        assert endian in ('<', '>'), "Endianness must be '<' or '>'"
        self.data = data
        self.offset = 0
        self.endian = endian

    # --- low-level helpers ---
    def _read_exact(self, n: int) -> Optional[bytes]:
        if self.offset + n > len(self.data):
            return None
        b = self.data[self.offset:self.offset + n]
        self.offset += n
        return b

    def read(self, fmt: str):
        """Read numeric value using struct fmt and advance."""
        size = struct.calcsize(fmt)
        raw = self._read_exact(size)
        if raw is None:
            return None
        return struct.unpack_from(fmt, raw, 0)[0]

    # --- primitives for STDF types ---
    def read_u1(self) -> Optional[int]:
        raw = self._read_exact(1)
        return None if raw is None else struct.unpack('B', raw)[0]

    def read_c1(self) -> str:
        """C*1: single ASCII character."""
        raw = self._read_exact(1)
        if raw is None:
            return ''
        # 'c' also works: struct.unpack('c', raw)[0].decode('ascii', errors='replace')
        return raw.decode('ascii', errors='replace')

    def read_u2(self) -> Optional[int]:
        return self.read(self.endian + 'H')

    def read_i2(self) -> Optional[int]:
        return self.read(self.endian + 'h')

    def read_u4(self) -> Optional[int]:
        return self.read(self.endian + 'I')

    def read_r4(self) -> Optional[float]:
        return self.read(self.endian + 'f')

    def read_cn(self, encoding: str = 'ascii') -> str:
        """
        C*n: U*1 length followed by n bytes of text.
        Returns empty string if missing/zero length.
        """
        length = self.read_u1()
        if length is None or length == 0:
            return ""
        raw = self._read_exact(length)
        if raw is None:
            return ""
        return raw.decode(encoding, errors='replace')

    # --- main decode ---
    def decode(self) -> Dict[str, object]:

        head_num = self.read_u1()           # U*1
        site_num = self.read_u1()           # U*1
        hbin_num = self.read('<H')          # U*2 
        hbin_cnt = self.read_u4()           # U*4
        hbin_pf = self.read_c1()            # C*1 (single char)

        # Strings (C*n)
        hbin_nam = self.read_cn()           # TEST_NAM

        out = {
            "REC_TYP": 1,                 # TSR typ (adjust if your spec differs)
            "REC_SUB": 40,                 # TSR sub (adjust if your spec differs)
            "RECORD_TYPE": "HBR",

            "HEAD_NUM": head_num,
            "SITE_NUM": site_num,
            "HBIN_NUM": hbin_num,
            "HBIN_CNT": hbin_cnt,
            "HBIN_PF": hbin_pf,

            "HBIN_NAME": hbin_nam,

        }
        return out


