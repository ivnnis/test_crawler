import urllib.parse
from urllib.parse import urljoin
from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import warnings
import threading

warnings.filterwarnings('ignore')


# Собирает все ссылки с одной страницы
def get_one_page_links(url: str) -> list[str]:
    try:
        response = requests.get(url, verify=False)
        soup = BeautifulSoup(response.content, "html.parser")
    except Exception as error:
        print(error)
        return 0
    links = []
    for element in soup.find_all(name=['a', 'link']):
        link = element.get("href")
        if link:
            links.append(link)
    return links



def worker(url: str) -> list[str]:

# Рекурсивно ищет ссылки
    def find_all_links(urls: list[str]) -> None:
        nonlocal base_url
        nonlocal all_urls
        if urls:
            for url in urls:
                if not url.startswith("http"):          # Проверяем является ли ссылка локальной
                    url = urljoin(base_url, url)
                elif base_url.split('/')[2] not in url: # Проверяем ведет ли ссылка на другой ресурс
                    continue
                if url not in all_urls:
                    res = get_one_page_links(url)
                    if res:
                        all_urls.append(url)
                        find_all_links(res)
    
    base_url = url
    all_urls = []
    find_all_links(url)

    return all_urls


sites = [["http://crawler-test.com/",   "crawler-test"],
         ["http://google.com/",         "google"],
         ["https://vk.com/",            "vk"],
         ["https://dzen.ru/",           "dzen"],
         ["https://stackoverflow.com/", "stackoverflow"]]

threads = []
for site in sites:
    t = threading.Thread(target=worker, args=(site[0],), name = site[1])
    threads.append(t)
    t.start()

for t in threads:
    with open(f'{t.name}.txt', 'w') as f:
        for line in t.join():
            f.write(line)