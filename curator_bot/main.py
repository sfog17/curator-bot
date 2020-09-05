import logging
from pathlib import Path
from typing import List
from curator_bot.download.pictures import download_artist_pictures


def build_dataset(list_artists: List[str], parent_dir: Path, max_images: int = 100):
    for artist in list_artists:
        download_artist_pictures(artist=artist, parent_dir=parent_dir, limit=max_images)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename='curator-bot.log')
    logging.getLogger().addHandler(logging.StreamHandler())
    build_dataset(
        list_artists=[
            'El Greco', 'Velazquez', 'Murillo', 'Ribera', 'Zurbaran', 'Goya',
            'Sorolla', 'Picasso', 'Dali', 'Miro'
        ],
        parent_dir=Path(__file__).resolve().parent.parent / 'data' / 'raw'
    )
