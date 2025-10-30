import struct

class FARDecoder:
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
        CPU_TYPE = self.read('B', 1)
        STDF_VER = self.read('B', 1)

        return {
            'RECORD_TYPE': 'FAR',
            'REC_LEN': REC_LEN,
            'REC_TYP': REC_TYP,
            'REC_SUB': REC_SUB,
            'CPU_TYPE': CPU_TYPE,
            'STDF_VER': STDF_VER,
        }