import struct

class RDRDecoder:
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
        NUM_BINS = self.read('H', 2)

        RTST_BIN = []
        for _ in range(NUM_BINS):
            bin_num = self.read('H', 2)
            RTST_BIN.append(bin_num)

        return {
            'RECORD_TYPE': 'RDR',
            'REC_LEN': REC_LEN,
            'REC_TYP': REC_TYP,
            'REC_SUB': REC_SUB,
            'NUM_BINS': NUM_BINS,
            'RTST_BIN': RTST_BIN,
        }