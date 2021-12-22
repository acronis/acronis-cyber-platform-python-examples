#!/usr/bin/python
# -*- coding: utf-8 -*-

# ************************************************************
# Copyright © 2019-2021 Acronis International GmbH.
# This source code is distributed under MIT software license.
# ************************************************************
import getpass   # used to securely read password from a command line
import requests  # used for sending requests to the API
import json      # used for manipulating JSON data
import pprint    # used for formatting the output of JSON objects received in API responses

import os
import sys
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, base_path)

# base classes to support generic functionality
from common.base_operations import Config

# Initialize config and read values form JSON config (full=False)
cfg = Config(full=False)

# Read username and password from a command line
username = input("Username: ")
password = getpass.getpass(prompt="Password: ")

# Request information about a user which is authenticated by
# username and password - Basic Authentication
response = requests.get(
    f'{cfg.base_url}api/2/users/me',
    auth=(username, password)
)

if response.ok:
    # Read tenant_id from received JSON
    my_tenant_id = response.json()["tenant_id"]

    # Build an object represents an API Client creation request JSON body
    client = {
        "type": "api_client",
        "tenant_id": f"{my_tenant_id}",
        "token_endpoint_auth_method": "client_secret_basic",
        "data": {
            "client_name": "Python.Client"
        }
    }

    # Create an API Client with Basic Authentication
    response = requests.post(
        f'{cfg.base_url}api/2/clients',
        headers={**cfg.header, **{'Content-Type': 'application/json'}},
        auth=(username, password),
        data=json.dumps(client)
    )

    if response.ok:
        # Save the created API Client info to api_client.json file
        with open(os.path.join(base_path, 'api_client.json'), 'w') as outfile:
            json.dump(response.json(), outfile)
    else:
        pprint.pprint(response.json())
else:
    pprint.pprint(response.json())
