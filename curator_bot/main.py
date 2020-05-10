import logging
from pathlib import Path
from curator_bot.download.pictures import download_artist_pictures

DATA_DIR = Path(__file__).parent.parent / 'data' / 'raw'


def build_dataset():
    download_artist_pictures(artist='Zurbaran', parent_dir=DATA_DIR)
    download_artist_pictures(artist='Sorolla', parent_dir=DATA_DIR)
    download_artist_pictures(artist='Bermejo', parent_dir=DATA_DIR)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename='curator-bot.log')
    logging.getLogger().addHandler(logging.StreamHandler())
    build_dataset()
