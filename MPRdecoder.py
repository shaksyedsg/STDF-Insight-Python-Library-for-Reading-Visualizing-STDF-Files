import struct
class MPRDecoder:
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

    def decode_array(self, count, fmt, size):
        return [self.read(fmt, size) for _ in range(count)]

    def decode(self) -> dict:
        REC_LEN = self.read('H', 2)
        REC_TYP = self.read('B', 1)
        REC_SUB = self.read('B', 1)
        TEST_NUM = self.read('I', 4)
        HEAD_NUM = self.read('B', 1)
        SITE_NUM = self.read('B', 1)
        TEST_FLG = self.read('B', 1)
        PARM_FLG = self.read('B', 1)

        RTN_ICNT = self.read('H', 2)
        RTN_INDX = self.decode_array(RTN_ICNT, 'H', 2)

        RSLT_CNT = self.read('H', 2)
        RTN_RSLT = self.decode_array(RSLT_CNT, 'f', 4)

        TEST_TXT_LEN = self.read('B', 1)
        TEST_TXT = self.read_str(TEST_TXT_LEN)

        ALARM_ID_LEN = self.read('B', 1)
        ALARM_ID = self.read_str(ALARM_ID_LEN)

        UNITS_LEN = self.read('B', 1)
        UNITS = self.read_str(UNITS_LEN)

        RTN_UNITS_LEN = self.read('B', 1)
        RTN_UNITS = self.read_str(RTN_UNITS_LEN)

        TEST_MIN = self.read('f', 4)
        TEST_MAX = self.read('f', 4)
        TEST_TYP = self.read('f', 4)

        return {
            'RECORD_TYPE': 'MPR',
            'REC_LEN': REC_LEN,
            'REC_TYP': REC_TYP,
            'REC_SUB': REC_SUB,
            'TEST_NUM': TEST_NUM,
            'HEAD_NUM': HEAD_NUM,
            'SITE_NUM': SITE_NUM,
            'TEST_FLG': TEST_FLG,
            'PARM_FLG': PARM_FLG,
            'RTN_ICNT': RTN_ICNT,
            'RTN_INDX': RTN_INDX,
            'RSLT_CNT': RSLT_CNT,
            'RTN_RSLT': RTN_RSLT,
            'TEST_TXT': TEST_TXT,
            'ALARM_ID': ALARM_ID,
            'UNITS': UNITS,
            'RTN_UNITS': RTN_UNITS,
            'TEST_MIN': TEST_MIN,
            'TEST_MAX': TEST_MAX,
            'TEST_TYP': TEST_TYP,
        }