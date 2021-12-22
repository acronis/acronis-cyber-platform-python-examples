#!/usr/bin/python
# -*- coding: utf-8 -*-

# ************************************************************
# Copyright © 2019-2021 Acronis International GmbH.
# This source code is distributed under MIT software license.
# ************************************************************

import json
import os
import sys
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, base_path)

from common.base_operations import Acronis, Config, BearerAuth, Tenant, User


def print_base_tenant_info(tenant_id, acronis: Acronis):
    response = acronis.get(
        f'api/2/tenants/{tenant_id}'
    )

    if response.ok:
        tenant = Tenant(json_str=response.text)
        print(f"{tenant.name}")


def disable_delete_tenant(tenant_id, acronis: Acronis):

    response = acronis.get(
        f'api/2/tenants/{tenant_id}'
    )

    if response.ok:
        tenant = Tenant(json_str=response.text)
        update_tenant = {
                        "version": f"{tenant.version}",
                        "enabled": f"false"
        }
        response = acronis.put(
                   f'api/2/tenants/{tenant_id}',
                   data=json.dumps(update_tenant)
                )
        if response.ok:
            print(f"{tenant.name} -- disabled.")
            response = acronis.get(
                        f'api/2/tenants/{tenant_id}'
                    )
            if response.ok:
                tenant = Tenant(json_str=response.text)

                response = acronis.delete(
                            f'api/2/tenants/{tenant_id}?version={tenant.version}'
                        )
                if response.ok:
                        print(f"{tenant.name} -- deleted.")


def get_child_tenants(tenant_id, acronis: Acronis):

    response = acronis.get(
        f'api/2/tenants/{tenant_id}/children'
    )

    if response.ok:
        for child_tenant_id in response.json()["items"]:
            #print(f"The tenant {tenant_id} has the child tenant {child_tenant_id} with name ", end='')
            #print_base_tenant_info(child_tenant_id, acronis)
            disable_delete_tenant(child_tenant_id, acronis)


# Initialize config and read all required values form JSON config
# an API client and a token files
cfg = Config(full=True)
acronis = Acronis(cfg)

print(F"The root tenant is {cfg.tenant_id} with name ", end='')
print_base_tenant_info(cfg.tenant_id, acronis)

get_child_tenants(cfg.tenant_id, acronis)
