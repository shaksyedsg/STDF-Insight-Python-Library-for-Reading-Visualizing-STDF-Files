import struct

class SDRDecoder:
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
        SITE_GRP = self.read('B', 1)
        SITE_CNT = self.read('B', 1)

        SITE_NUMS = []
        for _ in range(SITE_CNT):
            SITE_NUMS.append(self.read('B', 1))

        HAND_TYP = self.read_str(20)
        HAND_ID = self.read_str(20)
        CARD_TYP = self.read_str(20)
        CARD_ID = self.read_str(20)
        LOAD_TYP = self.read_str(20)
        LOAD_ID = self.read_str(20)
        DIB_TYP = self.read_str(20)
        DIB_ID = self.read_str(20)
        CABL_TYP = self.read_str(20)
        CABL_ID = self.read_str(20)
        CONT_TYP = self.read_str(20)
        CONT_ID = self.read_str(20)
        LASR_TYP = self.read_str(20)
        LASR_ID = self.read_str(20)
        EXTR_TYP = self.read_str(20)
        EXTR_ID = self.read_str(20)

        return {
            'RECORD_TYPE': 'SDR',
            'REC_LEN': REC_LEN,
            'REC_TYP': REC_TYP,
            'REC_SUB': REC_SUB,
            'HEAD_NUM': HEAD_NUM,
            'SITE_GRP': SITE_GRP,
            'SITE_CNT': SITE_CNT,
            'SITE_NUMS': SITE_NUMS,
            'HAND_TYP': HAND_TYP,
            'HAND_ID': HAND_ID,
            'CARD_TYP': CARD_TYP,
            'CARD_ID': CARD_ID,
            'LOAD_TYP': LOAD_TYP,
            'LOAD_ID': LOAD_ID,
            'DIB_TYP': DIB_TYP,
            'DIB_ID': DIB_ID,
            'CABL_TYP': CABL_TYP,
            'CABL_ID': CABL_ID,
            'CONT_TYP': CONT_TYP,
            'CONT_ID': CONT_ID,
            'LASR_TYP': LASR_TYP,
            'LASR_ID': LASR_ID,
            'EXTR_TYP': EXTR_TYP,
            'EXTR_ID': EXTR_ID,
        }
