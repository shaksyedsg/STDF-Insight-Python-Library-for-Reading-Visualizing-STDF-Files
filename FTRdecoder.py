import struct

class FTRDecoder:
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
        TEST_NUM = self.read('I', 4)
        HEAD_NUM = self.read('B', 1)
        SITE_NUM = self.read('B', 1)
        TEST_FLG = self.read('B', 1)
        OPT_FLAG = self.read('B', 1)
        CYCL_CNT = self.read('I', 4)
        REL_VECT = self.read('I', 4)
        VECT_OFF = self.read('I', 4)
        STATE_CNT = self.read('I', 4)
        VECT_NUM = self.read('I', 4)
        CAPTURE_CNT = self.read('I', 4)
        TEST_NAM_LEN = self.read('B', 1)
        TEST_NAM = self.read_str(TEST_NAM_LEN)
        ALARM_ID_LEN = self.read('B', 1)
        ALARM_ID = self.read_str(ALARM_ID_LEN)
        PROG_TXT_LEN = self.read('B', 1)
        PROG_TXT = self.read_str(PROG_TXT_LEN)
        RSULT_TXT_LEN = self.read('B', 1)
        RSULT_TXT = self.read_str(RSULT_TXT_LEN)
        PATG_NUM = self.read('H', 2)
        SPIN_MAP = self.read('B', 1)

        return {
            'RECORD_TYPE': 'FTR',
            'REC_LEN': REC_LEN,
            'REC_TYP': REC_TYP,
            'REC_SUB': REC_SUB,
            'TEST_NUM': TEST_NUM,
            'HEAD_NUM': HEAD_NUM,
            'SITE_NUM': SITE_NUM,
            'TEST_FLG': TEST_FLG,
            'OPT_FLAG': OPT_FLAG,
            'CYCL_CNT': CYCL_CNT,
            'REL_VECT': REL_VECT,
            'VECT_OFF': VECT_OFF,
            'STATE_CNT': STATE_CNT,
            'VECT_NUM': VECT_NUM,
            'CAPTURE_CNT': CAPTURE_CNT,
            'TEST_NAM': TEST_NAM,
            'ALARM_ID': ALARM_ID,
            'PROG_TXT': PROG_TXT,
            'RSULT_TXT': RSULT_TXT,
            'PATG_NUM': PATG_NUM,
}