import struct

class TSRDecoder:
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
        HEAD_NUM = self.read('B', 1)
        SITE_NUM = self.read('B', 1)
        TEST_TYP = self.read_str(1)
        TEST_NUM = self.read('I', 4)
        EXEC_CNT = self.read('I', 4)
        FAIL_CNT = self.read('I', 4)
        ALRM_CNT = self.read('I', 4)
        TEST_NAM_LEN = self.read('B', 1)
        TEST_NAM = self.read_str(TEST_NAM_LEN)
        SEQ_NAME_LEN = self.read('B', 1)
        SEQ_NAME = self.read_str(SEQ_NAME_LEN)
        OPT_FLAG = self.read('B', 1)
        TEST_TIM = self.read('f', 4)
        TEST_MIN = self.read('f', 4)
        TEST_MAX = self.read('f', 4)
        TST_SUMS = self.read('f', 4)
        TST_SQRS = self.read('f', 4)

        return {
            'RECORD_TYPE': 'TSR',
            'REC_LEN': REC_LEN,
            'REC_TYP': REC_TYP,
            'REC_SUB': REC_SUB,
            'HEAD_NUM': HEAD_NUM,
            'SITE_NUM': SITE_NUM,
            'TEST_TYP': TEST_TYP,
            'TEST_NUM': TEST_NUM,
            'EXEC_CNT': EXEC_CNT,
            'FAIL_CNT': FAIL_CNT,
            'ALRM_CNT': ALRM_CNT,
            'TEST_NAM': TEST_NAM,
            'SEQ_NAME': SEQ_NAME,
            'OPT_FLAG': OPT_FLAG,
            'TEST_TIM': TEST_TIM,
            'TEST_MIN': TEST_MIN,
            'TEST_MAX': TEST_MAX,
            'TST_SUMS': TST_SUMS,
            'TST_SQRS': TST_SQRS,
        }