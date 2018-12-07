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
print("Google sheet fetched Data: ", sheet_data.iloc[:, 1])
for index, row in sheet_data.iterrows():
    print("Extracting Pdf for Ref_no: {0}, Airline: {1}".format(row[" Ticket No "], row[" Airline/Hotel Name "]))
    extractor, booking_reference = extractor_selector(row[" Airline/Hotel Name "], row[" Ticket No "])
    if extractor is not None:
        # invoice extraction
        t1 = extractor(booking_reference)
        if t1.status == "success":
            print("Status: Success")
            subject_detail = "Airline: {0}, GSTInvoice Number:{1}, Booking Refernece Number:{2}".format(
                t1.airline_name, t1.invoiceNumber, t1.booking_reference_number)
            filename = t1.filename
            toaddr = row["Email address"]
            e = email_sender_with_attachment.SendInvoiceEmail(toaddr, subject_detail, filename)
            data_to_update = {
                "ID": int(row["ID"]),
                "Fetched Flag": "Y",
                "Last Checked": datetime.now()
            }
            spreadsheet_2.update_sheetData(data_to_update)
        else:
            print("Status: Waiting")
            print(t1.status)
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

print("Time taken:", time.time()-start, "seconds")
print("GST Invoice Automation ended here.")
logger.info("GST Invoice Automation ended")
