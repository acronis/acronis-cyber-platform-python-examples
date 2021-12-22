#!/usr/bin/python
# -*- coding: utf-8 -*-

# ************************************************************
# Copyright © 2019-2021 Acronis International GmbH.
# This source code is distributed under MIT software license.
# ************************************************************

import json			# used for manipulating JSON data
import pprint		# used for formatting the output of JSON objects received in API responses

import os
import sys

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, base_path)

from common.base_operations import Config, BearerAuth, Tenant, User, Acronis

# Initialize config and read all required values form JSON config
# an API client and a token files
cfg = Config(full=True)
acronis = Acronis(cfg)

login = input("New login: ")
email = input("Please enter a valid email, it will be used for account activation: ")

response = acronis.get(
    f"api/2/users/check_login?username={login}"
)

if response.ok and response.status_code == 204:
    customer = Tenant(os.path.join(base_path, "customer.json"))

    user = {
        "tenant_id": f"{customer.tenant_id}",
        "login": f"{login}",
        "contact": {
            "email": f"{email}",
            "firstname": f"First {login}",
            "lastname": f"Last {login}"
            }
        }

    response = acronis.post(
        'api/2/users',
        data=json.dumps(user)
    )

    if response.ok:
        with open(os.path.join(base_path, 'user.json'), 'w') as outfile:
            json.dump(response.json(), outfile)

        new_user = User(os.path.join(base_path, 'user.json'))

        response = acronis.post(
            f'api/2/users/{new_user.id}/send-activation-email'
        )

        if response.ok:
            print(f"User {login} is activated by sending an e-mail.")

            user_role = {
                            "items": [
                                {
                                    "id": "00000000-0000-0000-0000-000000000000",
                                    "issuer_id": "00000000-0000-0000-0000-000000000000",
                                    "role_id": "backup_user",
                                    "tenant_id": f"{customer.tenant_id}",
                                    "trustee_id": f"{new_user.id}",
                                    "trustee_type": "user",
                                    "version": 0
                                }
                            ]
                        }

            response = acronis.put(
                f'api/2/users/{new_user.id}/access_policies',
                data=json.dumps(user_role)
            )

            if response.ok:
                print(f"User {login} is assigned a backup user role.")
            else:
                pprint.pprint(response.json())
        else:
            pprint.pprint(response.json())
    else:
        pprint.pprint(response.json())
else:
    pprint.pprint(response.json())
