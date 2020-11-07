"""
Uses a second-order Markov process to generate random sentences based on
a source text.
"""
import random
import os


def combine_files(file_folder):
    """
    Combines lyrics text for all lyrics text files.

    This function first gets a list of all files within the specified
    directory. It then loops through each file in the directory, and
    reads the file, and adds it to a string that contains the combined
    lyrics text.

    Args:
        file_folder: A string containing the name of the folder that holds
        all the lyrics files.

    Returns:
        The combined text of all the lyrics, as a string.
    """
    # get list of files in the specified directory
    dirs = os.listdir(file_folder)

    # initialize empty string
    combined_text = ""

    for file in dirs:
        file_path = f"{file_folder}/{file}"
        is_file = os.path.isfile(file_path)
        if is_file is True:
            with open(file_path, "r") as f:
                source_text = f.read()
                combined_text = combined_text + source_text

    return combined_text


def build_word_list(source_text):
    """
    Splits a sample text into individual words.

    Takes in a string of sample text, and separates it into individual words by
    using the split function, which splits the string along whitespace and
    new lines.

    Args:
        source_text: A string of sample text.

    Returns:
        A list of strings which contain separate words.
    """
    return source_text.split()


def build_next_words_2(word_list):
    """
    Builds a dictionary of "next words" from a source text.

    Loops through each word in the provided sample text and identifies the
    next two words. If the word does not already exist as one of the two
    keys in the dictionary, it is added and the next word is added as the
    map. If the key already exists, the current next word is added to the
    map for that word. If the word ends with punctuation, it maps to an
    empty string.

    Args:
        word_list: A list of words where each word is a string.

    Returns:
        A dictionary where the keys map to a list of "next words".
    """
    next_words = {"": []}
    word_list_length = len(word_list)
    current_word = None

    for i, key1 in enumerate(word_list):
        if current_word is None:
            next_words[""].append(key1)
        else:
            if word_list_length > i + 2:
                key2 = word_list[i + 1]
                word = word_list[i + 2]
                if (key1, key2) not in next_words:
                    next_words[(key1, key2)] = [word]
                else:
                    next_words[(key1, key2)].append(word)
        # checks if end character has punctuation
        if key1[-1] in ".!?":
            next_words[(key1, key2)] = [""]
            current_word = None
        else:
            current_word = key1

    return next_words


def generate_lyrics(next_words, word_list):
    """
    Generates lyrics from a dictionary of "next_words".

    This function chooses random integers within the range of the length
    of word_list to find the keys, and initializes the sentence as the
    words associated with these keys. Until the sentence reaches an ending
    punctuation, a random word is chosen from the dictionary for the current
    key. The line will break before a word that begins with an uppercase
    letter. The sentence is added to and the key is updated. The final
    sentence is then returned.

    Args:
        next_words: A dictionary where each key maps to a list of "next words".
        word_list: A list of words where each word is a string.

    Returns:
        Prints a randomly generated sentence.
    """
    r = random.randint(0, len(word_list) - 1)
    key = (word_list[r], word_list[r + 1])
    sentence = key[0] + ' ' + key[1]

    while next_words[key] != [""]:
        word = random.choice(next_words[key])
        if word[0].isupper():
            sentence += '\n'
        sentence += ' ' + word
        key = (key[1], word)
    print(sentence)
