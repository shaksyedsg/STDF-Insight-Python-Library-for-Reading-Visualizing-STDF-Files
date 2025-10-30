import struct

class PRRDecoder:
    def __init__(self, data: bytes):
        self.data = data
        self.offset = 0

    def read(self, fmt: str, size: int):
        try:
            val = struct.unpack_from(fmt, self.data, self.offset)[0]
            self.offset += size
            return val
        except:
            return None

    def read_str(self, length: int):
        try:
            s = self.data[self.offset:self.offset + length].decode(errors='replace')
            self.offset += length
            return s.strip()
        except:
            return 'NaN'

    def decode(self) -> dict:
        REC_LEN = self.read('H', 2)
        REC_TYP = self.read('B', 1)
        REC_SUB = self.read('B', 1)
        HEAD_NUM = self.read('B', 1)
        SITE_NUM = self.read('B', 1)
        PART_FLG = self.read('B', 1)
        NUM_TEST = self.read('H', 2)
        HARD_BIN = self.read('H', 2)
        SOFT_BIN = self.read('H', 2)
        X_COORD = self.read('h', 2)
        Y_COORD = self.read('h', 2)
        TEST_T = self.read('i', 4)
        PART_ID_LEN = self.read('B', 1)
        PART_ID = self.read_str(PART_ID_LEN)
        PART_TXT_LEN = self.read('B', 1)
        PART_TXT = self.read_str(PART_TXT_LEN)
        PART_FIX_LEN = self.read('B', 1)
        PART_FIX = self.read_str(PART_FIX_LEN)

        return {
            'RECORD_TYPE': 'PRR',
            'REC_LEN': REC_LEN,
            'REC_TYP': REC_TYP,
            'REC_SUB': REC_SUB,
            'HEAD_NUM': HEAD_NUM,
            'SITE_NUM': SITE_NUM,
            'PART_FLG': PART_FLG,
            'NUM_TEST': NUM_TEST,
            'HARD_BIN': HARD_BIN,
            'SOFT_BIN': SOFT_BIN,
            'X_COORD': X_COORD,
            'Y_COORD': Y_COORD,
            'TEST_T': TEST_T,
            'PART_ID': PART_ID,
            'PART_TXT': PART_TXT,
            'PART_FIX': PART_FIX,
        }
