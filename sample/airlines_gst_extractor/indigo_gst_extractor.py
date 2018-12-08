#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thusrdey Dec  5 15:44:19 2018

@author: @tul tiwari
"""

import requests
from bs4 import BeautifulSoup as bs
import pdfkit
import logging
import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# GST Invoice for Indigo airline
class IndigoGSTInvoice:
    url_invoice_retrieve = "https://book.goindigo.in/Booking/GSTInvoiceDetails"
    url_gst_invoice = "https://book.goindigo.in/Booking/GSTInvoice"
    airline_name = "Indigo"

    def __init__(self, pnr):
        self.pnr = pnr
        logging.info("Indigo_gst_extractor: IndigoGSTInvoice object created successfully for booking reference number "
                     "{0}".format(self.pnr))
        self.get_invoice_html()
        self.get_pdf_data()

    def get_invoice_html(self):
        logging.info("Indigo_gst_extractor: entering function get_invoice_html")
        payload1 = {"indigoGSTDetails.PNR": self.pnr}
        try:
            logging.info("Indigo_gst_extractor: Inside function get_invoice_html fetching page1")
            # first post request with single form-data field
            page1 = requests.post(IndigoGSTInvoice.url_invoice_retrieve, data=payload1, timeout=60)
            logging.info("Indigo_gst_extractor: Inside function get_invoice_html fetched page1 successful")

            # Invoice is existed or not validation Logic
            if "Sorry we are unable to process your request at this time" in page1.text:
                self.status = "wait"
                print("GST Invoice is not Generated till now...")
                logging.info("GST Invoice is not Generated till now for booking_reference_number:{0}".
                             format(self.pnr))
                return
            self.status = "success"
            # passing extracted page to beautiful soup for data extraction
            logging.info("Indigo_gst_extractor: starting parsing with bs4 page1")
            soup = bs(page1.text, "html.parser")
            logging.info("Indigo_gst_extractor: parsing page1 completed")
            logging.info("Indigo_gst_extractor: finding id 'GSTInvoiceForm' ")
            token = soup.find(id="GSTInvoiceForm")
            if token is None:
                raise ValueError
            logging.info("Indigo_gst_extractor: found id 'GSTInvoiceForm' successful ")
            data = token.find("input", {"name": "__RequestVerificationToken"})
            temp_data = str(data).replace("</input>", "")
            soup2 = bs(temp_data, "html.parser")
            RequestVerificationToken = soup2.input['value']
            logging.info("Indigo_gst_extractor: extracted request token:{0}".format(RequestVerificationToken))

            self.invoiceNumber = soup.find(class_="ViewInvoice")["invoice-number"]
            logging.info("Indigo_gst_extractor: extracted invoice Number:{0}".format(self.invoiceNumber))
            payload2 = {
                "__RequestVerificationToken": RequestVerificationToken,
                "IndigoGSTInvoice.InvoiceNumber": self.invoiceNumber,
                "IndigoGSTInvoice.IsPrint": "false",
                "IndigoGSTInvoice.isExempted": "",
                "IndigoGSTInvoice.ExemptedMsg": ""
            }

            logging.info("Indigo_gst_extractor: Inside function get_invoice_html fetching page2")
            # second post request with 5 form-data fields
            page2 = requests.post(IndigoGSTInvoice.url_gst_invoice, data=payload2, timeout=60)
            logging.info("Indigo_gst_extractor: Inside function get_invoice_html fetched page2 successful")

            logging.info("Indigo_gst_extractor: starting parsing with bs4 page2")
            soup3 = bs(page2.text, "html.parser")
            logging.info("Indigo_gst_extractor: starting parsing page2 is completed")
            style_data = str(soup3.style)

            image_prefix = "https://book.goindigo.in"
            invoice_data = soup3.find(class_="pageHeight")
            img_fields = invoice_data.find_all("img")

            for child in img_fields:
                child["src"] = image_prefix + child['src']

            body_data = str(invoice_data)

            self.html_data = "<html><head>{0}</head><body>{1}</body></html>".format(style_data, body_data)
            logging.info("Indigo_gst_extractor: existing function get_invoice_html successfully")

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

    # making pdf
    def get_pdf_data(self):
        if self.status == "wait":
            return
        logging.info("Indigo_gst_extractor: entering function get_pdf_data")
        try:
            print("GST Invoice extracted successfully", "Getting PDF", sep='\n')
            self.filename = "{0}_{1}_{2}.pdf".format(IndigoGSTInvoice.airline_name, self.pnr, self.invoiceNumber)
            pdfkit.from_string(self.html_data, BASE_DIR+"/GST_PDF_DATA/"+self.filename)
            logging.info("Indigo_gst_extractor: existing function get_pdf_data successfully")
        except Exception as e:
            logging.error("Error during HTML to PDF : Value not found in the html page: {0}".format(e))
            print("Program stopped, please check the log file for more information")


