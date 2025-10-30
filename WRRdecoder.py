import struct

class WRRDecoder:
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
        SITE_GRP = self.read('B', 1)
        FINISH_T = self.read('I', 4)
        PART_CNT = self.read('H', 2)
        RTST_CNT = self.read('H', 2)
        ABRT_CNT = self.read('H', 2)
        GOOD_CNT = self.read('H', 2)
        FUNC_CNT = self.read('H', 2)
        WAFER_ID = self.read_str(20)
        FABWF_ID = self.read_str(20)
        FRAME_ID = self.read_str(20)
        MASK_ID = self.read_str(20)
        USR_DESC = self.read_str(20)
        EXC_DESC = self.read_str(20)

        return {
            'RECORD_TYPE': 'WRR',
            'REC_LEN': REC_LEN,
            'REC_TYP': REC_TYP,
            'REC_SUB': REC_SUB,
            'HEAD_NUM': HEAD_NUM,
            'SITE_GRP': SITE_GRP,
            'FINISH_T': FINISH_T,
            'PART_CNT': PART_CNT,
            'RTST_CNT': RTST_CNT,
            'ABRT_CNT': ABRT_CNT,
            'GOOD_CNT': GOOD_CNT,
            'FUNC_CNT': FUNC_CNT,
            'WAFER_ID': WAFER_ID,
            'FABWF_ID': FABWF_ID,
            'FRAME_ID': FRAME_ID,
            'MASK_ID': MASK_ID,
            'USR_DESC': USR_DESC,
            'EXC_DESC': EXC_DESC,
        }
