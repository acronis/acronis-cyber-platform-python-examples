#!/usr/bin/python
# -*- coding: utf-8 -*-

# ************************************************************
# Copyright © 2019-2021 Acronis International GmbH.
# This source code is distributed under MIT software license.
# ************************************************************

import json			# used for manipulating JSON data

import os
import sys
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, base_path)

from common.base_operations import Acronis, Config, BearerAuth, Tenant

# Initialize config and read all required values form JSON config
# an API client and a token files
cfg = Config(full=True)
acronis = Acronis(cfg)

query = input("Search for: ")

response = acronis.get(
        f'api/2/search?text={query}&tenant={cfg.tenant_id}'
    )

if response.ok:
    print(json.dumps(response.json(), indent=2, sort_keys=True))
else:
    print(f"The request was not OK. There is in the error status code: {response.status_code}")
