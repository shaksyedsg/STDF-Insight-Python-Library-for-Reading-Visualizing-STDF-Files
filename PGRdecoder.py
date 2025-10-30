import struct

class PGRDecoder:
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
        GRP_INDX = self.read('H', 2)
        GRP_NAME = self.read_str(20)
        INDX_CNT = self.read('H', 2)
        # Assuming pin indices follow, but need actual format to parse further

        return {
            'RECORD_TYPE': 'PGR',
            'REC_LEN': REC_LEN,
            'REC_TYP': REC_TYP,
            'REC_SUB': REC_SUB,
            'GRP_INDX': GRP_INDX,
            'GRP_NAME': GRP_NAME,
            'INDX_CNT': INDX_CNT,
            # 'PIN_INDX_LIST': [...]  # Optional: parse if format known
        }