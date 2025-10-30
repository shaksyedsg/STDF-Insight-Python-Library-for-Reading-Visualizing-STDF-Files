import struct

class HBRDecoder:
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

    def decode(self) -> dict:
        REC_LEN = self.read('H', 2)
        REC_TYP = self.read('B', 1)
        REC_SUB = self.read('B', 1)
        HEAD_NUM = self.read('B', 1)
        SITE_NUM = self.read('B', 1)
        HBIN_NUM = self.read('H', 2)
        HBIN_CNT = self.read('H', 2)
        HBIN_PF = self.read('B', 1)

        return {
            'RECORD_TYPE': 'HBR',
            'REC_LEN': REC_LEN,
            'REC_TYP': REC_TYP,
            'REC_SUB': REC_SUB,
            'HEAD_NUM': HEAD_NUM,
            'SITE_NUM': SITE_NUM,
            'HBIN_NUM': HBIN_NUM,
            'HBIN_CNT': HBIN_CNT,
            'HBIN_PF': HBIN_PF,
        }