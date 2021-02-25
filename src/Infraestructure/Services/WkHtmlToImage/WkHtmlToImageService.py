import random
from queue import Queue
from threading import Thread

import imgkit

from src.Controllers.ServerResponse.ServerResponse import ServerResponse
from src.Controllers.WayBackMachine.WayBackMachine import WayBackMachine
from src.Domain.Repositories.ProxyRepository.ProxyRepository import ProxyRepository
from src.Utils.Filters.FiltersPerYear.FilterPerYear import filter_per_year
from src.Utils.ManagementDirectories.ManagementDirectory import ManagementDirectory


class WkHtmlToImageService(Thread):
    def __init__(
            self,
            queue: Queue,
            management_directory: ManagementDirectory,
            proxies_repository: ProxyRepository,
            filter_domain_per_year: int,
    ):
        self.__queue = queue
        self.__management_directory = management_directory
        self._proxies_repository = proxies_repository
        self._filter_domain_per_year = filter_domain_per_year
        self.__way_back_machine = WayBackMachine()
        self._base_url = "http://web.archive.org/web/{}/{}"
        self.__session = ServerResponse(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36")
        super().__init__()

    def run(self) -> None:
        while True:
            domain = self.__queue.get()

            if domain is None:
                break
            self.wk_html_to_image(domain=domain)
            self.__queue.task_done()

    def wk_html_to_image(self, domain: str) -> None:
        domain = domain.strip()
        path_to_download = self.__management_directory.create_the_folder_if_it_does_not_exist(name_folder=domain)

        options = {
            'proxy': '',
            'javascript-delay': '2000',
            'width': '1920',
            'height': '1080',
            # 'quiet': ''
        }

        snapshots = self.__way_back_machine.search_snapshots(url=domain)
        print(f"[+] {domain}")

        snapshots_filters = filter_per_year(snapshots=snapshots, per_year=self._filter_domain_per_year)

        for timestamp in snapshots_filters:
            url = self._base_url
            time_stamp, status_code = timestamp
            try:
                url = url.format(time_stamp, domain)
            except AttributeError:
                continue

            if status_code == "301" or status_code == "302" or status_code == "303":
                # TODO - Resolver redireccion
                url = self.__session.resolve_redirect(url)
                if url is None:
                    continue

            output_image = path_to_download + time_stamp + ".jpg"
            if self._proxies_repository.use_proxies:
                options['proxy'] = self._proxies_repository.random_proxy()
            else:
                options.pop('proxy', None)

            try:
                imgkit.from_url(url, output_image.strip(), options=options)
            except OSError:
                continue

        print(f"[✓] {domain}")
