#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thusrdey Dec  5 15:44:19 2018

@author: @tul tiwari
"""

from airlines_gst_extractor import indigo_gst_extractor, goair_gst_extractor
from google_spreadsheet import spreadsheet_2
import os
import logging
import time
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

extractor_list = [ indigo_gst_extractor.IndigoGSTInvoice, goair_gst_extractor.GoairGSTInvoice ]
    # , spicejet_gst_extractor.SpicejetGSTInvoice,
    # goair_gst_extractor.GoairGSTInvoice ]

city_code = {
    "BANGALORE": "BLR",
    "DELHI": "DEL"
}


def extractor_selector(row):
    airline = row[" Airline/Hotel Name "]
    pnr = row[" Ticket No "]

    if airline.upper() in 'INDIGO':
        pnr = pnr.split("-")[1]
        ext_obj = indigo_gst_extractor.IndigoGSTInvoice(pnr)
        return ext_obj

    elif airline.upper() in 'GO AIR':
        origin_city = city_code[row[' Origin City '].upper()]
        pnr = pnr.split("-")[1]
        ext_obj = goair_gst_extractor.GoairGSTInvoice(pnr, origin_city)
        return ext_obj
    else:
        return None

# For googlesheet api testing
# set google api credential
# spreadsheet_2.init_credentials(fromfile=BASE_DIR +"/sample/google_spreadsheet/credentials.json")
# sheet_data = spreadsheet_2.get_sheetData()
# print(sheet_data.iloc[:, :])