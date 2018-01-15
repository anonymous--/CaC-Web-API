import requests
from bs4 import BeautifulSoup
from pprint import pprint


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
            for i in soup.find_all("div", attrs={"class": ["panel panel-default"]}):
                for i in i.find_all("h3", {"class": ["panel-title"]}):
                    for i in i.find_all("tbody"):
                        for i in i.find_all("tr"):
                            for i in i.find_all("td"):
                                for x in i.find_all("button", "btn btn-group-sm btn-info"):
                                    server_ids[
                                        str(x).split("Server ID:     &lt;/td&gt;&lt;td&gt; ")[1].rsplit("&")[0]] = {
                                        "id": str(x).split("Server ID:     &lt;/td&gt;&lt;td&gt; ")[1].rsplit("&")[0],
                                        "netmask": str(x).split("Netmask:&lt;/td&gt;&lt;td&gt; ")[1].rsplit("&")[0],
                                        "ip": str(x).split("IP Address:     &lt;/td&gt;&lt;td&gt; ")[1].rsplit("&")[0],
                                        "gateway": str(x).split("Gateway:&lt;/td&gt;&lt;td&gt; ")[1].rsplit("&")[0],
                                        "rootpass": str(x).split("Password:&lt;/td&gt;&lt;td&gt; ")[1].rsplit("&")[0],
                                        "mode": str(x).split("Run Mode:&lt;/td&gt;&lt;td&gt; ")[1].rsplit("&")[0]
                                    }
        return server_ids


pprint(api("enter your username in here with the quates in tact",
           "enter your password in here with the quates in tact").listservers())
