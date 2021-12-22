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

from common.base_operations import Config, BearerAuth, Tenant, id_generator, Acronis

# Initialize config and read all required values form JSON config
# an API client and a token files
cfg = Config(full=True)
acronis = Acronis(cfg)

partner = {
    "name": f"Python Locked Partner {id_generator()} v3.0",
    "parent_id": f"{cfg.tenant_id}",
    "kind": f"{cfg.partner_tenant}"
}

response = acronis.post(
     'api/2/tenants',
     data=json.dumps(partner)
)

if response.ok:

    new_partner = Tenant(json_str=response.text)

    response = acronis.get(
        f'api/2/tenants/{cfg.tenant_id}/offering_items/available_for_child?kind={cfg.partner_tenant}&edition={cfg.edition}'
    )

    if response.ok:

        offering_items = json.loads('{"offering_items":[]}')
        offering_items["offering_items"] = response.json()["items"]

        response = acronis.put(
            f'api/2/tenants/{new_partner.tenant_id}/offering_items',
            data=json.dumps(offering_items)
        )

        if response.ok:
            print(f"Offering items were set for tenant {new_partner.name}.")

            input("Press Enter to continue...")

            tenant_version = 1

            lock = {
                "update_lock": {
                        "owner_id": f"{cfg.tenant_id}",
                        "enabled": "true"
                },
                "version": f"{tenant_version}"
            }

            response = acronis.put(
                f'api/2/tenants/{new_partner.tenant_id}',
                data=json.dumps(lock)
            )

            if response.ok:
                print(f"The tenant {new_partner.name} was locked.")

                input("Press Enter to continue...")

                tenant_version = response.json()["version"]

                unlock = {
                    "update_lock": {
                        "enabled": "false"
                    },
                    "version": f"{tenant_version}"
                }

                response = acronis.put(
                    f'api/2/tenants/{new_partner.tenant_id}',
                    data=json.dumps(unlock)
                )
                if response.ok:
                    print(f"The tenant {new_partner.name} was unlocked.")

                    input("Press Enter to continue...")

                    update = {
                            "enabled": "false",
                            "version": f'{response.json()["version"]}'
                        }

                    response = acronis.put(
                        f'api/2/tenants/{new_partner.tenant_id}',
                        data=json.dumps(update)
                    )

                    if response.ok:

                        print(f"The tenant {new_partner.name} was disabled successfully.")

                        input("Press Enter to continue...")

                        response = acronis.delete(
                            f'api/2/tenants/{new_partner.tenant_id}?version={response.json()["version"]}'
                        )
                        if response.ok:
                            print(f"The tenant {new_partner.name} was deleted successfully.")
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
    else:
        pprint.pprint(response.json())
else:
    pprint.pprint(response.json())
