import struct

class PMRDecoder:
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
        PMR_INDX = self.read('H', 2)
        CHAN_TYP = self.read('H', 2)
        CHAN_NAM = self.read_str(20)
        PHY_NAM = self.read_str(20)
        LOG_NAM = self.read_str(20)
        HEAD_NUM = self.read('B', 1)
        SITE_NUM = self.read('B', 1)

        return {
            'RECORD_TYPE': 'PMR',
            'REC_LEN': REC_LEN,
            'REC_TYP': REC_TYP,
            'REC_SUB': REC_SUB,
            'PMR_INDX': PMR_INDX,
            'CHAN_TYP': CHAN_TYP,
            'CHAN_NAM': CHAN_NAM,
            'PHY_NAM': PHY_NAM,
            'LOG_NAM': LOG_NAM,
            'HEAD_NUM': HEAD_NUM,
            'SITE_NUM': SITE_NUM,
        }