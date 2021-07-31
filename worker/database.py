import logging
from multiprocessing import cpu_count, Pool, Manager
import pickle
from sys import argv, exit
from typing import Dict, Any

import jellyfish

logger = logging.getLogger(__name__)
homophone_index: Dict[str, Any]


def get_words(dictionary_file_path: str) -> [str]:
    """Get the list of words from a dictionary file."""
    with open(dictionary_file_path, "r") as file:
        return [word.strip().lower() for word in file]


def generate_for_word(word: str, words: [str], results: Dict[str, list]):
    """Adapted from https://github.com/cameronehrlich/homz"""
    matching_words = []

    for j, w2 in enumerate(words):
        if w2 == word:
            continue

        if jellyfish.match_rating_comparison(word, w2):
            jaro_winkler_score = jellyfish.jaro_winkler(word, w2)
            if jaro_winkler_score > 0.0:
                word_score = (w2, jaro_winkler_score)
                matching_words.append(word_score)

        if j == len(words) - 1:
            results[word] = sorted(matching_words,
                                   key=lambda tup: tup[1],
                                   reverse=True)


def generate(words: [str]):
    """Find homophones of each word and generate a database."""
    global homophone_index
    homophone_index = dict()

    # I PAID for the whole CPU so I'm going to USE the whole CPU
    # (don't try this at home)
    n_processes = cpu_count() * 2

    logger.info(f"Using {n_processes} process{'' if n_processes == 1 else 'es'}")

    with Pool(n_processes) as pool, Manager() as manager:
        results = manager.dict()

        for word in words:
            pool.apply_async(func=generate_for_word, args=(word, words, results))

        pool.close()
        pool.join()
        homophone_index[word] = dict(results)


def save():
    """Save the generated homophone database to disk."""
    with open("homophones.pk", "wb") as file:
        pickle.dump(homophone_index, file, pickle.HIGHEST_PROTOCOL)


def load():
    """Load a homophone database from disk."""
    global homophone_index

    try:
        with open("homophones.pk", "rb") as file:
            homophone_index = pickle.load(file)
    except FileNotFoundError:
        logger.error(
            "Homophone database does not exist. "
            "Run python -m worker.database to generate it."
        )
        exit(2)


def lookup(word: str, n=10) -> [str]:
    """
    Look up the homophones of a given word.

    :param word: the word to look up
    :param n: the maximum number of homophones to return
    """
    if "homophone_index" not in globals():
        load()

    homophones = homophone_index[word.strip().lower()]

    if len(homophones) > n:
        homophones = homophones[0:n]

    return homophones


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    if len(argv) != 2:
        logger.error(f"Usage: {argv[0]} <dictionary file path>")
        exit(1)

    logger.info(f"Reading {argv[1]}")
    words_ = get_words(argv[1])

    logger.info("Generating homophone index")
    generate(words_)

    logger.info(f"Saving dictionary with {len(homophone_index)} entries")
    save()
