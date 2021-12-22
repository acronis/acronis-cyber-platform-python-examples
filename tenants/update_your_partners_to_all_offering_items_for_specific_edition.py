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

from common.base_operations import Config, Acronis

# Initialize config and read all required values form JSON config
# an API client and a token files
cfg = Config(full=True)
acronis = Acronis(cfg)

response = acronis.get(
     f'api/2/tenants/{cfg.tenant_id}/children'
)

if response.ok:
    children = response.json()["items"]

    if response.ok:

        for child_tenant in children:

            response = acronis.get(
                f'api/2/tenants/{child_tenant}/offering_items?edition={cfg.edition}'
            )

            not_enabled_offering_items = [item for item in response.json()["items"] if item["status"] == 0]

            if len(not_enabled_offering_items) > 0:

                for item in not_enabled_offering_items:
                    item["status"] = 1

                offering_items = json.loads('{"offering_items":[]}')
                offering_items["offering_items"] = not_enabled_offering_items

                response = acronis.put(
                    f'api/2/tenants/{child_tenant}/offering_items',
                    data=json.dumps(offering_items)
                )

                if response.ok:
                    print(f'{child_tenant} - all available offering itemd for {cfg.edition} edition enabled.')
                else:
                    pprint.pprint(response.json())
    else:
        pprint.pprint(response.json())
else:
    pprint.pprint(response.json())
