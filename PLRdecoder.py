import struct

class PLRDecoder:
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

    def read_bytes(self, length: int):
        val = self.data[self.offset:self.offset + length]
        self.offset += length
        return val

    def decode(self) -> dict:
        REC_LEN = self.read('H', 2)
        REC_TYP = self.read('B', 1)
        REC_SUB = self.read('B', 1)
        GRP_CNT = self.read('H', 2)

        GRP_MODE = self.read_bytes(GRP_CNT)
        GRP_RADX = self.read_bytes(GRP_CNT)
        PGM_CHAR = self.read_bytes(GRP_CNT)
        RTN_CHAR = self.read_bytes(GRP_CNT)

        return {
            'RECORD_TYPE': 'PLR',
            'REC_LEN': REC_LEN,
            'REC_TYP': REC_TYP,
            'REC_SUB': REC_SUB,
            'GRP_CNT': GRP_CNT,
            'GRP_MODE': GRP_MODE,
            'GRP_RADX': GRP_RADX,
            'PGM_CHAR': PGM_CHAR,
            'RTN_CHAR': RTN_CHAR,
        }