#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pprint import pprint

import requests
from bs4 import BeautifulSoup
import re


class api():
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def listservers(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, "
                          "like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "origin": "https://panel.cloudatcost.com",
            "referer": "https://panel.cloudatcost.com/login.php"}

        payload = {"username": self.email, "password": self.password, "submit": "Login"}
        with requests.Session() as s:
            s.get('https://panel.cloudatcost.com', headers=headers)
            s.post("https://panel.cloudatcost.com/manage-check2.php", headers=s.headers, data=payload)
            soup = BeautifulSoup(s.get("https://panel.cloudatcost.com").content, 'html5lib')
            server_ids = dict()
            for i in soup.find_all("td"):
                for i in i.find_all("button", "btn btn-group-sm btn-info"):
                    server_ids[
                                        str(i).split("Server ID:     &lt;/td&gt;&lt;td&gt; ")[1].rsplit("&")[0]] = {
                                        "id": str(i).split("Server ID:     &lt;/td&gt;&lt;td&gt; ")[1].rsplit("&")[0],
                                        "netmask": str(i).split("Netmask:&lt;/td&gt;&lt;td&gt; ")[1].rsplit("&")[0],
                                        "ip": str(i).split("IP Address:     &lt;/td&gt;&lt;td&gt; ")[1].rsplit("&")[0],
                                        "gateway": str(i).split("Gateway:&lt;/td&gt;&lt;td&gt; ")[1].rsplit("&")[0],
                                        "rootpass": str(i).split("Password:&lt;/td&gt;&lt;td&gt; ")[1].rsplit("&")[0],
                                        "mode": str(i).split("Run Mode:&lt;/td&gt;&lt;td&gt; ")[1].rsplit("&")[0]
                                    }
        return server_ids

    def getresources(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, "
                          "like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "origin": "https://panel.cloudatcost.com",
            "referer": "https://panel.cloudatcost.com/login.php"}
        payload = {"username": self.email, "password": self.password, "submit": "Login"}
        with requests.Session() as s:
            s.get('https://panel.cloudatcost.com', headers=headers)
            s.post("https://panel.cloudatcost.com/manage-check2.php", headers=s.headers, data=payload)
            soup_acount_number = BeautifulSoup(s.get("https://panel.cloudatcost.com").content, 'html5lib')
            account_resources = dict()
            for i in soup_acount_number.find_all("a", {"class": "btn btn-sm btn-default"}):
                accountnumber = str(i).split('onclick="cloudpro(')[0].split('addNote("')[-1].split('-cloudpro-')[0].rsplit("c")[1]
            soup_acount_resources = BeautifulSoup(s.get("https://panel.cloudatcost.com/panel/_config/pop/cloudpro.php?CNM={}".format(accountnumber)).content, 'html5lib')
            for i in soup_acount_resources.find_all("table"):
                for i in i.find_all("tr"):
                    for i in i.find_all('td'):
                        if "CPU" in str(i):
                            totalcpus = str(i).split(" CPU:")[0].rsplit('">')[1]
                        if "RAM" in str(i):
                            totalram = str(i).split(" MB RAM:")[0].rsplit('">')[1]
                        if " SSD:" in str(i):
                            totalstorage = str(i).split(" SSD:")[0].rsplit('">')[1].split(" ")[0]
                account_resources['Available'] = {"cpus": totalcpus, "ram": totalram, "storage": totalstorage}
        return account_resources


data = api("enter your email here but leave the quotes", "enter yourpassword in here but leave the quotes")
pprint(data.listservers())