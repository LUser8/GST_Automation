#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thusrdey Dec 5 15:44:19 2018

@author: @tul tiwari
"""

from airlines_gst_extractor import indigo_gst_extractor
from email_sender import email_sender_with_attachment
from google_spreadsheet import spreadsheet_2
from helpers import *
import logging
import time
import os
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Creating and configuring logs
logs = logging.basicConfig(filename="../logs/gst_invoice_automation.log", format='%(asctime)s %(message)s', filemode='w'
                           , level=logging.DEBUG)

# Creating logger object
logger = logging.getLogger(logs)

logger.info("GST Invoice Automation Started..")
print("GST Invoice extraction started")

# program start time
start = time.time()

# set google api credential
spreadsheet_2.init_credentials(fromfile=BASE_DIR +"/sample/google_spreadsheet/credentials.json")

sheet_data = spreadsheet_2.get_sheetData()
print("Google sheet fetched Data: ", sheet_data.iloc[:, 0:2])
for index, row in sheet_data.iterrows():
    print("Extracting Pdf for Ref_no: {0}, Airline: {1}".format(row[" Ticket No "], row[" Airline/Hotel Name "]))
    ext_obj = extractor_selector(row)
    # extractor, booking_reference = extractor_selector(row[" Airline/Hotel Name "], row[" Ticket No "])
    if ext_obj is not None:
        # invoice extraction
        t1 = ext_obj
        # status update for success
        if t1.status == "success":
            print("Updating status in sheet:", t1.status)
            logging.info("status for Ticket No {0} is success".format(row[' Ticket No ']))
            subject_detail = "Airline: {0}, GSTInvoice Number:{1}, PNR:{2}".format(
                t1.airline_name, t1.invoiceNumber, t1.pnr)
            filename = t1.filename
            toaddr = row["Email address"]
            e = email_sender_with_attachment.SendInvoiceEmail(toaddr, subject_detail, filename)
            print("Updating ID {0} to {1}".format(row["ID"], t1.status))
            data_to_update = {
                "ID": int(row["ID"]),
                "Fetched Flag": "Y",
                "Last Checked": datetime.now()
            }
            spreadsheet_2.update_sheetData(data_to_update)
        # status update for success
        else:
            print("Updating ID {0} to {1}".format(row["ID"], t1.status))
            print("Status: Waiting")
            logging.info("status for Ticket No {0} is waiting".format(row[' Ticket No ']))
            print("Updating status in sheet:", t1.status)
            data_to_update = {
                "ID": int(row["ID"]),
                "Fetched Flag": "W",
                "Last Checked": datetime.now()
            }
            spreadsheet_2.update_sheetData(data_to_update)
        logging.info("-----------------------------****----------------------------")
        del t1
    else:
        pass
    del ext_obj

print("Time taken:", time.time()-start, "seconds")
print("GST Invoice Automation ended here.")
logger.info("GST Invoice Automation ended")
