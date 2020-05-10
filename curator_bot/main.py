import logging
from pathlib import Path
from typing import List
from curator_bot.download.pictures import download_artist_pictures

DATA_DIR = Path(__file__).parent.parent / 'data' / 'raw'


def build_dataset(list_artists: List[str]):
    for artist in list_artists:
        download_artist_pictures(artist=artist, parent_dir=DATA_DIR, limit=60)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename='curator-bot.log')
    logging.getLogger().addHandler(logging.StreamHandler())
    build_dataset([
        'Bermejo',
        'Zurbaran', 'Velazquez',
        'Goya', 'Sorolla',
        'Picasso', 'Dali', 'Miro'
    ])
