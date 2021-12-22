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

from common.base_operations import Config

# Initialize config and read all required values form JSON config
cfg = Config(full=False)

with open(os.path.join(base_path, 'api_client.json')) as api_client_file:
    api_client_json = json.load(api_client_file)

client_id = api_client_json["client_id"]
client_secret = api_client_json["client_secret"]

response = requests.post(
    f'{cfg.base_url}api/2/idp/token',
    headers={**cfg.header, **{'Content-Type': 'application/x-www-form-urlencoded'}},
    auth=(client_id, client_secret),
    data={'grant_type': 'client_credentials'}
)

if response.ok:
    with open(os.path.join(base_path, 'api_token.json'), 'w') as outfile:
        json.dump(response.json(), outfile)
else:
    pprint.pprint(response.json())
