#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thusrdey Dec 6 11:44:19 2018

@author: @tul tiwari
"""

# Python code to illustrate Sending mail with attachments
# from your Gmail account

# libraries to be imported
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class SendInvoiceEmail:
    # class variable
    fromaddr = "atul.tiwari@elitingbiz.us"
    password = "HyberitD100@"
    def __init__(self, toaddr, subject_detail, filename):
        print("GST Invoice pdf sending email Process Started.")
        logging.info("Sending Email process started")
        logging.info("SendInvoiceEmail: Createing object")
        self.toaddr = toaddr
        self.subject_detail = subject_detail
        self.filename = filename
        logging.info("SendInvoiceEmail: object created success")
        self.send_mail()

    def send_mail(self):
        logging.info("SendInvoiceEmail: Enter in function send_mail for {0}.".format(self.subject_detail))
        try:
            # instance of MIMEMultipart
            msg = MIMEMultipart()
            # storing the senders email address
            msg['From'] = SendInvoiceEmail.fromaddr
            # storing the receivers email address
            msg['To'] = self.toaddr
            # storing the subject
            msg['Subject'] = "GST Invoice PDF: {0}".format(self.subject_detail)
            # string to store the body of the mail
            body = "Dear Sir,\n\t PFA"
            # attach the body with the msg instance
            msg.attach(MIMEText(body, 'plain'))
            # open the file to be sent
            attachment = open(BASE_DIR+'/GST_PDF_DATA/'+self.filename, "rb")
            # instance of MIMEBase and named as p
            p = MIMEBase('application', 'octet-stream')
            # To change the payload into encoded form
            p.set_payload((attachment).read())
            # encode into base64
            encoders.encode_base64(p)
            p.add_header('Content-Disposition', "attachment; filename= %s" % self.filename)
            # attach the instance 'p' to instance 'msg'
            msg.attach(p)
            # creates SMTP session
            s = smtplib.SMTP('smtp.gmail.com', 587)
            # start TLS for security
            s.starttls()
            # Authentication
            s.login(SendInvoiceEmail.fromaddr, SendInvoiceEmail.password)
            # Converts the Multipart msg into a string
            text = msg.as_string()
            # sending the mail
            logging.info("Sending Email at address: {0}".format(self.toaddr))
            s.sendmail(SendInvoiceEmail.fromaddr, self.toaddr, text)
            logging.info("Email sent successfully")
            # terminating the session
            s.quit()
            print("Email Sent.")
            logging.info("SendInvoiceEmail: Exiting from function send_mail")

        except smtplib.SMTPServerDisconnected as e:
            logging.error("SMTPServerDisconnected Error: {0}".format(e))
            print("Program stopped, please check the log file for more information")
        except smtplib.SMTPResponseException as e:
            logging.error("SMTPResponseException Error: {0}".format(e))
            print("Program stopped, please check the log file for more information")
        except smtplib.SMTPSenderRefused as e:
            logging.error("SMTPSenderRefused Error: {0}".format(e))
            print("Program stopped, please check the log file for more information")
        except smtplib.SMTPRecipientsRefused as e:
            logging.error("SMTPRecipientsRefused Error: {0}".format(e))
            print("Program stopped, please check the log file for more information")
        except smtplib.SMTPDataError as e:
            logging.error("SMTPDataError : {0}".format(e))
            print("Program stopped, please check the log file for more information")
        except smtplib.SMTPConnectError as e:
            logging.error("SMTPConnectError : {0}".format(e))
            print("Program stopped, please check the log file for more information")
        except smtplib.SMTPHeloError as e:
            logging.error("SMTPHeloError : {0}".format(e))
            print("Program stopped, please check the log file for more information")
        except smtplib.SMTPNotSupportedError as e:
            logging.error("SMTPNotSupportedError : {0}".format(e))
            print("Program stopped, please check the log file for more information")
        except smtplib.SMTPAuthenticationError as e:
            logging.error("SMTPAuthenticationError : {0}".format(e))
            print("Program stopped, please check the log file for more information")
        except smtplib.SMTPException as e:
            logging.error("SMTPException : {0}".format(e))
            print("Program stopped, please check the log file for more information")
        except FileNotFoundError as e:
            logging.error("FileNotFoundError : {0}".format(e))
            print("Program stopped, please check the log file for more information")

