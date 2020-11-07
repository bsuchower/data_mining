"""
Use a first-order Markov process to generate random sentences based on
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


def build_next_words_1(word_list):
    """
    Builds a dictionary of "next words" from a source text.

    Loops through each word in the provided sample text and identifies the
    next word and the end character. If the word does not already exist as
    a key in the dictionary, it is added and the next word is added as the
    map. If the key already exists, the current next word is added to the
    map for that word. If the word ends with punctuation, it maps to an
    empty string.

    Args:
        word_list: A list of words where each word is a string.

    Returns:
        A dictionary where each key maps to a list of "next words".
    """
    final_dictionary = {}  # create empty dictionary
    i = 0  # initialize index outside of loop
    last_word = word_list[len(word_list) - 1]  # find the last word in the list

    for item in word_list:
        # prevents out of range error at end of loop
        if i >= len(word_list) - 1:
            break

        next_word = word_list[i + 1]
        end_character = item[len(item) - 1]

        if item in final_dictionary:
            if end_character == "." or end_character == "!" or end_character == "?":
                final_dictionary[item] = [""]
                final_dictionary[""].append(next_word)
            else:
                final_dictionary[item].append(next_word)
        else:
            if i == 0:
                final_dictionary[""] = [word_list[i]]
                final_dictionary[item] = [next_word]
            elif end_character == "." or end_character == "!" or end_character == "?":
                final_dictionary[item] = [""]
                final_dictionary[""].append(next_word)
            else:
                final_dictionary[item] = [next_word]

        i += 1  # increment index last

    final_dictionary[last_word] = [""]  # adds last word to dictionary
    return(final_dictionary)


def generate_sentence(next_words):
    """
    Generates a sentence based on a dictionary of "next words".

    Randomly assigns one of the words that start sentences as the first word
    in the sentence. Chooses a random word for each new word in the sentence
    based on the dictionary, until a word with ending punctuation is reached,
    ending the sentence.

    Args:
        next_words: A dictionary where each key maps to a list of "next words".

    Returns:
        One randomly generated sentence (as a string).
    """
    first_word = random.choice(next_words[""])
    end_character = first_word[len(first_word) - 1]
    last_word = first_word
    final_sentence = first_word

    while end_character != "." or end_character != "!" or end_character != "?":
        # prevents out of range index error
        if end_character == "." or end_character == "!" or end_character == "?":
            break
        last_word = random.choice(next_words[last_word])
        end_character = last_word[len(last_word) - 1]
        # breaks the line before each word that starts with uppercase letter
        if last_word[0].isupper():
            final_sentence += '\n'
        final_sentence += " " + last_word

    return final_sentence


def generate_text(next_words, num_sentences):
    """
    Generates multiple random sentences as a larger block of text.

    Randomly forms any number of sentences using the generate_sentence function,
    for the number passed by num_sentences.

    Args:
        next_words: A dictionary where each key maps to a list of "next words".
        num_sentences: The number of sentences to generate (int type).

    Returns:
        A randomly generated text (as a string).
    """
    for i in range(num_sentences):
        line = generate_sentence(next_words) + "\n"
        print(line)
