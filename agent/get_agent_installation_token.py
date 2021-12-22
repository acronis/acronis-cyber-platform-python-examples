#!/usr/bin/python
# -*- coding: utf-8 -*-

# ************************************************************
# Copyright © 2019-2021 Acronis International GmbH.
# This source code is distributed under MIT software license.
# ************************************************************

from time import clock_getres
import json			# used for manipulating JSON data
import pprint		# used for formatting the output of JSON objects received in API responses
import os
import sys

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, base_path)

from common.base_operations import Config, Tenant, Acronis

# Initialize config and read all required values form JSON config
# an API client and a token files
cfg = Config(full=True)
acronis = Acronis(cfg)

user = Tenant(os.path.join(base_path, 'user.json'))

token_request = {
  "expires_in": 3600,
  "scopes": [
   "urn:acronis.com:tenant-id::backup_agent_admin"
  ]
}

response = acronis.post(
    f'api/2/tenants/{user.id}/registration_tokens',
    data=json.dumps(token_request)
)

if response.ok:
    with open(os.path.join(base_path, 'agent_installation_token.json'), 'w') as outfile:
        json.dump(response.json(), outfile)
else:
    pprint.pprint(response.json())
