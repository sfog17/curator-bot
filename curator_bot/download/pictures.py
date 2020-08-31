""" Download all the paintings of a given artists from www.wikiart.org """
import html
import logging
import math
import random
import re
import shutil
import time
from typing import List, Tuple, Optional
from pathlib import Path
import requests

logger = logging.getLogger(__name__)

# Constants
NB_IMAGES_PAGE_1 = 20
NB_IMAGES_PAGE = 60
BASE_URL = 'https://www.wikiart.org/en'


class DownloadArtistException(Exception):
    pass


def find_artist_wikiname(artist_name: str) -> Tuple[str, str]:
    """ Look for an artist name and returns (url_artist_name, artist_wiki_name)"""
    potential_matches = []

    logger.info(f'Search matches for {artist_name}')
    first_letter = artist_name[0].lower()
    url = BASE_URL + f'/Alphabet/{first_letter}/text-list'
    req = requests.get(url)
    regex_artist = r'<a href="/en/(.*?)">(.*?)</a>'
    list_artists = re.findall(regex_artist, req.text)
    for artist in list_artists:
        if artist_name in artist[1]:
            potential_matches.append(artist)

    if not potential_matches:
        raise DownloadArtistException(f'{artist_name} - Found no match')
    elif len(potential_matches) > 1:
        raise DownloadArtistException(f'{artist_name} - Found multiple matches: {potential_matches}')
    elif len(potential_matches) == 1:
        logger.info(f'{artist_name} - Found 1 match: {potential_matches[0]}')

    url_artist_name = html.unescape(potential_matches[0][0])
    artist_wiki_name = html.unescape(potential_matches[0][1])

    return url_artist_name, artist_wiki_name


def extract_nb_paintngs(response_text: str):
    """ Regex to extract the number of paintings for an artist"""
    # Extract number of paintings, calculate number of pages to scrape
    logger.debug(re.findall(r'<title>(.*?)</title>', response_text))
    regex_title = r'<title>.* - (\d+?) .* - painting<\/title>'
    nb_paintings = int(re.search(regex_title, response_text).group(1))
    return nb_paintings


def find_paintings_page(url_artist_name: str) -> List[str]:
    """ Given a wikiart artist URL page, return URL for all its paintings """

    # Initialise
    paintings_url_pages = []

    # Create session and connect
    session = requests.Session()
    response = session.get(f'{BASE_URL}/{url_artist_name}/all-works/text-list')

    nb_paintings = extract_nb_paintngs(response.text)

    nb_pages = math.ceil(1 + ((nb_paintings - NB_IMAGES_PAGE_1) / NB_IMAGES_PAGE))
    logger.info(f'Found {nb_paintings} paintings')

    # For each page, extract the images url
    regex_path = r'https://uploads\d.wikiart.org/images/[\w\-/]+.jpg'

    for page_num in range(nb_pages):
        logger.debug(f'------- Page {page_num + 1} --------')

        url_request = f'{BASE_URL}/{url_artist_name}/mode/all-paintings'
        url_request += f'?json=2&layout=new&page={page_num + 1}&resultType=masonry'
        page_request = session.get(url_request)

        paths = re.findall(regex_path, page_request.text)
        for painting_path in paths:
            paintings_url_pages.append(painting_path)

        time.sleep(0.1)

    return paintings_url_pages


def download_images(
    list_url: List[str],
    out_dir_path: Path,
    artist: Optional[str] = None,
    limit: Optional[int] = None
):
    """ Download pictures from a list of URL """
    # Select N random images if limit is specified
    if limit:
        random.shuffle(list_url)
        urls = list_url[:100]
    else:
        urls = list_url
    logger.info(f'Downloading {len(urls)} paintings')

    for url_path in urls:
        # Extract Artist/Painting Name fron URL
        regex = r'https://uploads\d.wikiart.org/images/(.*?)/(.*?).jpg'
        regextract = re.search(regex, url_path)
        artist_name = artist if artist else regextract.group(1)
        painting = regextract.group(2)

        # Create directory (with artist name) if not exist
        dir_artist_path = out_dir_path / artist_name
        dir_artist_path.mkdir(exist_ok=True)

        # Download artist paintings (if not already present)
        out_path = dir_artist_path / (painting + '.jpg')
        if not out_path.exists():
            logger.info(f'Download {url_path} to {out_path}')
            response = requests.get(url_path, stream=True)
            with open(out_path, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            del response
            time.sleep(0.1)
        else:
            logger.info(f'File already exists - {out_path} ')


def download_artist_pictures(artist: str, parent_dir: Path, limit: int = 1000):
    """
    Download all pictures of an artist from WikiArt and create a subfolder
    with those pictures

    Args:
        artist: Artist name
        parent_dir: Parent folder where to create the subfolder
        limit: Max images to download
    """
    url_artist_name, artist_wiki_name = find_artist_wikiname(artist_name=artist)
    url_pages = find_paintings_page(url_artist_name=url_artist_name)
    logger.info(url_pages)
    download_images(url_pages, parent_dir, artist=artist_wiki_name, limit=limit)
