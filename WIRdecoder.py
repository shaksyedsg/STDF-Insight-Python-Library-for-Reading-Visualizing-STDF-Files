import struct

#WIR
# REC_LEN U*2 Bytes of data following header
# REC_TYP U*1 Record type (2)
# REC_SUB U*1 Record sub-type (10)
# HEAD_NUM U*1 Test head number
# SITE_GRP U*1 Site group number 255
# START_T U*4 Date and time first part tested
# WAFER_ID C*n Wafer ID length byte = 0

class WIRDecoder:
    def __init__(self, data: bytes):
        self.data = data
        self.offset = 0

    def read(self, fmt: str):
        """Read numeric value per 'fmt' and advance by its size."""
        size = struct.calcsize(fmt)
        if self.offset + size > len(self.data):
            return None
        val = struct.unpack_from(fmt, self.data, self.offset)[0]
        self.offset += size
        return val

    def read_c1(self) -> str:
        """Read a single character (C*1)."""
        if self.offset >= len(self.data):
            return 'NaN'
        b = self.data[self.offset:self.offset+1]
        self.offset += 1
        return b.decode('ascii', errors='replace')

    def read_cn(self, encoding: str = 'ascii') -> str:

        length = self.read('<B')  # U*1 length byte
        if length is None:
            return 'NaN'
        if length == 0:
            return ''
        if self.offset + length > len(self.data):
            return 'NaN'
        raw = self.data[self.offset:self.offset + length]
        self.offset += length
        return raw.decode(encoding, errors='replace')

    def decode(self) -> dict:

        head_num = self.read('<B')   # U*1
        site_grp = self.read('<B')   # U*1
        start_t = self.read('<I')   # U*4

        # (C*n) 
        fields_order = [
            'WAFER_ID',
            ]

        out = {
            'HEAD_NUM': head_num, 'SITE_GRP': site_grp, 
        }

        for name in fields_order:
            out[name] = self.read_cn()
            
            out["REC_TYP"] = 2   # WRR typ
            out["REC_SUB"] = 10  # WRR sub
            out["RECORD_TYPE"] = "WIR"
            
        return out
