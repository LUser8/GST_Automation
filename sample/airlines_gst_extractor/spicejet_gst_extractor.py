#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thusrdey Dec  10 10:5:19 2018

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


class SpiceJetGSTInvoice:
    def __init__(self):
        pass
