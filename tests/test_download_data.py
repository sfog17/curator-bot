""" Tests """
import pytest
from curator_bot.download.pictures import find_artist_wikiname, DownloadArtistException, extract_nb_paintngs


def test_find_artist():
    artist = find_artist_wikiname('Sorolla')
    assert artist == ('joaqu-n-sorolla', 'Joaquín Sorolla')


def test_find_artist_mistake():
    with pytest.raises(DownloadArtistException) as excinfo:
        artist = find_artist_wikiname('Bosche')
        print(artist)

    assert str(excinfo.value) == 'Bosche - Found no match'


def test_extract_nb_paintings():
    response = '<title>Andrea Mantegna - 145 artworks - painting</title>'
    assert extract_nb_paintngs(response) == 145
