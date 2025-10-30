import struct

class DTRDecoder:
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
            return s
        except (IndexError, UnicodeDecodeError):
            return 'NaN'

    def decode(self) -> dict:
        REC_LEN = self.read('H', 2)
        #print(REC_LEN)
        REC_TYP = self.read('B', 1)
        REC_SUB = self.read('B', 1)
        text_length = REC_LEN - 2
        TEXT_DAT = self.read_str(text_length) if text_length > 0 else 'NaN'

        return {
            'RECORD_TYPE': 'DTR',
            'REC_LEN': REC_LEN,
            'REC_TYP': REC_TYP,
            'REC_SUB': REC_SUB,
            'TEXT_DAT': TEXT_DAT
        }