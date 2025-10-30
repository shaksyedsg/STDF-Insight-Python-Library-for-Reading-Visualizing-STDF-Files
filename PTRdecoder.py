
#PTRdecoder.py
import struct
import numpy as np

class PTRDecoder:
    SCAL_PREFIX = {
        15: 'f', 12: 'p', 9: 'n', 6: 'u', 3: 'm', 2: '%', 0: '',
        -3: 'K', -6: 'M', -9: 'G', -12: 'T'
    }

    def __init__(self, data: bytes):
        self.data = data
        self.offset = 0

    def read(self, fmt: str, size: int):
        try:
            val = struct.unpack_from(fmt, self.data, self.offset)[0]
            self.offset += size
            return val
        except (struct.error, IndexError):
            return np.nan

    def read_str(self):
        try:
            length = self.data[self.offset]
            self.offset += 1
            s = self.data[self.offset:self.offset + length].decode(errors='replace')
            self.offset += length
            return s
        except (IndexError, UnicodeDecodeError):
            return 'NaN'

    def decode(self) -> dict:
        TEST_NUM = self.read('I', 4)
        HEAD_NUM = self.read('B', 1)
        SITE_NUM = self.read('B', 1)
        TEST_FLG = self.read('B', 1)
        PARM_FLG = self.read('B', 1)
        RESULT = self.read('f', 4)
        TEST_TXT = self.read_str()
        ALARM_ID = self.read('B', 1)
        OPT_FLAG = self.read('B', 1)
        RES_SCAL = self.read('b', 1)
        LLM_SCAL = self.read('b', 1)
        HLM_SCAL = self.read('b', 1)
        LO_LIMIT = self.read('f', 4)
        HI_LIMIT = self.read('f', 4)
        UNITS = self.read_str()
        C_RESFMT = self.read_str()
        C_LLMFMT = self.read_str()
        C_HLMFMT = self.read_str()

        scaled_result = RESULT * (10 ** RES_SCAL) if not np.isnan(RESULT) else np.nan
        scaled_lo_limit = LO_LIMIT * (10 ** LLM_SCAL) if not np.isnan(LO_LIMIT) else np.nan
        scaled_hi_limit = HI_LIMIT * (10 ** HLM_SCAL) if not np.isnan(HI_LIMIT) else np.nan

        display_units = f"{self.SCAL_PREFIX.get(RES_SCAL, '')}{UNITS}"

        try:
            display_result = C_RESFMT % scaled_result if C_RESFMT != 'NaN' else 'NaN'
        except (TypeError, ValueError):
            display_result = 'NaN'

        try:
            display_lo_limit = C_LLMFMT % scaled_lo_limit if C_LLMFMT != 'NaN' else 'NaN'
        except (TypeError, ValueError):
            display_lo_limit = 'NaN'

        try:
            display_hi_limit = C_HLMFMT % scaled_hi_limit if C_HLMFMT != 'NaN' else 'NaN'
        except (TypeError, ValueError):
            display_hi_limit = 'NaN'

        return {
            'RECORD_TYPE': 'PTR',
            'TEST_NUM': TEST_NUM,
            'SITE_NUM': SITE_NUM,
            'TEST_TXT': TEST_TXT,
            'LO_LIMIT': display_lo_limit,
            'LLM_SCAL': LLM_SCAL,
            'RESULT': display_result,
            'RES_SCAL': RES_SCAL,
            'UNITS': display_units,
            'HI_LIMIT': display_hi_limit,
            'HLM_SCAL': HLM_SCAL,
            'HEAD_NUM': HEAD_NUM,
            'TEST_FLG': TEST_FLG,
            'PARM_FLG': PARM_FLG,
            'ALARM_ID': ALARM_ID,
            'OPT_FLAG': OPT_FLAG,
            'C_RESFMT': C_RESFMT,
            'C_LLMFMT': C_LLMFMT,
            'C_HLMFMT': C_HLMFMT
        }