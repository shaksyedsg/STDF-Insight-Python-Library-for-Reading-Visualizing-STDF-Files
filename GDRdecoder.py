import struct

class GDRDecoder:
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

    def read_bytes(self, length: int):
        val = self.data[self.offset:self.offset + length]
        self.offset += length
        return val

    def read_str(self, length: int):
        try:
            s = self.read_bytes(length).decode(errors='replace')
            return s.strip()
        except:
            return 'NaN'

    def decode_field(self):
        type_code = self.read('B', 1)
        if type_code == 0:  # Pad field
            return {'type': 'PAD', 'value': None}
        elif type_code == 1:
            return {'type': 'U1', 'value': self.read('B', 1)}
        elif type_code == 2:
            return {'type': 'U2', 'value': self.read('H', 2)}
        elif type_code == 3:
            return {'type': 'U4', 'value': self.read('I', 4)}
        elif type_code == 4:
            return {'type': 'I1', 'value': self.read('b', 1)}
        elif type_code == 5:
            return {'type': 'I2', 'value': self.read('h', 2)}
        elif type_code == 6:
            return {'type': 'I4', 'value': self.read('i', 4)}
        elif type_code == 7:
            return {'type': 'R4', 'value': self.read('f', 4)}
        elif type_code == 8:
            return {'type': 'R8', 'value': self.read('d', 8)}
        elif type_code == 9:
            length = self.read('B', 1)
            return {'type': 'C*n', 'value': self.read_str(length)}
        elif type_code == 10:
            length = self.read('B', 1)
            return {'type': 'B*n', 'value': self.read_bytes(length)}
        elif type_code == 11:
            bit_len = self.read('H', 2)
            byte_len = (bit_len + 7) // 8
            return {'type': 'N*n', 'value': self.read_bytes(byte_len)}
        elif type_code == 12:
            return {'type': 'D*n', 'value': None}
        else:
            return {'type': f'Unknown({type_code})', 'value': None}

    def decode(self) -> dict:
        REC_LEN = self.read('H', 2)
        REC_TYP = self.read('B', 1)
        REC_SUB = self.read('B', 1)
        FLD_CNT = self.read('H', 2)

        GEN_DATA = []
        for _ in range(FLD_CNT):
            GEN_DATA.append(self.decode_field())

        return {
            'RECORD_TYPE': 'GDR',
            'REC_LEN': REC_LEN,
            'REC_TYP': REC_TYP,
            'REC_SUB': REC_SUB,
            'FLD_CNT': FLD_CNT,
            'GEN_DATA': GEN_DATA,
        }