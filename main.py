import pickle
from urllib.parse import urlparse, parse_qs

import requests
from bs4 import BeautifulSoup

MEM: dict[str, BeautifulSoup] = {}
CLASSES: tuple[str, ...] = ('63279', '63218', '63283', '63208', '63213', '63738')


def get_soup_url(url: str, mem: bool = True) -> BeautifulSoup:
    if not mem or url not in MEM:
        print(f'retrieving: {urlparse(url).netloc} ({url})\n')

        session = requests.Session()
        page = session.get(url)
        MEM[url] = BeautifulSoup(page.content, 'html.parser')
    else:
        print(f'cached: {urlparse(url).netloc} ({url})\n')

    return MEM[url]


def get_soup_file(file: str) -> BeautifulSoup:
    with open(file, 'r', encoding='utf-8') as _f:
        return BeautifulSoup(_f.read(), 'html5lib')  # 'html.parser')


if __name__ == '__main__':
    with open('mem', 'rb') as f:
        MEM = pickle.load(f)

    soup = get_soup_url(
        # 'https://urnik.fri.uni-lj.si/timetable/fri-2024_2025-zimski/allocations?subject=63283&type=LV&type=AV&type=LAB'
        # 'https://urnik.fri.uni-lj.si/timetable/fri-2024_2025-zimski/allocations?type=P&group=55603'
        'https://urnik.fri.uni-lj.si/timetable/fri-2024_2025-zimski/allocations?group=55603'
    )

    with open('mem', 'wb') as f:
        pickle.dump(MEM, f)

    # soup = get_soup_file('Urnik.htm')

    with open('original.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

    for div in soup.find_all('div', class_='bottom-aligned'):
        div.decompose()

    for div in soup.find_all('div', class_='grid-entry'):
        a = div.find('a', class_='link-subject')
        if parse_qs(urlparse(a['href']).query)['subject'][0] not in CLASSES:
            div.decompose()

    for a in soup.find_all('a', class_='link-subject'):
        a.string = a.string.split('_')[0].split('(')[0]

    div = soup.find('div', class_='group-list')
    div.decompose()

    with open('modified.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

# from selenium import webdriver
#
# browser = webdriver.Firefox()
# browser.get(
#     'https://urnik.fri.uni-lj.si/timetable/fri-2024_2025-zimski/allocations?subject=63283&type=LV&type=AV&type=LAB')
#
# print(browser.page_source)
