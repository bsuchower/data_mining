"""
Obtains a list of song titles and artist names, generates corresponding
urls for AZ Lyrics, and scrapes each lyrics page and stores each set of
lyrics as a text file.
"""
import requests
import string
import pandas as pd
from bs4 import BeautifulSoup


def get_soup(url):
    """
    Requests text data from a website and returns the parsed HTML data
    using the Beautiful Soup library.

    This function first makes a request to a website from the url, and then
    gets only the text from that page as the variable raw_text. It then
    uses the Beautiful Soup library to get the HTML text data from the
    website, and returns it.

    Args:
        url: A string containing the url of the website you are trying
        to get text data from.

    Returns:
        The parsed HTML text data.
    """
    r = requests.get(url)
    raw_text = r.text
    soup = BeautifulSoup(raw_text, features="lxml")
    return soup


def get_song_list(url):
    """
    Creates a file of song names and artists.

    This function first calls the get_soup function to get the HTML data
    from the website at the specified url. Since the website that is being
    scraped for song names has them within a table, each row of the table
    is looped through and data is collected from the relevant columns
    (song names and artists). Each row's results are added to an empty
    list called data, and Pandas is used to add each row to a dataframe
    and write this data to a csv file.

    Args:
        url: A string containing the url to a website that contains
        a list of songs.

    Returns:
        A csv file containing artist and song names.
    """
    # gets parsed HTML data from the website
    soup = get_soup(url)

    # find the table element
    data = []
    table = soup.find('table', attrs={"class": "music"})
    table_body = table.find("tbody")

    # add items from each row to data
    rows = table_body.find_all("tr")
    for row in rows:
        cols = row.find_all("td")
        cols = [item.text.strip() for item in cols]
        cols = cols[2:4]
        data.append([item for item in cols if item])

    # saves data as a csv file
    df = pd.DataFrame(data)
    df.to_csv('song_data.csv')


def clean_song_data(file_name):
    """
    Cleans the song data so it is in a format to be put into the
    website url.

    This function removes all punctuation and spaces from each entry in
    song_data, and also makes every character lowercase.

    Args:
        file_name: A string containing the name of the file containing
        song names and corresponding artists.

    Returns:
        A dataframe containing cleaned data for song titles and artists.
    """
    # import a string of all ASCII punctuation
    punctuation = string.punctuation

    # read csv file and reshape to just relevant columns and rows
    song_data = pd.read_csv("song_data.csv", names=["a", "artist", "title"])
    song_data = song_data.drop(columns="a", index=[0, 1])

    # removes punctuation, spaces, and makes uppercase characters lowercase
    i = 2  # index starts at 2 since some rows were deleted
    for artist in song_data.artist:
        for character in artist:
            if character in punctuation:
                artist = artist.replace(character, "")
            if character == " ":
                artist = artist.replace(character, "")
            if character.isupper() is True:
                artist = artist.lower()
        song_data.artist[i] = artist
        i += 1

    i = 2
    for title in song_data.title:
        for character in title:
            if character in punctuation:
                title = title.replace(character, "")
            if character == " ":
                title = title.replace(character, "")
            if character.isupper() is True:
                title = title.lower()
        song_data.title[i] = title
        i += 1

    return song_data


def get_url(file_name):
    """
    Formats the cleaned song titles and artists into urls to scrape
    lyrics from.

    This function first calls the function clean_song_data to get the
    cleaned data of song titles and artist names. For each row in this
    dataframe, the song title and artist name are formatted into a url
    specifically for AZlyrics. These urls are added to a list, which
    is returned at the end of the function.

    Args:
        file_name: A string containing the name of the file containing
        song names and corresponding artists.

    Returns:
        A list containing formatted urls for all the songs, containing
        song names and artist names.
    """
    # get cleaned song data
    song_data = clean_song_data(file_name)

    url_list = []
    i = 2  # index starts at 2 since some rows were deleted
    for row in song_data.index:
        artist = song_data.artist[i]
        title = song_data.title[i]
        url = f"https://www.azlyrics.com/lyrics/{artist}/{title}.html"
        url_list.append(url)
        i += 1

    return url_list


def get_lyrics(url):
    """
    Scrapes all the text off of a lyrics website and finds only the
    text of the lyrics.

    This function first gets the parsed HTML data from the website at the
    specified url. It then finds the body section that has the lyrics text,
    which should be as a specified class name. If the url does not lead to
    a page with lyrics, the function returns an empty string. If the url leads
    to a page with lyrics, all the div classes are searched through and added
    to a list. The div section that contains the lyrics is converted into
    text format and returned.

    Args:
        url: A string containing the url of the lyrics website.

    Returns:
        A string containing the lyrics.
    """
    # gets parsed HTML data from the website
    soup = get_soup(url)

    # find the body section that has the lyrics text
    body_section = soup.find_all("div", {"class": "col-xs-12 col-lg-8 text-center"})

    # if the url does not lead to a lyrics page, return an empty string
    if body_section == []:
        return ""

    body = body_section[0]
    # search through all div classes and add to a list
    divs = []
    for container in body.contents:
        if container.name == "div":
            divs.append(container)

    # return the div section that contains the lyrics
    lyrics = divs[4].text
    return lyrics


def create_lyrics_files(file_name, start_range, end_range):
    """
    Creates a folder of files containing scraped lyrics.

    This function first calls the function url_list to get a list of all the
    urls that will be scraped from. For each url in the list (a section of
    which is defined by the index), the lyrics are scraped from the url.
    If the get_lyrics returns an empty string, no file is created for that
    url. Otherwise, a text file is created within the "data" folder, and each
    file name is a number (incremented each time through the loop).

    Args:
        file_name: A string containing the name of the file containing
        song names and corresponding artists.

        start_range: An integer containing the beginning of the range to
        scrape for.

        end_range: An integer containing the end of the range to
        scrape for.

    Returns:
        Writes to a file in the data folder.
    """
    # gets the url list
    url_list = get_url(file_name)

    i = 1  # filenames start at 1
    for url in url_list[start_range:end_range]:
        lyrics_file = get_lyrics(url)
        if lyrics_file != "":
            with open(f"data/{i}.txt", "w") as f:
                f.write(lyrics_file)
        i += 1
