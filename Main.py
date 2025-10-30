# -*- coding: utf-8 -*-
"""
Created on Wed Oct 22 15:48:20 2025

@author: shaksyed
"""

import os
import struct
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import scipy.stats as stats
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
                    all_records.append(decoded)
            elif rec_typ == 15 and rec_sub == 15:  # MPR
                    decoder = MPRDecoder(data)
                    decoded = decoder.decode()
                    all_records.append(decoded)
            elif rec_typ == 15 and rec_sub == 20:  # FTR
                    decoder = FTRDecoder(data)
                    decoded = decoder.decode()
                    all_records.append(decoded)
           #No description available in the STDF V4 document
           # elif rec_typ == 15 and rec_sub == 30:  # STR
           #         print("Pending")
                    
            # Generic data
            elif rec_typ == 50 and rec_sub == 10:  # GDR
                decoder = GDRDecoder(header + data)
                decoded = decoder.decode()
                all_records.append(decoded)
            elif rec_typ == 50 and rec_sub == 30:  # DTR
                    decoder = DTRDecoder(data)
                    decoded = decoder.decode()
                    all_records.append(decoded)
                
             # Data collected per program segment
            elif rec_typ == 20 and rec_sub == 10:  # BPS
                    decoder = BPSDecoder(data)
                    decoded = decoder.decode()
                    all_records.append(decoded)
            elif rec_typ == 20 and rec_sub == 20:  # EPS
                    decoder = EPSDecoder(data)
                    decoded = decoder.decode()
                    all_records.append(decoded)
            
             # Data collected per test in the test program
            elif rec_typ == 10 and rec_sub == 30:  # TSR
                    decoder = TSRDecoder(data)
                    decoded = decoder.decode()
                    all_records.append(decoded)
                
             # Data collected on a per part basis
            elif rec_typ == 5 and rec_sub == 10:  # PIR
                    decoder = PIRDecoder(data)
                    decoded = decoder.decode()
                    all_records.append(decoded)
            elif rec_typ == 5 and rec_sub == 20:  # PRR
                    decoder = PRRDecoder(data)
                    decoded = decoder.decode()
                    all_records.append(decoded)
                
            #  Data collected per wafer
            elif rec_typ == 2 and rec_sub == 10:  # WIR
                    decoder = WIRDecoder(data)
                    decoded = decoder.decode()
                    all_records.append(decoded)
            elif rec_typ == 2 and rec_sub == 20:  # WRR
                    decoder = WRRDecoder(data)
                    decoded = decoder.decode()
                    all_records.append(decoded)
            elif rec_typ == 2 and rec_sub == 20:  # WCR
                    decoder = WCRDecoder(data)
                    decoded = decoder.decode()
                    all_records.append(decoded)
                          
            #  Data collected on a per lot basis
            elif rec_typ == 1 and rec_sub == 10:  # MIR
                    decoder = MIRDecoder(data)
                    decoded = decoder.decode()
                    all_records.append(decoded)
            elif rec_typ == 1 and rec_sub == 20:  # MRR
                    decoder = MRRDecoder(data)
                    decoded = decoder.decode()
                    all_records.append(decoded)
            elif rec_typ == 1 and rec_sub == 30:  # PCR
                    decoder = PCRDecoder(data)
                    decoded = decoder.decode()
                    all_records.append(decoded)
            elif rec_typ == 1 and rec_sub == 40:  # HBR
                    decoder = HBRDecoder(data)
                    decoded = decoder.decode()
                    all_records.append(decoded)
            elif rec_typ == 1 and rec_sub == 50:  # SBR
                    decoder = SBRDecoder(data)
                    decoded = decoder.decode()
                    all_records.append(decoded)
            elif rec_typ == 1 and rec_sub == 60:  # PMR
                    decoder = PMRDecoder(data)
                    decoded = decoder.decode()
                    all_records.append(decoded)
            elif rec_typ == 1 and rec_sub == 62:  # PGR
                    decoder = PGRDecoder(data)
                    decoded = decoder.decode()
                    all_records.append(decoded)
            elif rec_typ == 1 and rec_sub == 63:  # PLR
                    decoder = PLRDecoder(data)
                    decoded = decoder.decode()
                    all_records.append(decoded)
            elif rec_typ == 1 and rec_sub == 70:  # RDR
                    decoder = RDRDecoder(data)
                    decoded = decoder.decode()
                    all_records.append(decoded)
            elif rec_typ == 1 and rec_sub == 80:  # SDR
                    decoder = SDRDecoder(data)
                    decoded = decoder.decode()
                    all_records.append(decoded)
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
                    all_records.append(decoded)
            elif rec_typ == 0 and rec_sub == 20:  # ATR
                    decoder = ATRDecoder(data)
                    decoded = decoder.decode()
                    all_records.append(decoded)
            #No description available in the STDF V4 document
            # elif rec_typ == 0 and rec_sub == 30:  # VUR
            #         print("Pending")
            
    return all_records


#  Example usage 
file_path = 'test_data1.std'  # Replace with your actual file path


# Check file extension -- >> for STDF file
if file_path.lower().endswith(('.std', '.stdf')):
    records = decode_stdf(file_path)


# Future enhancements
# # Check file extension -- >> for ATDF file
# elif file_path.lower().endswith(('.atdf')):
#     records = decode_atdf(file_path)

# # Check file extension -- >> for txt file
# elif file_path.lower().endswith(('.atdf')):
#     records = decode_txt(file_path)

# # Check file extension -- >> for csv file
# elif file_path.lower().endswith(('.csv')):
#     records = decode_csv(file_path)

    # Exporting all records to CSV
    csv_file_path = "output_8.txt"
    if records:
        all_keys = set()
        for record in records:
            all_keys.update(record.keys())

        with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=list(all_keys))
            writer.writeheader()
            for record in records:
                writer.writerow(record)

        print(f"All decoded records have been exported to {csv_file_path}.")
    else:
        print("No records found to export.")

    # # Plotting each record
    # for record in records:
    #     labels = ['LO_LIMIT', 'RESULT', 'HI_LIMIT']
        
    #     # If values are missing fill it with "0"
    #     try:
    #         values = [
    #             float(record.get('LO_LIMIT', 0.0)),
    #             float(record.get('RESULT', 0.0)),
    #             float(record.get('HI_LIMIT', 0.0))
    #         ]
    #     except (ValueError, TypeError) as e:
    #         print(f"Error converting values to float: {e}")
    #         values = [0.0, 0.0, 0.0]
    #     except Exception as e:
    #         print(f"Unexpected error: {e}")
    #         values = [0.0, 0.0, 0.0]

    #     if all(v == 0.0 for v in values):
    #         print(f"Skipping plot for record due to missing or zero values: {record}")
    #         continue
        
    # # #Putting data into the data grids.
    # #     try:
    # #         values = [
    # #             str(record.get('RECORD_TYPE'), "Unkwon record type"),
    # #             float(record.get('TEST_NUM'), 9999.9999),
    # #             str(record.get('RECORD_TYPE'), "Unkwon test name"),
    # #             float(record.get('LO_LIMIT'), 0.0),
    # #             float(record.get('RESULT'), 0.0),
    # #             float(record.get('HI_LIMIT'), 0.0),
    # #             str(record.get('UNITS'), "ghosts"),
    # #         ]
    # #     except (ValueError, TypeError) as e:
    # #         print(f"Can't able to find the test details: {e}")
    # #     except Exception as e:
    # #         print(f" something is very wrong with the data: {e}")
    # #         values = ["GhostRecordType", 0.0, "DummyTname", 0.0, 0.0, 0.0, "DummyUnit"]
            
    # #         columns = ["RecordType", "TEST_NUM", "TEST_NAME", "LO_LIMIT", "RESULT", "HI_LIMIT", "UNITS"]
            
    # #         df = pd.DataFrame([values], columns=columns)
    # #         print(df)

    #     # plt.figure(figsize=(6, 4))
    #     # plt.bar(labels, values, color='skyblue')
    #     # plt.xlabel('Measurement Type')
    #     # plt.ylabel('Value')
    #     # plt.title(f"Test #{record.get('TEST_NUM', 'N/A')} - {record.get('TEST_TXT', '')}")
    #     # plt.grid(True)
    #     # plt.tight_layout()
    #     # plt.show()    
        
    #     # Create the Q-Q plot
    #     # plt.figure(figsize=(6, 4))
    #     # stats.probplot(values, dist="norm", plot=plt)

    #     # # Customize the plot
    #     # plt.title(f"Test #{record.get('TEST_NUM', 'N/A')} - {record.get('TEST_TXT', '')}")
    #     # plt.xlabel('Measurement Type')
    #     # plt.ylabel('Value')
    #     # plt.grid(True)
    #     # plt.tight_layout()
    #     # plt.show() 
    

# # Process each record
# for record in records:
#     labels = ['LO_LIMIT', 'RESULT', 'HI_LIMIT']

#     # Extract values with error handling
#     try:
#         values = [
#             float(record.get('LO_LIMIT', 0.0)),
#             float(record.get('RESULT', 0.0)),
#             float(record.get('HI_LIMIT', 0.0))
#         ]
#     except (ValueError, TypeError) as e:
#         print(f"Error converting values to float: {e}")
#         values = [0.0, 0.0, 0.0]
#     except Exception as e:
#         print(f"Unexpected error: {e}")
#         values = [0.0, 0.0, 0.0]

#     # Skip plotting if all values are zero
#     if all(v == 0.0 for v in values):
#         #print(f"Skipping plot for record due to missing or zero values: {record}")
#         continue

#     # # Extract full record details for DataFrame
#     try :
#         record_type = str(record.get('RECORD_TYPE', "NAN"))
#         #print(f"Printing the DTR record value : {record_type}")
#         print(record_type)
#     except (ValueError) as e:
#         record_type="ghost record"
#         print(f"The unknown record type :{e}")

# record_type = str(record.get("RECORD_TYPE", "N/A"))
    
# if record_type == "PTR":
#     try:
#         df_values = [
#             int(record.get('SITE_NUM', 99999)),
#             str(record.get('RECORD_TYPE', "Unknown record type")),
#             float(record.get('TEST_NUM', 9999.9999)),
#             str(record.get('TEST_TXT', "Unknown test name")),
#             float(record.get('LO_LIMIT', 0.0)),
#             float(record.get('RESULT', 0.0)),
#             float(record.get('HI_LIMIT', 0.0)),
#             str(record.get('UNITS', "ghosts"))
#         ]

#     # Create and display DataFrame
#     # columns = ["SITE", "RecordType", "TEST_NUM", "TEST_NAME", "LO_LIMIT", "RESULT", "HI_LIMIT", "UNITS"]
#     # df = pd.DataFrame([df_values], columns)
#     # print("Data in DataFrame format:")
#     # print(df)


#         # Create DataFrame
#         df = pd.DataFrame([df_values], columns=[
#             "SITE_NUM", "RECORD_TYPE", "TEST_NUM", "TEST_NAME",
#             "LO_LIMIT", "RESULT", "HI_LIMIT", "UNITS"
#         ])

#     # Open the file in append mode and write each row
#         with open('DataTxt.txt', 'a') as f:
#             for index, row in df.iterrows():
#                 line = '\t'.join(str(value) for value in row.values)
#                 f.write(line + '\n')
#                 print("PTR rows appended to output.txt")
                
#     except (ValueError, TypeError) as e:
#         print(f"Can't find the test details: {e}")
#         df_values = [99999, "GhostRecordType", 0.0, "DummyTname", 0.0, 0.0, 0.0, "DummyUnits"]

#     # Streamlit UI
#     # st.title("Test Records Viewer")
#     # st.write("Scroll below to view all test records:")
#     # st.dataframe(df, height=400)


#     # Bar plot
#     # plt.figure(figsize=(6, 4))
#     # plt.bar(labels, values, color='skyblue')
#     # plt.xlabel('Measurement Type')
#     # plt.ylabel('Value')
#     # plt.title(f"Test #{record.get('TEST_NUM', 'N/A')} - {record.get('TEST_TXT', '')}")
#     # plt.grid(True)
#     # plt.tight_layout()
#     # plt.show()

#     # Q-Q plot
#     # plt.figure(figsize=(6, 4))
#     # stats.probplot(values, dist="norm", plot=plt)
#     # plt.title(f"Q-Q Plot for Test #{record.get('TEST_NUM', 'N/A')} - {record.get('TEST_TXT', '')}")
#     # plt.xlabel('Theoretical Quantiles')
#     # plt.ylabel('Sample Quantiles')
#     # plt.grid(True)
#     # plt.tight_layout()
#     # plt.show()

#     print("Processing complete.")

# else:
#     print("Unsupported file type. Please use a .std or .stdf file.")


file_path = 'test_data2.std'  # Replace with your actual file path

# Validate file extension
if file_path.lower().endswith(('.std', '.stdf')):
    try:
        records = decode_stdf(file_path)  # Make sure this function is defined

        if not records:
            print("No records found to export.")
        else:
            # Export all records to CSV
            csv_file_path = "output_8.txt"
            all_keys = set()
            for record in records:
                all_keys.update(record.keys())

            with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=list(all_keys))
                writer.writeheader()
                for record in records:
                    writer.writerow(record)

            print(f"All decoded records have been exported to {csv_file_path}.")

            # Process each record
            for record in records:
                record_type = str(record.get("RECORD_TYPE", "N/A"))
                # if record_type == "GDR":
                #     print(record_type)
                # try:
                #     values = [
                #         float(record.get('LO_LIMIT', 0.0)),
                #         float(record.get('RESULT', 0.0)),
                #         float(record.get('HI_LIMIT', 0.0))
                #     ]
                # except (ValueError, TypeError) as e:
                #     print(f"Error converting values to float: {e}")
                #     values = [0.0, 0.0, 0.0]

                # if all(v == 0.0 for v in values):
                #     continue

                record_type = str(record.get('RECORD_TYPE', "NAN"))
                #print(f"Record Type: {record_type}")
                
                if record_type in ["MIR"]:
                    print("YES IM MIR EXISTS")

                if record_type in ["DTR"]:
                    df_values = [record_type,str(record.get('TEXT_DAT', "Unknown DTR record"))]
                    df = pd.DataFrame([df_values])

                    with open('DataTxt.txt', 'a') as f:
                        for index, row in df.iterrows():
                                line = '\t'.join(str(value) for value in row.values)
                                f.write(line + '\n')
                        #print("PTR rows appended to DataTxt.txt")

                      
                elif record_type in ["PTR"]:
                    try:
                        df_values = [
                            int(record.get('SITE_NUM', 99999)),
                            record_type,
                            float(record.get('TEST_NUM', 9999.9999)),
                            str(record.get('TEST_TXT', "Unknown test name")),
                            float(record.get('LO_LIMIT', 0.0)),
                            float(record.get('RESULT', 0.0)),
                            float(record.get('HI_LIMIT', 0.0)),
                            str(record.get('UNITS', "ghosts"))
                        ]
                        
                        df = pd.DataFrame([df_values], columns=[
                             "SITE_NUM", "RECORD_TYPE", "TEST_NUM", "TEST_NAME",
                             "LO_LIMIT", "RESULT", "HI_LIMIT", "UNITS"
                         ])
                        
                        #print(df)

                        with open('DataTxt.txt', 'a') as f:
                            for index, row in df.iterrows():
                                line = '\t'.join(str(value) for value in row.values)
                                f.write(line + '\n')
                            #print("PTR rows appended to DataTxt.txt")

                    except (ValueError, TypeError) as e:
                        print(f"Can't find the test details: {e}")

    except Exception as e:
        print(f"Error decoding STDF file: {e}")
else:
    print("Unsupported file type. Please use a .std or .stdf file.")
