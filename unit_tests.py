"""
Test some of the lyrics scraping and Markov functions.
"""
import pytest
from lyrics_scraping import *
from first_order_markov import *
from second_order_markov import *

def test_get_soup():
    """
    Tests that a request can be made to this website, and HTML data can be
    parsed from it.
    """
    url = "https://www.cs.ubc.ca/~davet/music/list/Best9.html"
    soup = get_soup(url)
    title = "<title>Rolling Stone - 500 Greatest Songs (Music Database :: Dave Tompkins)</title>"
    assert str(soup.title) == title


def test_clean_song_data():
    """
    Tests that the data cleaning process works and returns a certain cell
    from the resulting dataframe.
    """
    file_name = "song_data.csv"
    song_data = clean_song_data(file_name)
    first_cell = song_data.at[2, 'artist']
    assert first_cell == "bobdylan"


def test_get_url():
    """
    Tests that the url generation function returns what is expected.
    """
    file_name = "song_data.csv"
    url_list = get_url(file_name)
    first_url = url_list[0]
    test_url = "https://www.azlyrics.com/lyrics/bobdylan/likearollingstone.html"
    assert first_url == test_url


def test_get_lyrics():
    """
    Checks that a url makes a successful request and returns just the text.
    """
    url = "https://www.azlyrics.com/lyrics/queen/underpressure.html"
    lyrics = get_lyrics(url)
    assert lyrics[3:11] == "Pressure"


def test_build_word_list():
    """
    Testing the build_word_list function.
    """
    sample_text = "testing split function"
    sample_list = ["testing", "split", "function"]
    assert first_order_markov.build_word_list(sample_text) == sample_list
