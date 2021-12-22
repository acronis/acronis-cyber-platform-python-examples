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

from common.base_operations import Acronis, Config, Tenant, id_generator

# Initialize config and read all required values form JSON config
# an API client and a token files
cfg = Config(full=True)
acronis = Acronis(cfg)

partner = Tenant(os.path.join(base_path, 'partner.json'))

customer = {
    "name": f"Python Customer {id_generator()} v3.0",
    "parent_id": f"{partner.tenant_id}",
    "kind": f"{cfg.customer_tenant}"
}

response = acronis.post(
     'api/2/tenants',
     data=json.dumps(customer)
)

if response.ok:
    with open(os.path.join(base_path, 'customer.json'), 'w') as outfile:
        json.dump(response.json(), outfile)

    new_customer = Tenant(os.path.join(base_path, 'customer.json'))

    response = acronis.get(
        f'api/2/tenants/{cfg.tenant_id}/offering_items/available_for_child?kind={cfg.customer_tenant}&edition={cfg.edition}'
    )

    if response.ok:

        offering_items = json.loads('{"offering_items":[]}')
        offering_items_to_filter = response.json()["items"]

        # Only 1 location for a customer as well only 1 storage of 1 type
        # ba2976d0-c13e-4661-ae60-b4593583fce2 - Google DR storage for dev-cloud
        filtered_offering_items = [oi for oi in offering_items_to_filter if (oi["type"] == 'infra' and oi["infra_id"] != 'ba2976d0-c13e-4661-ae60-b4593583fce2') or (oi["type"] != 'infra')]
        filtered_offering_items = [oi for oi in filtered_offering_items if (oi["type"] == 'feature' and oi["usage_name"].startswith("dr_") and oi["infra_id"] != 'ba2976d0-c13e-4661-ae60-b4593583fce2') or (oi["type"] != 'feature') or not oi["usage_name"].startswith("dr_")]

        offering_items["offering_items"] = filtered_offering_items

        with open(os.path.join(base_path, 'customer_offering_items.json'), 'w') as outfile:
            json.dump(offering_items, outfile)

        response = acronis.put(
            f'api/2/tenants/{new_customer.tenant_id}/offering_items',
            data=json.dumps(offering_items)
        )

        if response.ok:
            print(f"Offering items were set for tenant {new_customer.tenant_id}")

            response = acronis.get(
                f'api/2/tenants/{new_customer.tenant_id}/pricing'
            )

            if response.ok:

                pricing = response.json()
                pricing["mode"] = "production"

                response = acronis.put(
                    f'api/2/tenants/{new_customer.tenant_id}/pricing',
                    data=json.dumps(pricing)
                )

                if response.ok:
                    print(f"Customer tenant {new_customer.tenant_id} pricing set to production mode.")
                else:
                    pprint.pprint(response.json())
            else:
                pprint.pprint(response.json())
        else:
            pprint.pprint(response.json())
    else:
        pprint.pprint(response.json())
else:
    pprint.pprint(response.json())
