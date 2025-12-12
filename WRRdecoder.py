import struct

#WRR
# REC_LEN U*2 Bytes of data following header
# REC_TYP U*1 Record type (2)
# REC_SUB U*1 Record sub-type (20)
# HEAD_NUM U*1 Test head number
# SITE_GRP U*1 Site group number 255
# FINISH_T U*4 Date and time last part tested
# PART_CNT U*4 Number of parts tested
# RTST_CNT U*4 Number of parts retested 4,294,967,295
# ABRT_CNT U*4 Number of aborts during testing 4,294,967,295
# GOOD_CNT U*4 Number of good (passed) parts tested 4,294,967,295
# FUNC_CNT U*4 Number of functional parts tested 4,294,967,295
# WAFER_ID C*n Wafer ID length byte = 0
# FABWF_ID C*n Fab wafer ID length byte = 0
# FRAME_ID C*n Wafer frame ID length byte = 0
# MASK_ID C*n Wafer mask ID length byte = 0
# USR_DESC C*n Wafer description supplied by user length byte = 0
# EXC_DESC C*n Wafer description supplied by exec length byte = 0

class WRRDecoder:

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
        finish_t = self.read('<I')   # U*4
        part_cnt = self.read('<I')   # U*4
        rtst_cnt = self.read('<I')   # U*4
        abrt_cnt = self.read('<I')   # U*4
        good_cnt = self.read('<I')   # U*4
        func_cnt = self.read('<I')   # U*4

        # (C*n) 
        fields_order = [
            'WAFER_ID', 'FABWF_ID', 'FRAME_ID', 'MASK_ID', 'USR_DESC', 'EXC_DESC',
            ]

        out = {
            'HEAD_NUM': head_num, 'SITE_GRP': site_grp, 'FINISH_T': finish_t,
            'PART_CNT': part_cnt, 'RTST_CNT': rtst_cod, 'ABRT_CNT': abrt_cnt,
            'GOOD_CNT': good_cnt, 'FUNC_CNT': func_cnt,
        }

        for name in fields_order:
            out[name] = self.read_cn()
            
            out["REC_TYP"] = 2   # WRR typ
            out["REC_SUB"] = 20  # WRR sub
            out["RECORD_TYPE"] = "WRR"

            
        return out
