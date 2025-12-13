# -*- coding: utf-8 -*-
"""
Created on Wed Oct 22 15:48:20 2025

@author: shaksyed
"""

# STEP1 : Importing libs
# STEP2 : Perform decoding
# STEP3 : Sorting record specific data, for now sorting data in text file, exploring db options still

# MIR, DTR, PTR, TSR, PRR, PIR, SBR, HBR, etc, recodr types verified and working perfectly

import os
import struct
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import scipy.stats as stats
import json
from datetime import datetime

# import streamlit as st

#Importing Python STDF libararies, i will use it in End to decode
from DTRdecoder import DTRDecoder
from PTRdecoder import PTRDecoder
from GDRdecoder import GDRDecoder
from EPSdecoder import EPSDecoder
from BPSdecoder import BPSDecoder
from FTRdecoder import FTRDecoder
from TSRdecoder import TSRDecoder
from PRRdecoder import PRRDecoder
from PIRdecoder import PIRDecoder
from WCRdecoder import WCRDecoder
from WRRdecoder import WRRDecoder
from WIRdecoder import WIRDecoder
from SDRdecoder import SDRDecoder
from RDRdecoder import RDRDecoder
from PLRdecoder import PLRDecoder
from PGRdecoder import PGRDecoder
from PMRdecoder import PMRDecoder
from HBRdecoder import HBRDecoder
from PCRdecoder import PCRDecoder
from MRRdecoder import MRRDecoder
from FARdecoder import FARDecoder
from MIRdecoder import MIRDecoder
from MPRdecoder import MPRDecoder
from SBRdecoder import SBRDecoder
from ATRdecoder import ATRDecoder

#Step 1 : Read the file as binary for STDF
def decode_stdf(file_path):
    all_records = []
    with open(file_path, "rb") as f:
        while True:
            header = f.read(4)
            if len(header) == 0 or len(header) < 4:
                break

            rec_len = int.from_bytes(header[0:2], byteorder='little')
            rec_typ = header[2]
            rec_sub = header[3]
            
#This is how sample binary data looks after reading it as rb.
#b'\x0b\x00\x00\x00\x01\x02\x00@\x00\x00\x80?\x0cPrintPgmInfo\x00\x0e\x00\x00\x00\x00\x00\x80?\x00\x00 A\x00\x02%f\x02%f\x02%f'

#Step 2 :  Decode the data as per STDF specificatons.
#Refer to my xls workbok to see the mapping of rec_len and rec_sub mapping to each record

            data = f.read(rec_len)
            if len(data) < rec_len:
                break
            
            # Data collected per test execution
            if rec_typ == 15 and rec_sub == 10:  # PTR
                if len(data) >= 10:
                    decoder = PTRDecoder(data)
                    decoded = decoder.decode()
                    yield decoded
                    #all_records.append(decoded)
            elif rec_typ == 15 and rec_sub == 15:  # MPR
                    decoder = MPRDecoder(data)
                    decoded = decoder.decode()
                    yield decoded
                    #all_records.append(decoded)
            elif rec_typ == 15 and rec_sub == 20:  # FTR
                    decoder = FTRDecoder(data)
                    decoded = decoder.decode()
                    yield decoded
                    #all_records.append(decoded)
           #No description available in the STDF V4 document
           # elif rec_typ == 15 and rec_sub == 30:  # STR
           #         print("Pending")
                    
            # Generic data
            elif rec_typ == 50 and rec_sub == 10:  # GDR
                     decoder = GDRDecoder(header + data)
                     decoded = decoder.decode()
                     yield decoded
                     #all_records.append(decoded)
            elif rec_typ == 50 and rec_sub == 30:  # DTR
                    decoder = DTRDecoder(data)
                    decoded = decoder.decode()
                    yield decoded
                    #all_records.append(decoded)
                
             # Data collected per program segment
            elif rec_typ == 20 and rec_sub == 10:  # BPS
                    decoder = BPSDecoder(data)
                    decoded = decoder.decode()
                    yield decoded
                    #all_records.append(decoded)
            elif rec_typ == 20 and rec_sub == 20:  # EPS
                    decoder = EPSDecoder(data)
                    decoded = decoder.decode()
                    yield decoded
                    #all_records.append(decoded)
            
             # Data collected per test in the test program
            elif rec_typ == 10 and rec_sub == 30:  # TSR
                    decoder = TSRDecoder(data)
                    decoded = decoder.decode()
                    yield decoded
                    #all_records.append(decoded)
                
             # Data collected on a per part basis
            elif rec_typ == 5 and rec_sub == 10:  # PIR
                    decoder = PIRDecoder(data)
                    decoded = decoder.decode()
                    yield decoded
                    #all_records.append(decoded)
            elif rec_typ == 5 and rec_sub == 20:  # PRR
                    decoder = PRRDecoder(data)
                    decoded = decoder.decode()
                    yield decoded
                    #all_records.append(decoded)
                
            #  Data collected per wafer
            elif rec_typ == 2 and rec_sub == 10:  # WIR
                    decoder = WIRDecoder(data)
                    decoded = decoder.decode()
                    yield decoded
                    #all_records.append(decoded)
            elif rec_typ == 2 and rec_sub == 20:  # WRR
                    decoder = WRRDecoder(data)
                    decoded = decoder.decode()
                    yield decoded
                    #all_records.append(decoded)
            elif rec_typ == 2 and rec_sub == 20:  # WCR
                    decoder = WCRDecoder(data)
                    decoded = decoder.decode()
                    yield decoded
                    #all_records.append(decoded)
                          
            #  Data collected on a per lot basis
            elif rec_typ == 1 and rec_sub == 10:  # MIR
                    decoder = MIRDecoder(data)
                    decoded = decoder.decode()
                    yield decoded
                    #all_records.append(decoded)
            elif rec_typ == 1 and rec_sub == 20:  # MRR
                    decoder = MRRDecoder(data)
                    decoded = decoder.decode()
                    yield decoded
                    #all_records.append(decoded)
            elif rec_typ == 1 and rec_sub == 30:  # PCR
                    decoder = PCRDecoder(data)
                    decoded = decoder.decode()
                    yield decoded
                    #all_records.append(decoded)
            elif rec_typ == 1 and rec_sub == 40:  # HBR
                    decoder = HBRDecoder(data)
                    decoded = decoder.decode()
                    yield decoded
                    #all_records.append(decoded)
            elif rec_typ == 1 and rec_sub == 50:  # SBR
                    decoder = SBRDecoder(data)
                    decoded = decoder.decode()
                    yield decoded
                    #all_records.append(decoded)
            elif rec_typ == 1 and rec_sub == 60:  # PMR
                    decoder = PMRDecoder(data)
                    decoded = decoder.decode()
                    yield decoded
                    #all_records.append(decoded)
            elif rec_typ == 1 and rec_sub == 62:  # PGR
                    decoder = PGRDecoder(data)
                    decoded = decoder.decode()
                    yield decoded
                    #all_records.append(decoded)
            elif rec_typ == 1 and rec_sub == 63:  # PLR
                    decoder = PLRDecoder(data)
                    decoded = decoder.decode()
                    yield decoded
                    #all_records.append(decoded)
            elif rec_typ == 1 and rec_sub == 70:  # RDR
                    decoder = RDRDecoder(data)
                    decoded = decoder.decode()
                    yield decoded
                    #all_records.append(decoded)
            elif rec_typ == 1 and rec_sub == 80:  # SDR
                    decoder = SDRDecoder(data)
                    decoded = decoder.decode()
                    yield decoded
                    #all_records.append(decoded)
            #No description available in the STDF V4 document
            # elif rec_typ == 1 and rec_sub == 90:  # PSR
            #         decoder = PSRDecoder(data)
            #         decoded = decoder.decode()
            #         all_records.append(decoded)
            # elif rec_typ == 1 and rec_sub == 91:  # NMR
            #         print("Pending")
            # elif rec_typ == 1 and rec_sub == 92:  # CNR
            #         print("Pending")
            # elif rec_typ == 1 and rec_sub == 93:  # SSR
            #         print("Pending")
            # elif rec_typ == 1 and rec_sub == 94:  # SCR
            #        print("Pending")

            #  Information about the STDF file
            elif rec_typ == 0 and rec_sub == 10:  # FAR
                    decoder = FARDecoder(data)
                    decoded = decoder.decode()
                    yield decoded
                    #all_records.append(decoded)
            elif rec_typ == 0 and rec_sub == 20:  # ATR
                    decoder = ATRDecoder(data)
                    decoded = decoder.decode()
                    yield decoded
                    #all_records.append(decoded)
            #No description available in the STDF V4 document
            # elif rec_typ == 0 and rec_sub == 30:  # VUR
            #         print("Pending")
            
    return all_records

#Helpers to handle the none value

def safe_int(value, default=99999):
    # Treat None, empty string, and non-numeric as default
    if value is None:
        return default
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def safe_float(value, default=999.99):
    if value is None:
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def safe_str(value, default=""):
    if value is None:
        return default
    try:
        return str(value)
    except Exception:
        return default


def get_with_aliases(record, *keys):
    for k in keys:
        v = record.get(k)
        if v is not None:
            return v
    # If all are None, still return None
    return None


def normalize_test_typ(v, default=""):
    """
    TEST_TYP (C*1) may come as a 1-char string or a byte/int depending on parser.
    Normalize to a single-character string.
    """
    if v is None:
        return default
    if isinstance(v, int):
        # Convert a byte value (0..255) to a char; otherwise fall back to default
        return chr(v) if 0 <= v <= 255 else default
    # If bytes of length 1, decode; if longer string, take first char
    if isinstance(v, (bytes, bytearray)):
        try:
            return v[:1].decode('ascii', errors='replace')
        except Exception:
            return default
    s = str(v)
    return s[:1] if s else default

    
file_path = 'gu_site7.std'  # Replace with your actual file path

os.makedirs('OUTPUT', exist_ok=True)

if file_path.lower().endswith(('.std', '.stdf')):
    processed = 0
    written = 0
    skipped = 0
    errors = 0
    for record in decode_stdf(file_path):  # generator iteration
        processed += 1
        record_type = str(record.get("RECORD_TYPE", "N/A"))
        
        # MIR
        if record_type == "MIR":
            df_vals_MIR = [
                record_type,
                str(record.get('LOT_ID', "LotID is Empty")),
                str(record.get('PART_TYP', "PartType is Empty")),
                str(record.get('NODE_NAM', "Tester name is Empty")),
                str(record.get('TSTR_TYP', "TesterType is Empty")),
                str(record.get('JOB_NAM', "Job Name is Empty")),
                str(record.get('SBLOT_ID', "Sub LOT ID is Empty")),
                str(record.get('OPER_NAM', "Operator is Empty")),
                str(record.get('EXEC_TYP', "Empty")),
                str(record.get('EXEC_VER', "Empty")),
                str(record.get('TEST_COD', "Empty")),
                str(record.get('TST_TEMP', "Empty")),
            ]
            df_MIR = pd.DataFrame(
                [df_vals_MIR],
                columns=[
                    "RECORD_TYPE","LOT_ID","PART_TYP","NODE_NAM","TSTR_TYP","JOB_NAM","SBLOT_ID",
                    "OPER_NAM","EXEC_TYP","EXEC_VER","TEST_COD","TST_TEMP"
                ]
            )
            df_MIR.to_csv('OUTPUT/DataMIR.txt', sep='\t', header=False, index=False, mode='a')
            print("MIR rows appended to DataMIR.txt")

            columns_mir = [
                    "RECORD_TYPE", "LOT_ID","PART_TYP","NODE_NAM","TSTR_TYP","JOB_NAM","SBLOT_ID",
                    "OPER_NAM","EXEC_TYP","EXEC_VER","TEST_COD","TST_TEMP"
                                    ]

                        # Build the JSON-ready dict (`rec`) from df_values
            rec = dict(zip(columns_mir,df_vals_MIR))
            # Optional: add metadata
            rec["timestamp"] = datetime.utcnow().isoformat(timespec="seconds") + "Z"

                             #JSON                   
                             # Write NDJSON (append mode)
            out_path = 'OUTPUT/DataAll.ndjson'
            with open(out_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(rec, ensure_ascii=False) + '\n')


                #WIR
        elif record_type in ["WIR"]:
                    print("YES WIR IS EXECUTING")
                    df_val_WIR = [
                        record_type, 
                        float(record.get('WAFER_ID', "Wafer ID is Empty"))
                        ]
                    df_WIR = pd.DataFrame([df_val_WIR])

                    with open('OUTPUT/DataWIR.txt', 'a') as f:
                        for index, row in df_WIR.iterrows():
                                line = '\t'.join(str(value) for value in row.values)
                                f.write(line + '\n')
                        print("WIR rows appended to DataWIR.txt")
                        
                        columns_wrr = [
                                    "RECORD_TYPE", "WAFER_ID"
                                    ]

                        # Build the JSON-ready dict (`rec`) from df_values
                        rec = dict(zip(columns_wrr,df_val_WIR))
                        # Optional: add metadata
                        rec["timestamp"] = datetime.utcnow().isoformat(timespec="seconds") + "Z"

                             #JSON                   
                             # Write NDJSON (append mode)
                        out_path = 'OUTPUT/DataAll.ndjson'
                        with open(out_path, 'a', encoding='utf-8') as f:
                                 f.write(json.dumps(rec, ensure_ascii=False) + '\n')


                #WRR
        elif record_type in ["WRR"]:
                    print("YES WRR IS EXECUTING")
                    df_val_WRR = [
                        record_type,
                        int(record.get('PART_CNT', 99999)),
                        int(record.get('RTST_CNT', 99999)),
                        int(record.get('ABRT_CNT', 99999)),
                        int(record.get('GOOD_CNT', 99999)),
                        int(record.get('FUNC_CNT', 99999)),
                        str(record.get('WAFER_ID', "Wafer ID is Empty")),
                        str(record.get('FABWF_ID', "FABWafer ID is Empty")),
                        ]
                    df_WRR = pd.DataFrame([df_val_WRR])

                    with open('OUTPUT/DataWRR.txt', 'a') as f:
                        for index, row in df_WRR.iterrows():
                                line = '\t'.join(str(value) for value in row.values)
                                f.write(line + '\n')
                        print("WIR rows appended to DataWIR.txt")
                        
                        columns_wrr = [
                                    "RECORD_TYPE", "PART_CNT", "RTST_CNT", "ABRT_CNT", "GOOD_CNT",
                                    "FUNC_CNT", "WAFER_ID", "HI_LIMIT"
                                    ]

                        # Build the JSON-ready dict (`rec`) from df_values
                        rec = dict(zip(columns_wrr,df_val_WRR))
                        # Optional: add metadata
                        rec["timestamp"] = datetime.utcnow().isoformat(timespec="seconds") + "Z"

                             #JSON                   
                             # Write NDJSON (append mode)
                        out_path = 'OUTPUT/DataAll.ndjson'
                        with open(out_path, 'a', encoding='utf-8') as f:
                                 f.write(json.dumps(rec, ensure_ascii=False) + '\n')
                  
                #PIR 
        elif record_type in ["PIR"]:
                    print("YES PIR IS EXECUTING")
                    
                    head_num = safe_int(record.get('HEAD_NUM'), 99999)
                    site_num = safe_int(record.get('SITE_NUM'), 99999)
                    df_PIR = pd.DataFrame([[head_num, site_num]], columns=["HEAD_NUM", "SITE_NUM"])

                    #df_PIR = pd.DataFrame([df_val_PIR])

                    with open('OUTPUT/DataPIR.txt', 'a') as f:
                        for index, row in df_PIR.iterrows():
                                line = '\t'.join(str(value) for value in row.values)
                                f.write(line + '\n')
                        print("PIR rows appended to DataPIR.txt")

                             # Build the JSON-ready dict (`rec`) from df_values
                        rec = {
                                    "RECORD_TYPE": "PIR",
                                    "HEAD_NUM": head_num,
                                    "SITE_NUM": site_num,
                                    "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z"
                                 }
                             #dict(zip(columns_sbr, df_SBR_json))
                             # Optional: add metadata
                        rec["timestamp"] = datetime.utcnow().isoformat(timespec="seconds") + "Z"
            
                             #JSON                   
                             # Write NDJSON (append mode)
                        out_path = 'OUTPUT/DataAll.ndjson'
                        with open(out_path, 'a', encoding='utf-8') as f:
                                 f.write(json.dumps(rec, ensure_ascii=False) + '\n')

                  
                #PRR        
        elif record_type in ["PRR"]:
                    print("YES PRR IS EXECUTING")
                                    
                    # Try common casings; adjust to your parser’s actual keys
                    head_num  = safe_int(get_with_aliases(record, 'HEAD_NUM',  'head_num'))
                    site_num  = safe_int(get_with_aliases(record, 'SITE_NUM',  'site_num'))
                    part_flg  = safe_int(get_with_aliases(record, 'PART_FLG',  'part_flg'))
                    num_test  = safe_int(get_with_aliases(record, 'NUM_TEST',  'num_test'))
                    hard_bin  = safe_int(get_with_aliases(record, 'HARD_BIN',  'hard_bin'))
                    soft_bin  = safe_int(get_with_aliases(record, 'SOFT_BIN',  'soft_bin'))
                    x_coord   = safe_int(get_with_aliases(record, 'X_COORD',   'x_coord'))
                    y_coord   = safe_int(get_with_aliases(record, 'Y_COORD',   'y_coord'))
                    test_t    = safe_float(get_with_aliases(record, 'TEST_T',   'test_t'))   # seconds
                    part_id   = safe_str (get_with_aliases(record, 'PART_ID',   'part_id'),  default="")  # often alphanumeric
                    part_txt  = safe_str (get_with_aliases(record, 'PART_TXT',  'part_txt'), default="")
                    part_fix  = safe_str (get_with_aliases(record, 'PART_FIX',  'part_fix'), default="")

                    df_val_PRR = [head_num, site_num, part_flg, num_test, hard_bin, soft_bin,x_coord, y_coord, test_t, part_id, part_txt, part_fix]
                    
                    df_PRR = pd.DataFrame([df_val_PRR])

                    with open('OUTPUT/DataPRR.txt', 'a') as f:
                        for index, row in df_PRR.iterrows():
                                line = '\t'.join(str(value) for value in row.values)
                                f.write(line + '\n')
                        print("PIR rows appended to DataPRR.txt")
 
                             # Build the JSON-ready dict (`rec`) from df_values
                        rec = {
                                    "RECORD_TYPE": "PRR",
                                    "PART_FLG": part_flg,
                                    "NUM_TEST": num_test,
                                    "HARD_BIN": hard_bin,
                                    "SOFT_BIN": soft_bin,
                                    "X_COORD": x_coord,
                                    "Y_COORD": y_coord,
                                    "TEST_T": test_t,
                                    "PART_ID": part_id,
                                    "PART_TXT": part_txt,
                                    "PART_FIX": part_fix,
                                    "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z"
                                 }
                             #dict(zip(columns_sbr, df_SBR_json))
                             # Optional: add metadata
                        rec["timestamp"] = datetime.utcnow().isoformat(timespec="seconds") + "Z"
            
                             #JSON                   
                             # Write NDJSON (append mode)
                        out_path = 'OUTPUT/DataAll.ndjson'
                        with open(out_path, 'a', encoding='utf-8') as f:
                                 f.write(json.dumps(rec, ensure_ascii=False) + '\n')
                          
                #TSR
        elif record_type == "TSR":
                     print("YES TSR IS EXECUTING")

                     head_num = safe_int(record.get('HEAD_NUM'))
                     site_num = safe_int(record.get('SITE_NUM'))
                     test_typ = normalize_test_typ(record.get('TEST_TYP'), default="")
                     test_num = safe_int(record.get('TEST_NUM'))
                     exec_cnt = safe_int(record.get('EXEC_CNT'))
                     fail_cnt = safe_int(record.get('FAIL_CNT'))
                     test_nam = str(record.get('TEST_NAM', "TEST_NAM is Empty") or "")
                     seq_name = str(record.get('SEQ_NAME', "SEQ_NAME is Empty") or "")
                     test_lbl = str(record.get('TEST_LBL', "TEST_LBL is Empty") or "")

                     df_TSR = pd.DataFrame([[head_num, site_num, test_typ, test_num, exec_cnt, fail_cnt, test_nam, seq_name, test_lbl]])

                     os.makedirs('OUTPUT', exist_ok=True)
                     df_TSR.to_csv('OUTPUT/DataTSR.txt', sep='\t', header=False, index=False, mode='a')
                     print("TSR rows appended to DataTSR.txt")
                     
                     # Build the JSON-ready dict (`rec`) from df_values
                     rec = {
                            "RECORD_TYPE": "TSR",
                            "TEST_TYP": test_typ,
                            "TEST_NUM": test_num,
                            "EXEC_CNT": exec_cnt,
                            "FAIL_CNT": fail_cnt,
                            "TEST_NAM": test_nam,
                            "SEQ_NAME": seq_name,
                            "TEST_LBL": test_lbl,
                            "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z"
                         }
                     #dict(zip(columns_sbr, df_SBR_json))
                     # Optional: add metadata
                     rec["timestamp"] = datetime.utcnow().isoformat(timespec="seconds") + "Z"
    
                     #JSON                   
                     # Write NDJSON (append mode)
                     out_path = 'OUTPUT/DataAll.ndjson'
                     with open(out_path, 'a', encoding='utf-8') as f:
                         f.write(json.dumps(rec, ensure_ascii=False) + '\n')
                    
                     
                #HBR
        elif record_type == "HBR":
                     print("YES HBR IS EXECUTING")

                     head_num = safe_int(record.get('HEAD_NUM'))
                     site_num = safe_int(record.get('SITE_NUM'))
                     hbin_num = safe_int(record.get('HBIN_NUM'))
                     hbin_cnt = safe_int(record.get('HBIN_CNT'))
                     hbin_pf = safe_int(record.get('HBIN_PF'))
                     hbin_name = str(record.get('HBIN_NAME', "TEST_NAM is Empty") or "")


                     df_HBR = pd.DataFrame([[head_num, site_num, hbin_num, hbin_cnt, hbin_pf, hbin_name]])

                     os.makedirs('OUTPUT', exist_ok=True)
                     df_HBR.to_csv('OUTPUT/DataHBR.txt', sep='\t', header=False, index=False, mode='a')
                     print("HBR rows appended to DataHBR.txt")
                     
                     columns_hbr = [
                                    "RECORD_TYPE", "HBIN_NUM", "HBIN_CNT", "HBIN_NAME"
                                    ]
                    
                     # Build the JSON-ready dict (`rec`) from df_values
                     rec = {
                            "RECORD_TYPE": "HBR",
                            "HBIN_NUM": hbin_num,
                            "HBIN_CNT": hbin_cnt,
                            "HBIN_NAME": hbin_name,
                            "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z"
                         }
                     #dict(zip(columns_sbr, df_SBR_json))
                     # Optional: add metadata
                     rec["timestamp"] = datetime.utcnow().isoformat(timespec="seconds") + "Z"
    
                     #JSON                   
                     # Write NDJSON (append mode)
                     out_path = 'OUTPUT/DataAll.ndjson'
                     with open(out_path, 'a', encoding='utf-8') as f:
                         f.write(json.dumps(rec, ensure_ascii=False) + '\n')
                         print("SBR record appended to DataAll.ndjson")



                #SBR
        elif record_type == "SBR":
                     print("YES SBR IS EXECUTING")

                     head_num = safe_int(record.get('HEAD_NUM'))
                     site_num = safe_int(record.get('SITE_NUM'))
                     sbin_num = safe_int(record.get('SBIN_NUM'))
                     sbin_cnt = safe_int(record.get('SBIN_CNT'))
                     sbin_pf = safe_int(record.get('SBIN_PF'))
                     sbin_name = str(record.get('SBIN_NAME', "TEST_NAM is Empty") or "")


                     df_SBR = pd.DataFrame([[head_num, site_num, sbin_num, sbin_cnt, sbin_pf, sbin_name]])

                     os.makedirs('OUTPUT', exist_ok=True)
                     df_SBR.to_csv('OUTPUT/DataSBR.txt', sep='\t', header=False, index=False, mode='a')
                     print("SBR rows appended to DataSBR.txt")
                     
                     
                     columns_sbr = [
                                    "RECORD_TYPE", "SBIN_NUM", "SBIN_CNT", "SBIN_NAME"
                                    ]
                    
                     # Build the JSON-ready dict (`rec`) from df_values
                     rec = {
                            "RECORD_TYPE": "SBR",
                            "SBIN_NUM": sbin_num,
                            "SBIN_CNT": sbin_cnt,
                            "SBIN_NAME": sbin_name,
                            "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z"
                         }
                     #dict(zip(columns_sbr, df_SBR_json))
                     # Optional: add metadata
                     rec["timestamp"] = datetime.utcnow().isoformat(timespec="seconds") + "Z"
    
                     #JSON                   
                     # Write NDJSON (append mode)
                     out_path = 'OUTPUT/DataAll.ndjson'
                     with open(out_path, 'a', encoding='utf-8') as f:
                         f.write(json.dumps(rec, ensure_ascii=False) + '\n')
                         print("SBR record appended to DataAll.ndjson")



                #DTR
        elif record_type in ["DTR"]:
                    df_values_dtr = [record_type,str(record.get('TEXT_DAT', "Unknown DTR record"))]
                    df = pd.DataFrame([df_values_dtr])

                    with open('OUTPUT/DataDTR.txt', 'a') as f:
                        for index, row in df.iterrows():
                                line = '\t'.join(str(value) for value in row.values)
                                f.write(line + '\n')
                        print("PTR rows appended to DataDTR.txt")
                        
                        columns_dtr = [
                                    "RECORD_TYPE", "DATA_TEXT"
                                    ]
                        
                        # Build the JSON-ready dict (`rec`) from df_values
                        rec = dict(zip(columns_dtr,df_values_dtr))
                        # Optional: add metadata
                        rec["timestamp"] = datetime.utcnow().isoformat(timespec="seconds") + "Z"

                        #JSON                   
                        # Write NDJSON (append mode)
                        out_path = 'OUTPUT/DataAll.ndjson'
                        with open(out_path, 'a', encoding='utf-8') as f:
                            f.write(json.dumps(rec, ensure_ascii=False) + '\n')
                            print("DTR record appended to DataAll.ndjson")

                #PTR     
        elif record_type in ["PTR"]:

                    try:
                        df_values_ptr = [
                            record_type,
                            int(record.get('SITE_NUM', 99999)),
                            float(record.get('TEST_NUM', 9999.9999)),
                            str(record.get('TEST_TXT', "Unknown test name")),
                            float(record.get('LO_LIMIT', 0.0)),
                            float(record.get('RESULT', 0.0)),
                            float(record.get('HI_LIMIT', 0.0)),
                            str(record.get('UNITS', "ghosts"))
                        ]
                        
                        columns_ptr = [
                                     "RECORD_TYPE","SITE_NUM","TEST_NUM", "TEST_NAME",
                                    "LO_LIMIT", "RESULT", "HI_LIMIT", "UNITS"
                                    ]

                        # Build the JSON-ready dict (`rec`) from df_values
                        rec = dict(zip(columns_ptr,df_values_ptr))
                        # Optional: add metadata
                        rec["timestamp"] = datetime.utcnow().isoformat(timespec="seconds") + "Z"

                        
                        df = pd.DataFrame([df_values_ptr], columns=[
                              "RECORD_TYPE","SITE_NUM", "TEST_NUM", "TEST_NAME",
                             "LO_LIMIT", "RESULT", "HI_LIMIT", "UNITS"
                         ])

                        with open('OUTPUT/DataPTR.txt', 'a') as f:
                            for index, row in df.iterrows():
                                line = '\t'.join(str(value) for value in row.values)
                                f.write(line + '\n')
                            #print("PTR rows appended to DataPTR.txt")
                            
                        #JSON                   
                        # Write NDJSON (append mode)
                        out_path = 'OUTPUT/DataAll.ndjson'
                        with open(out_path, 'a', encoding='utf-8') as f:
                            f.write(json.dumps(rec, ensure_ascii=False) + '\n')
                            print("PTR record appended to DataAll.ndjson")


                    except (ValueError, TypeError) as e:
                        print(f"Can't find the test details: {e}")

# After the loop:
if processed == 0:
    print("No records found to export.")
else:
    print(f"Processed: {processed}, Written: {written}, Skipped: {skipped}, Errors: {errors}")



