#PRR
# REC_LEN U*2 Bytes of data following header
# REC_TYP U*1 Record type (5)
# REC_SUB U*1 Record sub-type (20)
# HEAD_NUM U*1 Test head number
# SITE_NUM U*1 Test site number
# PART_FLG B*1 Part information flag
# NUM_TEST U*2 Number of tests executed
# HARD_BIN U*2 Hardware bin number
# SOFT_BIN U*2 Software bin number 65535
# X_COORD I*2 (Wafer) X coordinate -32768
# Y_COORD I*2 (Wafer) Y coordinate -32768
# TEST_T U*4 Elapsed test time in milliseconds 0
# PART_ID C*n Part identification length byte = 0
# PART_TXT C*n Part description text length byte = 0
# PART_FIX B*n Part repair information length byte = 0

import struct

class PRRDecoder:

    def __init__(self, data: bytes):
        self.data = data
        self.offset = 0

    def read(self, fmt: str):
        """Read numeric value per 'fmt' and advance by its size."""
        size = struct.calcsize(fmt)
        if self.offset + size > len(self.data):
            return None
        val = struct.unpack_from(fmt, self.data, self.offset)[0]
        self.offset += size
        return val

    def read_c1(self) -> str:
        """Read a single character (C*1)."""
        if self.offset >= len(self.data):
            return 'NaN'
        b = self.data[self.offset:self.offset+1]
        self.offset += 1
        return b.decode('ascii', errors='replace')

    def read_cn(self, encoding: str = 'ascii') -> str:

        length = self.read('<B')  # U*1 length byte
        if length is None:
            return 'NaN'
        if length == 0:
            return ''
        if self.offset + length > len(self.data):
            return 'NaN'
        raw = self.data[self.offset:self.offset + length]
        self.offset += length
        return raw.decode(encoding, errors='replace')

    def decode(self) -> dict:
    
        # ---- Numeric + single-char segment ----
        head_num  = self.read('<B')   # U*1
        site_num  = self.read('<B')   # U*1
        part_flg = self.read('<B')   # U*1
        num_test = self.read('<H')   # U*2
        hard_bin = self.read('<H')   # U*2
        soft_bin = self.read('<H')   # U*2
        x_coord = self.read('<h')   # I*2
        y_coord = self.read('<h')   # I*2
        test_t = self.read('<I')   # U*4

        # (C*n) 
        fields_order = [
            'PART_ID', 'PART_TXT', 'PART_FIX'
        ]  
        out = {
            'HEAD_NUM' : head_num, 'SITE_NUM' : site_num, 'PART_FLG' : part_flg, 'NUM_TEST' : num_test, 'HARD_BIN' : hard_bin, 'SOFT_BIN' : soft_bin,
            'X_COORD' : x_coord, 'Y_COORD' : y_coord, 'TEST_T' : test_t
        }
        for name in fields_order:
            out[name] = self.read_cn()
            
            out["REC_TYP"] = 5   # PRR typ
            out["REC_SUB"] = 10  # PRR sub
            out["RECORD_TYPE"] = "PRR"

        return out
