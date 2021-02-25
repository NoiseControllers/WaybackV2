import argparse
from multiprocessing import Manager
from queue import Queue

from src.Controllers.ProxiesChecker.ProxyChecker import ProxyChecker
from src.Domain.Repositories.ProxyRepository.ProxyRepository import ProxyRepository
from src.Infraestructure.Services.WkHtmlToImage.WkHtmlToImageService import WkHtmlToImageService
from src.Utils.LoadFiles.LoadFiles import load_file
from src.Utils.ManagementDirectories.ManagementDirectory import ManagementDirectory
from src.Utils.ManagementDirectories.MyDividerBar import my_divider_bar


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', help='Fichero txt', dest='file', type=str, required=True)
    parser.add_argument('-t', help='Numero de hilos', dest='threads', type=int)
    parser.add_argument('-p', help='Fichero de proxies', dest='proxies_file', type=str)
    parser.add_argument('-y', help='', dest='per_year', type=int)

    args = parser.parse_args()
    file = args.file
    thread_count = args.threads or 1
    proxies_file = args.proxies_file or None
    per_year = args.per_year or 1

    queue = Queue()
    threads = []

    bar = my_divider_bar()
    proxies_repository = ProxyRepository()

    print("[~] Loading proxies in memory.")
    if proxies_file is None:
        proxies_repository.automatic_proxies_load()
    else:
        proxies_repository.manually_proxies_load(path=proxies_file)

    print(f"[!] Total proxies loaded: {len(proxies_repository.proxies)}")
    print("[~] Checking proxies.")
    proxies_repository.set_use_proxies(True)

    with Manager() as manager:
        goods = manager.list()
        processes = []
        queue_proxies = Queue()

        for thread in range(200):
            p = ProxyChecker(queue_proxies=queue_proxies, list_goods=goods)
            p.start()
            processes.append(p)

        for proxy in proxies_repository.proxies:
            queue_proxies.put(proxy)

        queue_proxies.join()

        for t in range(200):
            queue_proxies.put(None)

        for process in processes:
            process.join()

        goods = list(goods)

    proxies_repository.update_proxies(goods)
    print("[~] Finish checking proxies.")
    print(f"[!] Valid proxies: {len(proxies_repository.proxies)}")

    management_directory = ManagementDirectory(bar=bar)

    print("[~] Initialize the threads.")

    # Initialize the threads
    for t in range(thread_count):
        thread = WkHtmlToImageService(
            queue=queue,
            management_directory=management_directory,
            proxies_repository=proxies_repository,
            filter_domain_per_year=per_year
        )
        thread.start()
        threads.append(thread)

    print("[~] Loading file and inserting in queue.")
    domains = load_file(file_path=file)

    for domain in domains:
        queue.put(domain)

    queue.join()

    for t in range(thread_count):
        queue.put(None)

    for t in threads:
        t.join()

    print("DONE!")


if __name__ == '__main__':
    main()
