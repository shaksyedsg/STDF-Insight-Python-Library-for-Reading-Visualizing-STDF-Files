#MIR
# SETUP_T U*4 Date and time of job setup
# START_T U*4 Date and time first part tested
# STAT_NUM U*1 Tester station number
# MODE_COD C*1 Test mode code (e.g. prod, dev) space
# RTST_COD C*1 Lot retest code space
# PROT_COD C*1 Data protection code space
# BURN_TIM U*2 Burn-in time (in minutes) 65,535
# CMOD_COD C*1 Command mode code space
# LOT_ID C*n Lot ID (customer specified)
# PART_TYP C*n Part Type (or product ID)
# NODE_NAM C*n Name of node that generated data
# TSTR_TYP C*n Tester type
# JOB_NAM C*n Job name (test program name)
# JOB_REV C*n Job (test program) revision number length byte = 0
# SBLOT_ID C*n Sublot ID length byte = 0
# OPER_NAM C*n Operator name or ID (at setup time) length byte = 0
# EXEC_TYP C*n Tester executive software type length byte = 0
# EXEC_VER C*n Tester exec software version number length byte = 0
# TEST_COD C*n Test phase or step code length byte = 0
# TST_TEMP C*n Test temperature length byte = 0
# USER_TXT C*n Generic user text length byte = 0
# AUX_FILE C*n Name of auxiliary data file length byte = 0
# PKG_TYP C*n Package type length byte = 0
# FAMLY_ID C*n Product family ID length byte = 0
# DATE_COD C*n Date code length byte = 0
# FACIL_ID C*n Test facility ID length byte = 0
# FLOOR_ID C*n Test floor ID length byte = 0
# PROC_ID C*n Fabrication process ID length byte = 0
# OPER_FRQ C*n Operation frequency or step length byte = 0

import struct

class MIRDecoder:

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
    
        # ---- Numeric + single-char segment ----
        setup_t  = self.read('<I')   # U*4
        start_t  = self.read('<I')   # U*4
        stat_num = self.read('<B')   # U*1
        mode_cod = self.read_c1()    # C*1
        rtst_cod = self.read_c1()    # C*1
        prot_cod = self.read_c1()    # C*1
        burn_tim = self.read('<H')   # U*2  (this was the offset bug)
        cmod_cod = self.read_c1()    # C*1

        # (C*n) 
        fields_order = [
            'LOT_ID', 'PART_TYP', 'NODE_NAM', 'TSTR_TYP', 'JOB_NAM', 'JOB_REV',
            'SBLOT_ID', 'OPER_NAM', 'EXEC_TYP', 'EXEC_VER', 'TEST_COD', 'TST_TEMP',
            'USER_TXT', 'AUX_FILE', 'PKG_TYP', 'FAMLY_ID', 'DATE_COD', 'FACIL_ID',
            'FLOOR_ID', 'PROC_ID', 'OPER_FRQ', 'SPEC_NAM', 'SPEC_VER', 'FLOW_ID',
            'SETUP_ID', 'DSGN_REV', 'ENG_ID', 'ROM_COD', 'SERL_NUM', 'SUPR_NAM'
        ]  
        out = {
            'SETUP_T': setup_t, 'START_T': start_t, 'STAT_NUM': stat_num,
            'MODE_COD': mode_cod, 'RTST_COD': rtst_cod, 'PROT_COD': prot_cod,
            'BURN_TIM': burn_tim, 'CMOD_COD': cmod_cod,
        }
        for name in fields_order:
            out[name] = self.read_cn()
            
            out["REC_TYP"] = 1   # MIR typ
            out["REC_SUB"] = 10  # MIR sub
            out["RECORD_TYPE"] = "MIR"

            
        return out