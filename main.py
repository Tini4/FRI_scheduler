import pickle
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

MEM: dict[str, BeautifulSoup]
SUBJECTS: set[str] = {'63220', '63216', '63280', '63217'}
URL: str = 'https://urnik.fri.uni-lj.si/timetable/fri-2024_2025-letni'


def load_mem():
    global MEM

    # noinspection PyBroadException
    try:
        with open('MEM.pickle', 'rb') as f:
            MEM = pickle.load(f)
    except Exception:
        MEM = {}


def store_mem():
    with open('MEM.pickle', 'wb') as f:
        pickle.dump(MEM, f)


def get_soup_url(url: str, mem: bool = True) -> BeautifulSoup:
    if not mem or url not in MEM:
        print(f'retrieving: {urlparse(url).path} ({url})\n')

        session = requests.Session()
        page = session.get(url)
        MEM[url] = BeautifulSoup(page.content, 'html.parser')  # 'html5lib')
    else:
        print(f'cached: {urlparse(url).path} ({url})\n')

    return MEM[url]


def get_soup_file(file: str) -> BeautifulSoup:
    with open(file, 'r', encoding='utf-8') as _f:
        return BeautifulSoup(_f.read(), 'html.parser')  # 'html5lib')


def run(soup: BeautifulSoup) -> None:
    with open('original.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

    for div in soup.find_all('div', class_='bottom-aligned'):
        div.decompose()

    # from urllib.parse import urlparse, parse_qs
    # for div in soup.find_all('div', class_='grid-entry'):
    #     a = div.find('a', class_='link-subject')
    #     if parse_qs(urlparse(a['href']).query)['subject'][0] not in SUBJECTS:
    #         div.decompose()

    for a in soup.find_all('a', class_='link-subject'):
        a.string = a.string.split('_')[0].split('(')[0]

    div = soup.find('div', class_='group-list')
    div.decompose()

    with open('modified.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())


if __name__ == '__main__':
    load_mem()

    query: str = '/allocations?' + '&'.join('subject=' + subj for subj in sorted(SUBJECTS))
    soup_ = get_soup_url(URL + query, True)

    store_mem()

    run(soup_)
