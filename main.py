# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (c) 2022 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

__author__ = "Simon Fang <sifang@cisco.com>"
__copyright__ = "Copyright (c) 2022 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime
from config import MERAKI_ORGANIZATION_NAME, SSID, NETWORK_ID
import sys

# Load environment variables
load_dotenv()

# Read environment variables
MERAKI_EMAIL = os.getenv('MERAKI_EMAIL')
MERAKI_PASSWORD = os.getenv('MERAKI_PASSWORD')
MERAKI_API_KEY = os.getenv('MERAKI_API_KEY')

BASE_URL = "https://account.meraki.com"
MERAKI_API_URL = "https://dashboard.meraki.com/api"

# Establish a session
session = requests.Session()

# Helper functions
def post_login_credentials():
    print("*** Posting the login credentials to the dashboard ***")
    url = f'{BASE_URL}/login/login'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    body = {
        'email': MERAKI_EMAIL,
        'password': MERAKI_PASSWORD
    }
    response = session.post(url, data=body, headers=headers)
    if response.ok:
        print("*** The login credentials were successfully posted ***")
        

def get_org_url_from_org_list():
    print("*** Getting the org url from the org list ***")
    url = f'{BASE_URL}/login/org_list'
    response = session.get(url)
    if response.ok:
        print("*** The org list was successfully obtained ***")

    soup = BeautifulSoup(response.content, 'html.parser')

    print(soup.find_all('a'))

    for tag in soup.find_all('a'):
        if MERAKI_ORGANIZATION_NAME in tag:
            org_url = tag.get('href')
            return org_url
    # Could not find org url
    print(f"Org_url could not be obtained for {MERAKI_ORGANIZATION_NAME}")
    return None

def get_dashboard_base_url(org_url):
    print("*** Getting the dashboard base url ***")
    # Choose org
    url = f'{BASE_URL}{org_url}'
    response = session.get(url)
    if response.history:
        print("The request was redirected to the following dashboard url:")
        # Obtain last redirect url
        dashboard_url = response.history[-1].url
        # Remove dashboard from dashboard url
        DASHBOARD_BASE_URL = dashboard_url[:-10]
        print(DASHBOARD_BASE_URL)
        return DASHBOARD_BASE_URL
    else:
        print("Request was not redirected")
        return 

def get_clients_connected_to_guest_SSID():
    print("Let's obtain the clients connected to the guest SSID")
    url = f'{MERAKI_API_URL}/v0/networks/{NETWORK_ID}/clients'
    headers = {
        'X-Cisco-Meraki-API-Key': MERAKI_API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.ok:
        print("*** The list of clients connected to the guest SSID was successfully obtained ***")
    response.raise_for_status()
    guest_clients = []
    for client in response.json():
        if client['ssid'] == SSID:
            guest_clients.append(client['id'])

    return guest_clients

def get_AP_from_clients_endpoint(DASHBOARD_BASE_URL, client_id):
    url = f"{MERAKI_API_URL}/v1/networks/{NETWORK_ID}/clients?perPage=1000" #adapt code if there are more than 1000 clients
    headers = {
        'X-Cisco-Meraki-API-Key': MERAKI_API_KEY
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    clients = response.json()
    for client in clients:
        if client["id"] == client_id:
            ap = client["recentDeviceName"]
            return ap
    return None

def get_date_time_from_last_seen(epoch_time):
    date_time = datetime.fromtimestamp(int(epoch_time))
    date_time_string_format = date_time.strftime('%Y/%m/%d %H:%M')
    return date_time_string_format

def get_splash_info_per_client_id(DASHBOARD_BASE_URL, client_id):
    url = f"{DASHBOARD_BASE_URL}/usage/client_show/{client_id}?t0=&t1=&timespan=86400&filter="
    headers = {
        'X-Requested-With': 'XMLHttpRequest'
    }

    response = session.get(url=url, headers=headers)
    if response.ok:
        print("*** The splash infos per client ID was successfully obtained ***")

    splash_info = {}
    client_info = response.json()

    splash_info['description'] = client_info['description']
    splash_info['last_seen'] = get_date_time_from_last_seen(client_info['last_seen'])
    splash_info['os'] = client_info['os']
    splash_info['ip'] = client_info['ip']
    splash_info['mac'] = client_info["mac"]
    splash_info['sponsor_email'] = client_info['wireless_bigacl'][0]['sponsor_email']
    splash_info['authorized'] = client_info['wireless_bigacl'][0]['authorized']
    splash_info['expires'] = client_info['wireless_bigacl'][0]['expires']
    splash_info['AP'] = get_AP_from_clients_endpoint(DASHBOARD_BASE_URL, client_id)
    splash_info['ssid'] = client_info["ssid_name"]
    return splash_info

def write_to_csv_from_splash_infos(splash_infos):
    try:
        print("*** Writing to csv ***")
        df = pd. DataFrame(splash_infos)
        file_path = f"csv_reports/{datetime.now().strftime('%Y%m%d_%H%M')}_splash_infos_{SSID.replace(' ', '_')}.csv"
        csv = df.to_csv(file_path, index=False)
        print("*** Writing to csv was successful***")
        print(f"*** The file can be found here: {file_path}")
    except Exception as e:
        print(e)

# Main function
def main():
    # Log in to Meraki Dashboard
    post_login_credentials()

    # Get list of organizations
    org_url = get_org_url_from_org_list()

    # If none, then exit
    if not org_url:
        sys.exit()

    # Get dashboard base url from org url
    DASHBOARD_BASE_URL = get_dashboard_base_url(org_url)

    # Get list of clients connected to a specific SSID
    guest_clients =  get_clients_connected_to_guest_SSID()

    splash_infos = []
    # Get splash info per client id
    for client_id in guest_clients:
        splash_info = get_splash_info_per_client_id(DASHBOARD_BASE_URL, client_id)
        splash_infos.append(splash_info)

    # Convert to CSV
    write_to_csv_from_splash_infos(splash_infos)


if __name__ == "__main__":
    main()