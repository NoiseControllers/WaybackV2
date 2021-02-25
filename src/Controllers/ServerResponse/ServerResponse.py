import time
from random import randint

import requests
from bs4 import BeautifulSoup


class ServerResponse:
    def __init__(self, user_agent: str):
        self._user_agent = user_agent

    def get(self, url: str, **kwargs):
        headers = {
            "User-Agent": self._user_agent
        }
        while True:
            try:
                resp = requests.get(url, headers=headers, stream=True, **kwargs)
            except Exception:
                time.sleep(randint(1, 3))
                continue

            if resp.status_code != 200:
                print(f"[~] HTTP status code {resp.status_code} {url}")
                if int(resp.status_code / 100) == 5:
                    print(f"[!] Waiting 3 seconds before retrying.")
                    time.sleep(3)

                if resp.status_code != 404:
                    continue

            return resp

    @staticmethod
    def resolve_redirect(url: str):
        print(url)
        bad_status_code = [404, 403]
        while True:
            try:
                resp = requests.get(url, allow_redirects=True, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"})
            except Exception as e:
                print(e)
                continue

            if resp.status_code in bad_status_code:
                return None

            bs4 = BeautifulSoup(resp.content, "lxml")
            try:
                redirect_to = bs4.find("p", class_="impatient").find("a")["href"]
            except AttributeError as e:
                print(e)
                redirect_to = resp.url
            # return resp.url
            return redirect_to
