#TSR
# REC_LEN U*2 Bytes of data following header
# REC_TYP U*1 Record type (10)
# REC_SUB U*1 Record sub-type (30)
# HEAD_NUM U*1 Test head number See note
# SITE_NUM U*1 Test site number
# TEST_TYP C*1 Test type space
# TEST_NUM U*4 Test number
# EXEC_CNT U*4 Number of test executions 4,294,967,295
# FAIL_CNT U*4 Number of test failures 4,294,967,295
# ALRM_CNT U*4 Number of alarmed tests 4,294,967,295
# TEST_NAM C*n Test name length byte = 0
# SEQ_NAME C*n Sequencer (program segment/flow) name length byte = 0
# TEST_LBL C*n Test label or text length byte = 0
# OPT_FLAG B*1 Optional data flag See note
# TEST_TIM R*4 Average test execution time in seconds OPT_FLAG bit 2 = 1
# TEST_MIN R*4 Lowest test result value OPT_FLAG bit 0 = 1
# TEST_MAX R*4 Highest test result value OPT_FLAG bit 1 = 1
# TST_SUMS R*4 Sumof test result values OPT_FLAG bit 4 = 1
# TST_SQRS R*4 Sum of squares of test result values OPT_FLAG bit 5 = 1

import struct
from typing import Optional, Dict

class TSRDecoder:
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
        """
        Decodes TSR fields in the order provided in your snippet.
        Adjust field sequence/types to match your STDF spec if needed.
        """
        head_num = self.read_u1()           # U*1
        site_num = self.read_u1()           # U*1
        test_typ = self.read_c1()           # C*1 (single char)
        test_num = self.read_u4()           # U*4
        exec_cnt = self.read_u4()           # U*4
        fail_cnt = self.read_u4()           # U*4
        alrm_cnt = self.read_u4()           # U*4
        x_coord  = self.read_i2()           # I*2 (signed 2-byte)
        y_coord  = self.read_i2()           # I*2 (signed 2-byte)
        test_t   = self.read_r4()           # R*4 (float seconds)

        # Strings (C*n)
        test_nam = self.read_cn()           # TEST_NAM
        seq_name = self.read_cn()           # SEQ_NAME
        test_lbl = self.read_cn()           # TEST_LBL

        out = {
            "REC_TYP": 10,                 # TSR typ (adjust if your spec differs)
            "REC_SUB": 30,                 # TSR sub (adjust if your spec differs)
            "RECORD_TYPE": "TSR",

            "HEAD_NUM": head_num,
            "SITE_NUM": site_num,
            "TEST_TYP": test_typ,
            "TEST_NUM": test_num,
            "EXEC_CNT": exec_cnt,
            "FAIL_CNT": fail_cnt,
            "ALRM_CNT": alrm_cnt,
            "X_COORD":  x_coord,
            "Y_COORD":  y_coord,
            "TEST_T":   test_t,

            "TEST_NAM": test_nam,
            "SEQ_NAME": seq_name,
            "TEST_LBL": test_lbl,
        }
        return out
