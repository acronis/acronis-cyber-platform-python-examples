#!/usr/bin/python
# -*- coding: utf-8 -*-

# ************************************************************
# Copyright © 2019-2021 Acronis International GmbH.
# This source code is distributed under MIT software license.
# ************************************************************

import requests  # used for sending requests to the API
import json      # used for manipulating JSON data
import pprint  # used for formatting the output of JSON objects received in API responses

import os
import sys
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, base_path)

from common.base_operations import Config, BearerAuth

# Initialize config and read all required values form JSON config
cfg = Config(full=True)

with open(os.path.join(base_path, 'customer.json')) as customer_file:
    customer = json.load(customer_file)

customer_tenant_id = customer["id"]


params = {
    'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer',
    'assertion': f'{cfg.access_token}',
    'scope': f'urn:acronis.com:tenant-id:{customer_tenant_id}'
}

# bc is that URL mean Backup Console
# At time of the scripts publication to receive a token
# with grant type urn:ietf:params:oauth:grant-type:jwt-bearer
# bc/idp/token need to be used.
response = requests.post(
    f'{cfg.base_url}bc/idp/token',
    headers={**cfg.header, **{'Content-Type': 'application/x-www-form-urlencoded'}},
    auth=BearerAuth(cfg.access_token),
    data=params
)

if response.ok:
    with open(os.path.join(base_path, 'api_customer_scoped_token.json'), 'w') as outfile:
        json.dump(response.json(), outfile)
    print("Customer scoped access token issued successfully.")
else:
    pprint.pprint(response.json())
