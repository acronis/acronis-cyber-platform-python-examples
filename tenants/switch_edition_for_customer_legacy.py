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

from common.base_operations import Acronis, Config, BearerAuth, Tenant, id_generator

# Initialize config and read all required values form JSON config
# an API client and a token files
cfg = Config(full=True)
acronis = Acronis(cfg)

partner = {
    "name": f"Python Switch Edition Customer {id_generator()} v3.0",
    "parent_id": f"{cfg.tenant_id}",
    "kind": f"{cfg.customer_tenant}"
}

response = acronis.post(
     'api/2/tenants',
     data=json.dumps(partner)
)

if response.ok:

    new_customer = Tenant(json_str=response.text)

    response = acronis.get(
        f'api/2/tenants/{cfg.tenant_id}/offering_items/available_for_child?kind={cfg.customer_tenant}&edition={cfg.edition}'
    )

    if response.ok:

        offering_items = json.loads('{"offering_items":[]}')

        # Only 1 location for a csutomer as well only 1 strage of 1 type
        # ba2976d0-c13e-4661-ae60-b4593583fce2 - Google DR storage for dev-cloud
        filtered_offering_items = [oi for oi in response.json()["items"] if (oi["type"] == 'infra' and oi["infra_id"] != 'ba2976d0-c13e-4661-ae60-b4593583fce2') or (oi["type"] != 'infra')]
        filtered_offering_items = [oi for oi in filtered_offering_items if (oi["type"] == 'feature' and oi["usage_name"].startswith("dr_") and oi["infra_id"] != 'ba2976d0-c13e-4661-ae60-b4593583fce2') or (oi["type"] != 'feature') or not oi["usage_name"].startswith("dr_")]

        offering_items["offering_items"] = filtered_offering_items

        response = acronis.put(
            f'api/2/tenants/{new_customer.tenant_id}/offering_items',
            data=json.dumps(offering_items)
        )

        if response.ok:
            print(f"Offering items for {cfg.edition} edition were set for tenant {new_customer.name}.")

            input("Press Enter to continue...")

            response = acronis.get(
                f'api/2/tenants/{cfg.tenant_id}/offering_items/available_for_child?kind={cfg.customer_tenant}&edition={cfg.switch_edition}'
            )

            if response.ok:
                disabled_offering_items = [
                    offering_item for offering_item in offering_items["offering_items"]
                    if (
                         offering_item["edition"] == cfg.edition
                    )
                    ]

                for offering_item in disabled_offering_items:
                    offering_item["status"] = 0

                enabled_offering_items = [
                    offering_item for offering_item in response.json()["items"]
                    if (
                         offering_item["edition"] == cfg.switch_edition
                    )
                    ]

                for offering_item in enabled_offering_items:
                    offering_item["status"] = 1

                 # Only 1 location for a csutomer as well only 1 strage of 1 type
                # ba2976d0-c13e-4661-ae60-b4593583fce2 - Google DR storage for dev-cloud
                filtered_offering_items = [oi for oi in enabled_offering_items if (oi["type"] == 'infra' and oi["infra_id"] != 'ba2976d0-c13e-4661-ae60-b4593583fce2') or (oi["type"] != 'infra')]
                filtered_offering_items = [oi for oi in filtered_offering_items if (oi["type"] == 'feature' and oi["usage_name"].startswith("dr_") and oi["infra_id"] != 'ba2976d0-c13e-4661-ae60-b4593583fce2') or (oi["type"] != 'feature') or not oi["usage_name"].startswith("dr_")]

                offering_items_list = disabled_offering_items + filtered_offering_items

                offering_items = json.loads('{"offering_items":[]}')
                offering_items["offering_items"] = offering_items_list

                response = acronis.put(
                    f'api/2/tenants/{new_customer.tenant_id}/offering_items',
                    data=json.dumps(offering_items)
                )

                if response.ok:
                    print(f"The tenant {new_customer.name} was switched from {cfg.edition} to {cfg.switch_edition} successfully.")
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
