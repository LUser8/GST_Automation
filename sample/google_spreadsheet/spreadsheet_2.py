#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 15:44:19 2018

@author: macbot4
"""

import webbrowser
import requests
import httplib2
import pandas as pd
import datetime
from pprint import pprint

from oauth2client.client import OAuth2WebServerFlow, OAuth2Credentials
from apiclient.discovery import build
from apiclient import errors

CLIENT_ID = "707910520551-l09mrjphooi2lqcr91dc1c58loap8klo.apps.googleusercontent.com"
CLIENT_SECRET = "Y8KvgxGCPPZCxBDko_Sr0W54"
SCOPES = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/spreadsheets"]

flow = OAuth2WebServerFlow(client_id=CLIENT_ID,
                       client_secret=CLIENT_SECRET,
                       scope=SCOPES,
                       redirect_uri='http://localhost:5000/google_auth_return')

spreadsheetId = "1oQ4EOboX5z7AjyfHi2PivS7bh4tHUhZW8jeQJYmix70"
sheetId = "Sample"
spreadsheet = None


def get_authCode():
    
    auth_uri = flow.step1_get_authorize_url()
    return auth_uri
#    webbrowser.open(auth_uri)


def init_credentials(auth_code=None, fromfile=None):
    global credentials, http
    
    if fromfile:
        with open(fromfile) as f:
            credentials = OAuth2Credentials.new_from_json(f.read())
    
    if auth_code:
        credentials = flow.step2_exchange(auth_code)
        
    http = credentials.authorize(httplib2.Http())
    
    set_accessToken()


def write_credentials():
    with open("credentials.json", 'w') as f:
            f.write(credentials.to_json())


def set_accessToken():
    
    global access_token
    access_token = credentials.access_token
    
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
        
    global access_token
    global credentials
    global http
    
    access_token = credentials.access_token
    
    credentials.refresh(httplib2.Http())
    http = credentials.authorize(httplib2.Http())


def watch_change():
    service = build('drive', 'v3', http=http)
    
    response = service.changes().getStartPageToken().execute()
    saved_start_page_token = response.get('startPageToken')
    
    page_token = saved_start_page_token
    last_time = ""
    while page_token is not None:
        response = service.changes().list(pageToken=page_token, spaces='drive').execute()
        
        for change in response.get('changes'):                
            # Process change            
            if (change.get('fileId') == spreadsheetId and change.get('time') != last_time):
                last_time = change.get('time')
                
                print('Change found for file: %s' % change.get('fileId'))
            
        if 'newStartPageToken' in response:
            # Last page, save this token for the next polling interval
            saved_start_page_token = response.get('newStartPageToken')

#        page_token = response.get('nextPageToken')


def get_sheetData():
    
    url = "https://sheets.googleapis.com/v4/spreadsheets/"+spreadsheetId+"/values/"+sheetId
#    url = "https://sheets.googleapis.com/v4/spreadsheets/"+spreadsheetId+"/values:batchGet?ranges="+sheetId+"!O2:O&ranges="+sheetId+"!H2:H&majorDimension=COLUMNS"

    headers = {
                "x-origin": "https://developers.google.com",
                "authorization": "Bearer " + access_token
              }
    
    response = requests.get(url, headers=headers).json()
    
    if response.get("error", False):
        print("Updating access token")
        update_accessToken()
        return get_sheetData()
    
    df = pd.DataFrame(response['values'][1:], columns=response['values'][0])
    
    df['Last Checked'] = pd.to_datetime(df['Last Checked'])
    
    global spreadsheet
    spreadsheet = df
    
    selects = ['ID', ' Ticket No ', ' Airline/Hotel Name ', 'Email address', 'Fetched Flag', 'Last Checked']
    
    return df[(df['Fetched Flag'] == "N") | ((df['Fetched Flag'] == "W") & (pd.Series([delta.seconds//3600 for delta in (datetime.datetime.now() - df['Last Checked'])]) > 0))][selects]
    
#    return [
#        ranges['values'][0] for ranges in response['valueRanges']
#        ]
#    return [
#            [item for cell in col['values'] for item in cell] for col in response['valueRanges']
#            ]


def columnToLetter(column):
    letter = ''
    while (column > 0): 
        temp = (column - 1) % 26
        letter = chr(int(temp) + 65) + letter
        column = (column - temp - 1) / 26
    return letter


def get_row(idCol, value):
    return spreadsheet.index[spreadsheet[idCol] == value].tolist()[0] + 1


def get_col(idCol):
    return columnToLetter(spreadsheet.columns.get_loc(idCol) + 1)


def make_hit(place, value):
    
    url = "https://sheets.googleapis.com/v4/spreadsheets/"+spreadsheetId+"/values/"+place+ "?valueInputOption=USER_ENTERED"

    headers = {
                "x-origin": "https://developers.google.com",
                "authorization": "Bearer " + access_token
              }
    data = "{'values':[['" + str(value) + "']]}"
    
    response = requests.put(url, data=data, headers=headers).json()
    
    if response.get("error", False):
        print("Updating access token")
        update_accessToken()
        return get_sheetData()


def update_sheetData(data):
    if spreadsheet is None:
        get_sheetData()
    
    idCol = 'ID'
    
    # row = get_row(idCol, data[idCol]) + 1
    row = data[idCol] + 1
    
    for key, value in data.items():
        
        if key != idCol:
            col = get_col(key)
            make_hit(str(col) + "" + str(row), value)