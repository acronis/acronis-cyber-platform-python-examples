#!/usr/bin/python
# -*- coding: utf-8 -*-

# ************************************************************
# Copyright © 2019-2021 Acronis International GmbH.
# This source code is distributed under MIT software license.
# ************************************************************

import pprint		# used for formatting the output of JSON objects received in API responses

import os
import sys
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, base_path)

from common.base_operations import Config, BearerAuth, Tenant, Acronis

# Initialize config and read all required values form JSON config
# an API client and a token files
cfg = Config(full=True)
acronis = Acronis(cfg)

response = acronis.get(
        f'api/2/applications'
    )

platform_id = None

if response.ok:
    platform = [
        application for application in response.json()["items"]
        if (
            application["type"] == "platform"
        )
        ]

    if len(platform) == 1:
        platform_id = platform[0]["id"]
    else:
        print("The platform application should be only one.")
        exit
else:
    pprint.pprint(response.json())
    exit

customer = Tenant(os.path.join(base_path, "customer.json"))

response = acronis.get(
        f'api/2/tenants/{customer.tenant_id}/applications'
    )

if response.ok:
    for application_id in response.json()["items"]:
        if application_id != platform_id:
            response = acronis.delete(
                f'api/2/applications/{application_id}/bindings/tenants/{customer.tenant_id}'
            )
            if response.ok:
                print(f"The application {application_id} was disable successfully for the tenant {customer.tenant_id}.")
            else:
                pprint.pprint(response.json())
else:
    pprint.pprint(response.json())
