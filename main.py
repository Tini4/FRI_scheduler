import pickle
import re
from argparse import ArgumentParser, Namespace
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from requests import Session

CACHE_FILE: str = 'cache.pkl'
SCHEDULE_URL: str = 'https://urnik.fri.uni-lj.si'


def load_cache() -> dict[str, BeautifulSoup]:
    # noinspection PyBroadException
    try:
        with open(CACHE_FILE, 'rb') as f:
            return pickle.load(f)
    except Exception:
        return {}


def store_cache(cache: dict[str, BeautifulSoup]) -> None:
    with open(CACHE_FILE, 'wb') as f:
        pickle.dump(cache, f)


def get_url() -> str:
    # TODO: cache
    session = Session()
    page = session.get(SCHEDULE_URL)

    return page.url[:-1]


def get_query(subjects: list[str]) -> str:
    return '/allocations?' + '&'.join('subject=' + subj for subj in sorted(set(subjects)))


def get_soup_url(url: str, use_cache: bool = True) -> BeautifulSoup:
    cache = load_cache()
    url_print = f'{urlparse(url).netloc}{urlparse(url).path}'

    if use_cache and url in cache:
        print(f'cached: {url_print} ({url})\n')
    else:
        print(f'retrieving: {url_print} ({url})\n')

        session = Session()
        page = session.get(url)
        cache[url] = BeautifulSoup(page.content, 'html.parser')  # 'html5lib')

        store_cache(cache)

    return cache[url]


def get_soup_file(file: str) -> BeautifulSoup:
    with open(file, 'r', encoding='utf-8') as _f:
        return BeautifulSoup(_f.read(), 'html.parser')  # 'html5lib')


def parse_arguments() -> Namespace:
    parser = ArgumentParser(
        prog='FRI_scheduler',
        description='Create your schedule for UL FRI.',
        epilog='by Tini4'
    )
    parser.add_argument('subject', nargs='+',
                        help='Subject IDs (e.g. 63220 63216 63280 ...)')
    parser.add_argument('-u', '--url',
                        help='Schedule URL (e.g. https://urnik.fri.uni-lj.si/timetable/fri-2024_2025-letni)')
    parser.add_argument('-c', '--cache', action='store_false',
                        help='Disable caching')

    args = parser.parse_args()

    if args.url is None:
        args.url = get_url()

    return args


def main() -> None:
    args = parse_arguments()

    soup = get_soup_url(args.url + get_query(args.subject), args.cache)

    with open('original.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

    # Add main.js
    soup.head.append(soup.new_tag('script', src='static/main.js'))

    # Add style.css
    soup.head.append(soup.new_tag('link', href='static/style.css', rel='stylesheet'))

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

    # Remove header links
    soup.find('div', class_='header').find('div', class_='aside').decompose()

    # Rename subjects
    for a in soup.find_all('a', class_='link-subject'):
        a.string = re.match(r'(.*?)(?:\(.*\))?_.*', a.string).group(1)

    # Recolour
    for div in soup.find_all('div', class_='grid-entry'):
        div['style'] = re.sub(r'(hsla\(.+, .+%, ).+(%, .+\))', r'\g<1>35\g<2>', div['style'])

    with open('modified.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

    print(Path('modified.html').absolute().as_uri())


if __name__ == '__main__':
    main()
