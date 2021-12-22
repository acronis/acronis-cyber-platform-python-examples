#!/usr/bin/python
# -*- coding: utf-8 -*-

# ************************************************************
# Copyright © 2019-2021 Acronis International GmbH.
# This source code is distributed under MIT software license.
# ************************************************************

import requests
import json			# used for manipulating JSON data
import pprint		# used for formatting the output of JSON objects received in API responses

import os
import sys
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, base_path)

from common.base_operations import Config, BearerAuth, User

# Initialize config and read all required values form JSON config
# an API client and a token files
cfg = Config(full=True)

user = User(os.path.join(base_path, "user.json"))

ott_request = {
  "purpose": "user_login",
  "login": f"{user.login}"
}

response = requests.post(
     f'{cfg.base_url}api/2/idp/ott',
     headers={**cfg.header, **{'Content-Type': 'application/json'}},
     auth=BearerAuth(cfg.access_token),
     data=json.dumps(ott_request)
)

if response.ok:

    session = requests.Session()

    response = session.post(
        f'{cfg.base_url}api/2/idp/ott/login',
        headers={**cfg.header, **{'Content-Type': 'application/json'}},
        auth=BearerAuth(cfg.access_token),
        data=response.text
    )

    if response.ok:
        response = session.get(
             f'{cfg.base_url}api/2/users/me',
             headers=cfg.header
        )

        if response.ok:
            print(f"The user {user.login} was successfully impersonated.")

            print(json.dumps(response.json(), indent=2))

            response = session.get(
                f'{cfg.base_url}api/2/idp/logout',
                headers=cfg.header
            )

            if response.ok:
                print(f"The user {user.login} was successfully logged out.")
            else:
                pprint.pprint(response.json())
        else:
            pprint.pprint(response.json())
    else:
        pprint.pprint(response.json())
else:
    pprint.pprint(response.json())
