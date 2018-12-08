#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thusrdey Dec  8 11:41:19 2018

@author: @tul tiwari
"""

import requests
from bs4 import BeautifulSoup as bs
import pdfkit
import logging
import sys
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# GST Invoice for Indigo airline
class GoairGSTInvoice:
    url_invoice_retrieve = "https://gst.goair.in/api/Info/SecurityCheck"
    url_gst_invoice = "https://gst.goair.in/Home/UrlAsPDF"
    airline_name = "Go Air"

    def __init__(self, pnr, origin):
        self.pnr = pnr
        self.origin = origin
        logging.info("Indigo_gst_extractor: IndigoGSTInvoice object created successfully for booking reference number "
                     "{0}".format(self.pnr))
        self.get_invoice()

    def get_invoice(self):
        logging.info("goair_gst_extractor: entering function get_invoice")
        payload1 = {"PNR": pnr, "Origin":origin}
        try:
            logging.info("goair_gst_extractor: Inside function get_invoice_html fetching page1")
            # first post request with single form-data field
            page1 = requests.get(GoairGSTInvoice.url_invoice_retrieve, params=payload1, timeout=60)
            logging.info("goair_gst_extractor: Inside function get_invoice_html fetched page1 successful")

            # Invoice is existed or not validation Logic
            if '"Message":"Something went wrong"' in page1.text:
                self.status = "wait"
                print("GST Invoice is not Generated till now...")
                logging.info("GST Invoice is not Generated till now for booking_reference_number:{0}".
                             format(self.pnr))
                return

            self.status = "success"
            data = page1.text
            data = data.replace("[", "")
            data = data.replace("]", "")
            data = json.loads(data)

            payload2 = {"invId": data["InvoiceKey"]}
            r = requests.get(url2, params=payload2, timeout=60)

            self.invoiceNumber = data["InvoiceNumber"]
            self.filename = "{0}_{1}_{2}.pdf".format(GoairGSTInvoice.airline_name, self.pnr, self.invoiceNumber)
            with open(BASE_DIR+"/GST_PDF_DATA/"+self.filename, 'wb') as f:
                f.write(r.content)

            logging.info("goair_gst_extractor: entering function get_invoice")
        # Requests Exceptions
        except requests.exceptions.Timeout as e:
            logging.error("Time Out Error: {0}".format(e))
            print("Program stopped, please check the log file for more information")
        except requests.exceptions.ConnectionError as e:
            logging.error("Connection Error: {0}".format(e))
            print("Program stopped, please check the log file for more information")
        except requests.exceptions.HTTPError as e:
            logging.error("HTTP Error: {0}".format(e))
            print("Program stopped, please check the log file for more information")
        except requests.exceptions.TooManyRedirects as e:
            logging.error("TooManyRedirects Error: {0}".format(e))
            print("Program stopped, please check the log file for more information")

        # Beautiful Soup exceptions
        except bs.HTMLParser.HTMLParseError as e:
            logging.error("Beautiful Soup HTML Parse Error: {0}".format(e))
            print("Program stopped, please check the log file for more information")

        # Value Error
        except ValueError as e:
            logging.error("ValueError: Value not found in the html page: {0}".format(e))
            print("Program stopped, please check the log file for more information")




# raw code for testing *****************************************
# url1 = "https://gst.goair.in/api/Info/SecurityCheck"
# pnr = "FDMG7A"
# origin = "BLR"
#
# payload1 = {"PNR": pnr, "Origin":origin}
# page1 = requests.get(url1, params=payload1, timeout=60)

# with open("results.html", "w") as f:
#     f.write(page1.text)
# data = page1.text
# data = data.replace("[", "")
# data = data.replace("]", "")
#
# data = json.loads(data)
#
# url2 = "https://gst.goair.in/Home/UrlAsPDF"
# payload2 = {"invId": data["InvoiceKey"]}
# r = requests.get(url2, params=payload2, timeout=60)

# with open("invoice.pdf",'wb') as f:
#     f.write(r.content)

# print(page1.url)
# print(page1.text)
# if '"Message":"Something went wrong"' in page1.text:
#     print("Status:", "wait")
# print(data)


# raw test code end **********************************************