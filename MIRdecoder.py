import struct

class MIRDecoder:
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
        SETUP_T = self.read('I', 4)
        START_T = self.read('I', 4)
        STAT_NUM = self.read('B', 1)
        MODE_COD = self.read_str(1)
        RTST_COD = self.read_str(1)
        PROT_COD = self.read_str(1)
        BURN_TIM = self.read('I', 4)
        CMOD_COD = self.read_str(1)
        # Additional fields from the image
        LOT_ID = self.read_str(20)
        JOB_NAM = self.read_str(20)
        NODE_NAM = self.read_str(20)
        TESTER_SN = self.read_str(20)
        OPER_NAM = self.read_str(20)
        EXEC_NAM = self.read_str(20)
        SPEC_NAM = self.read_str(20)
        FLOW_ID = self.read_str(20)

        return {
            'RECORD_TYPE': 'MIR',
            'REC_LEN': REC_LEN,
            'REC_TYP': REC_TYP,
            'REC_SUB': REC_SUB,
            'SETUP_T': SETUP_T,
            'START_T': START_T,
            'STAT_NUM': STAT_NUM,
            'MODE_COD': MODE_COD,
            'RTST_COD': RTST_COD,
            'PROT_COD': PROT_COD,
            'BURN_TIM': BURN_TIM,
            'CMOD_COD': CMOD_COD,
            'LOT_ID': LOT_ID,
            'JOB_NAM': JOB_NAM,
            'NODE_NAM': NODE_NAM,
            'TESTER_SN': TESTER_SN,
            'OPER_NAM': OPER_NAM,
            'EXEC_NAM': EXEC_NAM,
            'SPEC_NAM': SPEC_NAM,
            'FLOW_ID': FLOW_ID,
        }