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

from common.base_operations import Config, BearerAuth, Tenant, Acronis, id_generator

# Initialize config and read all required values form JSON config
# an API client and a token files
cfg = Config(full=True)
acronis = Acronis(cfg)

partner = {
    "name": f"Python Partner All Editions {id_generator()} v3.0",
    "parent_id": f"{cfg.tenant_id}",
    "kind": f"{cfg.partner_tenant}"
}

response = acronis.post(
     'api/2/tenants',
     data=json.dumps(partner)
)

if response.ok:
    with open(os.path.join(base_path, 'partner_all_editions.json'), 'w') as outfile:
        json.dump(response.json(), outfile)

    new_partner = Tenant(os.path.join(base_path, 'partner_all_editions.json'))

    response = acronis.get(
        f'api/2/tenants/{cfg.tenant_id}/offering_items/available_for_child?kind={cfg.partner_tenant}&edition=*'
    )

    if response.ok:

        offering_items = json.loads('{"offering_items":[]}')
        offering_items["offering_items"] = response.json()["items"]

        response = acronis.put(
            f'api/2/tenants/{new_partner.tenant_id}/offering_items',
            data=json.dumps(offering_items)
        )

        if response.ok:
            print(f"Offering items were set for tenant {new_partner.tenant_id}")
        else:
            pprint.pprint(response.json())
    else:
        pprint.pprint(response.json())
else:
    pprint.pprint(response.json())
