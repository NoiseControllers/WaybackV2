import random

from src.Controllers.ServerResponse.ServerResponse import ServerResponse
from src.Utils.LoadFiles.LoadFiles import load_file


class ProxyRepository:
    def __init__(self):
        self.__session = ServerResponse(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        )
        self._proxies = []
        self._use_proxies = False

    def automatic_proxies_load(self) -> None:
        url = "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=3000&country=all&ssl=all&anonymity=all"

        resp = self.__session.get(url)

        for line in resp.iter_lines(decode_unicode=True):
            self._proxies.append(line)

    def manually_proxies_load(self, path: str) -> None:
        self._proxies = load_file(file_path=path)

    def random_proxy(self) -> str:
        return random.choice(self._proxies)

    def remove_proxy(self, proxy) -> None:
        try:
            self._proxies.remove(proxy)
        except (UnboundLocalError, ValueError):
            pass

    def update_proxies(self, new_proxies: list) -> None:
        self._proxies.clear()
        self._proxies = new_proxies

    @property
    def proxies(self) -> list:
        return self._proxies

    @property
    def use_proxies(self) -> bool:
        return self._use_proxies

    def set_use_proxies(self, value: bool) -> None:
        self._use_proxies = value
