#!/usr/bin/python
# -*- coding: utf-8 -*-

# ************************************************************
# Copyright © 2019-2021 Acronis International GmbH.
# This source code is distributed under MIT software license.
# ************************************************************

import json
import os.path
from typing import Any
import requests
import pprint
import random       # to generate random string
import string       # to generate random string

from time import time

import os
import sys

base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, base_path)


class BearerAuth(requests.auth.AuthBase):

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["Authorization"] = "Bearer " + self.token
        return r


class Tenant:

    __tenant = None

    tenant_id = None
    name = None
    version = None

    def __init__(self, file_path: str = None, json_str: str = None):

        if json_str is None:
            self.__read_tenant(file_path)
        else:
            self.__tenant = json.loads(json_str)

        self.tenant_id = self.__tenant["id"]
        self.name = self.__tenant["name"]
        self.version = self.__tenant["version"]

    def __read_tenant(self, file_path: str):
        if os.path.exists(file_path):
            with open(file_path) as tenant_file:
                self.__tenant = json.load(tenant_file)


class User:

    __user = None

    id = None
    personal_tenant_id = None
    login = None

    def __init__(self, file_path: str = None, json_str: str = None):

        if json_str is None:
            self.__read_user(file_path)
        else:
            self.__user = json.loads(json_str)

        self.id = self.__user["id"]
        self.login = self.__user["login"]
        self.personal_tenant_id = self.__user["personal_tenant_id"]

    def __read_user(self, file_path: str):
        if os.path.exists(file_path):
            with open(file_path) as user_file:
                self.__user = json.load(user_file)


class Config:

    __cfg = None
    __cgf_default = None
    __api_client = None
    __api_token = None
    __api_scoped_token = None

    base_url = None
    partner_tenant = None
    customer_tenant = None
    edition = None
    switch_edition = None
    header = None
    cyber_protection_application_id = None

    client_id = None
    client_secret = None

    access_token = None
    scoped_access_token = None

    tenant_id = None

    def __init__(self, full: bool):
        if full:
            self.__read_config()
            self.base_url = self.__cfg.get("base_url", self.__сfg_default["base_url"])
            self.partner_tenant = self.__cfg.get("partner_tenant", self.__сfg_default["partner_tenant"])
            self.customer_tenant = self.__cfg.get("customer_tenant", self.__сfg_default["customer_tenant"])
            self.edition = self.__cfg.get("edition", self.__сfg_default["edition"])
            self.switch_edition = self.__cfg.get("switch_edition", self.__сfg_default["switch_edition"])
            self.cyber_protection_application_id = self.__cfg.get("cyber_protection_application_id", self.__сfg_default["cyber_protection_application_id"])

            self.__read_client()
            self.client_id = self.__api_client["client_id"]
            self.client_secret = self.__api_client["client_secret"]
            self.tenant_id = self.__api_client["tenant_id"]

            self.__read_token()
            self.access_token = self.__api_token["access_token"]

            self.__read_scoped_token()
            if self.__api_scoped_token is not None:
                self.scoped_access_token = self.__api_scoped_token["access_token"]

            self.header = {"User-Agent": "ACP 1.0/Acronis Cyber Platform Python Examples"}
        else:
            self.__read_config()
            self.base_url = self.__cfg.get("base_url", self.__сfg_default["base_url"])
            self.partner_tenant = self.__cfg.get("partner_tenant", self.__сfg_default["partner_tenant"])
            self.customer_tenant = self.__cfg.get("customer_tenant", self.__сfg_default["customer_tenant"])
            self.edition = self.__cfg.get("edition", self.__сfg_default["edition"])
            self.switch_edition = self.__cfg.get("switch_edition", self.__сfg_default["switch_edition"])
            self.cyber_protection_application_id = self.__cfg.get("cyber_protection_application_id", self.__сfg_default["cyber_protection_application_id"])

            self.header = {"User-Agent": "ACP 3.0/Acronis Cyber Platform Python Examples"}

    def __read_config(self):

        if os.path.exists(os.path.join(base_path, 'cyber.platform.cfg.json')):
            with open(os.path.join(base_path,'cyber.platform.cfg.json')) as сfg_file:
                self.__cfg = json.load(сfg_file)

        if os.path.exists(os.path.join(base_path,'cyber.platform.cfg.defaults.json')):
            with open(os.path.join(base_path,'cyber.platform.cfg.defaults.json')) as сfg_default_file:
                self.__сfg_default = json.load(сfg_default_file)

    def __read_client(self):
        if os.path.exists(os.path.join(base_path, 'api_client.json')):
            with open(os.path.join(base_path, 'api_client.json')) as api_client_file:
                self.__api_client = json.load(api_client_file)
        else:
            print("The api_client.json file doesn't exist.")

    def __read_token(self):
        if os.path.exists(os.path.join(base_path, 'api_token.json')):
            with open(os.path.join(base_path, 'api_token.json')) as api_token_file:
                self.__api_token = json.load(api_token_file)
                expires_on = self.__api_token["expires_on"]
                if expires_on - time() < 900:
                    if os.path.exists(os.path.join(base_path, 'api_customer_scoped_token.json')):
                        self.scoped_access_token = None
                        print("Warning: A customer scoped token expired and deleted. Please re-issue manually.")
                        os.remove(os.path.join(base_path, 'api_customer_scoped_token.json'))
                    self.__issue_token()
        else:
            self.__issue_token()

    def __read_scoped_token(self):
        if os.path.exists(os.path.join(base_path, 'api_customer_scoped_token.json')):
            with open(os.path.join(base_path, 'api_customer_scoped_token.json')) as api_token_file:
                self.__api_scoped_token = json.load(api_token_file)
        else:
            print("Warning: There is no any customer scoped token. Please, issue if need.")

    def __issue_token(self):
        if os.path.exists(os.path.join(base_path, 'api_client.json')):
            client_id = self.__api_client["client_id"]
            client_secret = self.__api_client["client_secret"]

            response = requests.post(
                f'{self.base_url}api/2/idp/token',
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                auth=(client_id, client_secret),
                data={'grant_type': 'client_credentials'}
            )

            if response.ok:
                self.__api_token = response.json()
                self.access_token = self.__api_token["access_token"]
                with open(os.path.join(base_path, 'api_token.json'), 'w') as outfile:
                    json.dump(self.__api_token, outfile)
            else:
                pprint.pprint(response.json())


# Copied from https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class Acronis:

    __cfg = None
    __auth = None

    def __init__(self, cfg: Config):
        self.__cfg = cfg
        if cfg.scoped_access_token is not None:
            print("Warning: A customer scoped token is used for authentication.")
            self.__auth = BearerAuth(self.__cfg.scoped_access_token)
        else:
            self.__auth = BearerAuth(self.__cfg.access_token)

    def get(self, uri: str, data: Any = None):
        return requests.get(
            f'{self.__cfg.base_url}{uri}',
            params=data,
            headers=self.__cfg.header,
            auth=self.__auth
            )

    def delete(self, uri: str, data: Any = None):
        return requests.delete(
            f'{self.__cfg.base_url}{uri}',
            params=data,
            headers=self.__cfg.header,
            auth=self.__auth
            )

    def post(self, uri: str, data: Any = None):
        return requests.post(
            f'{self.__cfg.base_url}{uri}',
            headers={**self.__cfg.header, **{'Content-Type': 'application/json'}},
            auth=self.__auth,
            data=data
            )

    def put(self, uri: str, data: Any = None):
        return requests.put(
            f'{self.__cfg.base_url}{uri}',
            headers={**self.__cfg.header, **{'Content-Type': 'application/json'}},
            auth=self.__auth,
            data=data
            )
