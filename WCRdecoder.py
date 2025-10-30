import struct

class WCRDecoder:
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

    def decode(self) -> dict:
        REC_LEN = self.read('H', 2)
        REC_TYP = self.read('B', 1)
        REC_SUB = self.read('B', 1)
        WAFR_SIZ = self.read('f', 4)
        DIE_HT = self.read('f', 4)
        DIE_WID = self.read('f', 4)
        DIE_UNITS = self.read('B', 1)
        WF_FLAT = self.read('B', 1)
        CENTER_X = self.read('h', 2)
        CENTER_Y = self.read('h', 2)
        POS_X = self.read('h', 2)
        POS_Y = self.read('h', 2)

        return {
            'RECORD_TYPE': 'WCR',
            'REC_LEN': REC_LEN,
            'REC_TYP': REC_TYP,
            'REC_SUB': REC_SUB,
            'WAFR_SIZ': WAFR_SIZ,
            'DIE_HT': DIE_HT,
            'DIE_WID': DIE_WID,
            'DIE_UNITS': DIE_UNITS,
            'WF_FLAT': WF_FLAT,
            'CENTER_X': CENTER_X,
            'CENTER_Y': CENTER_Y,
            'POS_X': POS_X,
            'POS_Y': POS_Y,
        }