#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thusrdey Dec  5 15:44:19 2018

@author: @tul tiwari
"""

from airlines_gst_extractor import indigo_gst_extractor
from google_spreadsheet import spreadsheet_2
import os
import logging
import time
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

extractor_list = [ indigo_gst_extractor.IndigoGSTInvoice ]

def extractor_selector(airline, ticket_no):
    if airline.upper() in 'INDIGO':
        ticket_no = ticket_no.split("-")[1]
        return extractor_list[0], ticket_no
    else:
        return None, None

