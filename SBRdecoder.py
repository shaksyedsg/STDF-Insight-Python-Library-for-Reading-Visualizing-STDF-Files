import struct

class SBRDecoder:
    def __init__(self, data: bytes):
        self.data = data
        self.offset = 0

    def read(self, fmt: str, size: int):
        try:
            val = struct.unpack_from(fmt, self.data, self.offset)[0]
            self.offset += size
            return val
        except (struct.error, IndexError):
            return None

    def read_str(self, length: int):
        try:
            s = self.data[self.offset:self.offset + length].decode(errors='replace')
            self.offset += length
            return s.strip()
        except (IndexError, UnicodeDecodeError):
            return 'NaN'

    def decode(self) -> dict:
        REC_LEN = self.read('H', 2)
        REC_TYP = self.read('B', 1)
        REC_SUB = self.read('B', 1)
        HEAD_NUM = self.read('B', 1)
        SITE_NUM = self.read('B', 1)
        SBIN_NUM = self.read('H', 2)
        SBIN_CNT = self.read('I', 4)
        SBIN_PF = self.read_str(1)
        SBIN_NAM = self.read_str(REC_LEN - 12)  # Adjust based on actual length

        return {
            'RECORD_TYPE': 'SBR',
            'REC_LEN': REC_LEN,
            'REC_TYP': REC_TYP,
            'REC_SUB': REC_SUB,
            'HEAD_NUM': HEAD_NUM,
            'SITE_NUM': SITE_NUM,
            'SBIN_NUM': SBIN_NUM,
            'SBIN_CNT': SBIN_CNT,
            'SBIN_PF': SBIN_PF,
            'SBIN_NAM': SBIN_NAM,
        }