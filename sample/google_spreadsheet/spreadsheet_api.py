#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 15:44:19 2018

@author: macbot4
"""

import webbrowser
import requests
import httplib2
from oauth2client.client import OAuth2WebServerFlow
from apiclient.discovery import build
from apiclient import errors
import logging

CLIENT_ID = "707910520551-l09mrjphooi2lqcr91dc1c58loap8klo.apps.googleusercontent.com"
CLIENT_SECRET = "Y8KvgxGCPPZCxBDko_Sr0W54"
SCOPES = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/spreadsheets"]

flow = OAuth2WebServerFlow(client_id=CLIENT_ID,
                           client_secret=CLIENT_SECRET,
                           scope=SCOPES,
                           redirect_uri='http://localhost:5000/google_auth_return')

spreadsheetId = "1oQ4EOboX5z7AjyfHi2PivS7bh4tHUhZW8jeQJYmix70"
sheetId = "Sample"

access_token = "ya29.GlxqBoU-nQ1-mn1XJ3I8_FUjzbdU8Mg8SrpQLuPMPGuO8bieLy3aAFsF1Dsbx94m-3eI49r3Xia3tBtkl_zUgKg0IF0zaw0U5TeylBPgrrpTgc0Wx8n768pFLx7ONQ "


def get_authCode():
    logging.info("SpreadsheetAPI: entering function get_authCode")
    auth_uri = flow.step1_get_authorize_url()
    # return auth_uri
    webbrowser.open(auth_uri)
    logging.info("SpreadsheetAPI: exiting function get_authCode")


def set_accessToken(auth_code):
    logging.info("SpreadsheetAPI: entering function set_accessToken")
    global credentials
    credentials = flow.step2_exchange(auth_code)

    global http
    http = credentials.authorize(httplib2.Http())

    global access_token
    access_token = credentials.access_token

    logging.info("SpreadsheetAPI: exiting function set_accessToken")


#    url = "https://www.googleapis.com/oauth2/v4/token"
#    data = {
#                "grant_type": "authorization_code",
#                "client_id": CLIENT_ID,
#                "client_secret": CLIENT_SECRET,
#                "code": auth_code
#            }
#
#    response = requests.post(url = url, data = data)
#    print(response.json())

def update_accessToken():
    logging.info("SpreadsheetAPI: entering function update_accessToken")
    global access_token
    global credentials
    access_token = credentials.access_token

    global http
    http = credentials.authorize(httplib2.Http())
    credentials.refresh(http)
    logging.info("SpreadsheetAPI: exiting function update_accessToken")



def watch_change():
    logging.info("SpreadsheetAPI: entering function watch_change")
    service = build('drive', 'v3', http=http)

    response = service.changes().getStartPageToken().execute()
    saved_start_page_token = response.get('startPageToken')

    page_token = saved_start_page_token

    while page_token is not None:
        response = service.changes().list(pageToken=page_token, spaces='drive').execute()

        for change in response.get('changes'):
            # Process change
            print('Change found for file: %s on %s' % (change.get('fileId'), change.get('time')))

        if 'newStartPageToken' in response:
            # Last page, save this token for the next polling interval
            saved_start_page_token = response.get('newStartPageToken')

        page_token = response.get('nextPageToken')

    logging.info("SpreadsheetAPI: exiting function watch_change")


def get_sheetData():
    logging.info("SpreadsheetAPI: entering function get_sheetData")
    url = "https://sheets.googleapis.com/v4/spreadsheets/" + spreadsheetId + "/values:batchGet?ranges=" + sheetId + "!O2:O&ranges=" + sheetId + "!H2:H"

    headers = {
        "x-origin": "https://developers.google.com",
        "authorization": "Bearer " + access_token
    }

    response = requests.get(url, headers=headers).json()

    logging.info("SpreadsheetAPI: exiting function get_sheetData")

    return [
        [item for cell in col['values'] for item in cell] for col in response['valueRanges']
    ]

