import pickle
import re
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

MEM: dict[str, BeautifulSoup]
USE_MEM: bool = True

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

    # Add main.js
    soup.head.append(soup.new_tag('script', src='/static/js/main.js'))

    # Disable links
    for a in soup.find_all('a'):
        a.attrs.pop('href')

    # Remove popups
    for div in soup.find_all('div', class_='entry-hover'):
        div.decompose()

    # Remove group list
    soup.find('div', class_='group-list').decompose()

    # Remove groups
    for div in soup.find_all('div', class_='bottom-aligned'):
        div.decompose()

    # Rename subjects
    for a in soup.find_all('a', class_='link-subject'):
        a.string = re.match(r'(.*?)(?:\(.*\))?_.*', a.string).group(1)

    # Recolour
    for div in soup.find_all('div', class_='grid-entry'):
        div['style'] = re.sub(r'(hsla\(.+, .+%, ).+(%, .+\))', r'\g<1>35\g<2>', div['style'])

    with open('modified.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())


if __name__ == '__main__':
    load_mem()

    query: str = '/allocations?' + '&'.join('subject=' + subj for subj in sorted(SUBJECTS))
    soup_ = get_soup_url(URL + query, USE_MEM)

    store_mem()

    run(soup_)
