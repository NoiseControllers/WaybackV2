from queue import Queue
from threading import Thread

import requests


class ProxyChecker(Thread):
    def __init__(self, queue_proxies: Queue, list_goods):
        self._queue = queue_proxies
        self.list_ = list_goods
        super().__init__()

    def run(self) -> None:
        while True:
            proxy = self._queue.get()

            if proxy is None:
                break

            self.check_proxy(proxy=proxy)
            self._queue.task_done()

    def check_proxy(self, proxy: str) -> None:
        proxy_url = f"http://{proxy}"

        try:
            r = requests.get(
                "http://web.archive.org/",
                proxies={"http": proxy_url, "https": proxy_url},
                timeout=5,
            )
            if r.status_code == 200:
                self.list_.append(proxy)
        except Exception:
            pass
