#!/usr/bin/python
# -*- coding: utf-8 -*-

# ************************************************************
# Copyright © 2019-2021 Acronis International GmbH.
# This source code is distributed under MIT software license.
# ************************************************************

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


def print_base_user_info(user_id, acronis: Acronis):
    response = acronis.get(
        f'api/2/users/{user_id}'
    )

    if response.ok:
        user = User(json_str=response.text)
        print(f"{user.login}")


def get_tenant_users(tenant_id, acronis: Acronis):

    response = acronis.get(
        f'api/2/tenants/{tenant_id}/users'
    )

    if response.ok:
        for user_id in response.json()["items"]:
            print(f"The tenant {tenant_id} has user {user_id} with login ", end='')
            print_base_user_info(user_id, acronis)


def get_child_tenants(tenant_id, acronis: Acronis):

    response = acronis.get(
        f'api/2/tenants/{tenant_id}/children'
    )

    if response.ok:
        for child_tenant_id in response.json()["items"]:
            print(f"The tenant {tenant_id} has the child tenant {child_tenant_id} with name ", end='')
            print_base_tenant_info(child_tenant_id, acronis)
            get_tenant_users(child_tenant_id, acronis)
            get_child_tenants(child_tenant_id, acronis)


# Initialize config and read all required values form JSON config
# an API client and a token files
cfg = Config(full=True)
acronis = Acronis(cfg)

print(F"The root tenant is {cfg.tenant_id} with name ", end='')
print_base_tenant_info(cfg.tenant_id, acronis)

get_child_tenants(cfg.tenant_id, acronis)
