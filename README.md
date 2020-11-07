# Generating Song Lyrics  

## Introduction  
This project generates new song lyrics using a language-based Markov chain,
based on the lyrics of existing songs. I obtained a list of song titles and
artist names from [Rolling Stone's "500 Greatest Songs of All Time"](https://www.rollingstone.com/music/music-lists/500-greatest-songs-of-all-time-151127/) list, published
in 2003. I then obtained the song lyrics for each song by scraping each
relevant page from [AZ Lyrics](https://www.azlyrics.com/). Finally, I generated new song
lyrics using both a first and second order Markov chain in order to compare
them.  

The `lyrics_scraping.py` file contains functions that obtain a list of song
titles and artist names, generates corresponding urls for AZ Lyrics, and
scrapes each lyrics page and stores each set of lyrics as a text file within
the `data` folder. The `first_order_markov.py` and `second_order_markov.py`
files both generate lyrics based on the text of the sample lyrics obtained.  

The `computational_essay.ipynb` file contains relevant blocks of code to run
in order to see the generated lyrics.  

## Libraries  
This program uses the following Python libraries:  
- `requests`  
- `string`
- `pandas`  
- `Beautiful Soup`  
- `random`  
- `os`  
Each library is imported within the code, so there is nothing to install.