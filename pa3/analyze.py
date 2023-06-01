'''
Analyzing Election Tweets

Jerry Shi

Use the algorithms in the previous part on the dataset of
tweets. Every collection of tweets is represented as a JSON
file. Functions to implement:
  find_top_k_entities,
  find_min_count_entities,
  find_top_k_ngrams,
  find_min_count_ngrams,
  find_most_salient_ngrams
'''

import unicodedata
import sys

from basic_algorithms import find_top_k, find_min_count, find_most_salient

##################### DO NOT MODIFY THIS CODE #####################

def keep_chr(ch):
    '''
    Find all characters that are classifed as punctuation in Unicode
    (except #, @, &) and combine them into a single string.
    '''

    return unicodedata.category(ch).startswith('P') and \
        ch not in ("#", "@", "&")

PUNCTUATION = " ".join([chr(i) for i in range(sys.maxunicode)
                        if keep_chr(chr(i))])

# When processing tweets, ignore these words
STOP_WORDS = ["a", "an", "the", "this", "that", "of", "for", "or",
              "and", "on", "to", "be", "if", "we", "you", "in", "is",
              "at", "it", "rt", "mt", "with"]

# When processing tweets, words w/ a prefix that appears in this list
# should be ignored.
STOP_PREFIXES = ("@", "#", "http", "&amp")


#####################  MODIFY THIS CODE #####################

def load_tweets(tweets, entity_key):
    '''
    Takes a bunch of messy tweets and returns a nice list of
    tokens present in tokens

    Inputs:
        tweets: a list of dictionaries
        entity_key: a pair of hash ("hashtags", "text"),
          ("user_mentions", "screen_name"), etc

    Returns:
        tokens: a list of all the strings that appear in
        tweets within the specified entity_key pair
        (i.e. all hashtag text of a set of tweets)
    '''
    
    (entity_type, key) = entity_key
    tokens = []

    for tweet in tweets:
        dictionary = tweet["entities"][entity_type]
        for data in dictionary:
            tokens.append(data[key].lower())

    return tokens


def find_top_k_entities(tweets, entity_key, k):
    '''
    Find the K most frequently occuring entitites

    Inputs:
        tweets: a list of tweets
        entity_key: a pair ("hashtags", "text"),
          ("user_mentions", "screen_name"), etc
        k: integer

    Returns: list of entity, count pairs
    '''
    tokens = load_tweets(tweets, entity_key)

    top_k = find_top_k(tokens, k)
        
    return top_k


def find_min_count_entities(tweets, entity_key, min_count):
    '''
    Find the entities that occur at least min_count times.

    Inputs:
        tweets: a list of tweets
        entity_key: a pair ("hashtags", "text"),
          ("user_mentions", "screen_name"), etc
        min_count: integer

    Returns: list of entity, count pairs
    '''

    tokens = load_tweets(tweets, entity_key)

    min_count_entities = find_min_count(tokens, min_count)
        
    return min_count_entities


def process(tweet, n, skip='do not skip'):
    '''
    Takes a bunch of messy tweets and returns a list of ngrams
    with all the punctuation, hashtag symbols, url's, etc.
    filtered out. Optionally, certain "STOP WORDS" can be
    filtered out as well.


    Inputs:
        tweets: a list of tweets
        n : int, length of n-grams
        skip: optional argument, put sany value to skip stop
        word filtering

    Returns:
        tokens: a list of all the words that appear in tweets
    '''

    ngrams = []
    tokens = []
    data = tweet["abridged_text"].lower()
    data = data.split()
    for string in data:
        string = string.strip(PUNCTUATION)
        if not string.startswith(STOP_PREFIXES):
            if skip != "do not skip":
                tokens.append(string)
            else:
                if string not in STOP_WORDS:
                    tokens.append(string)
    tokens = list(filter(None, tokens))
    for i in range(len(tokens) - n + 1):
        ngrams.append(tuple(tokens[i:i + n]))

    return ngrams

def find_top_k_ngrams(tweets, n, k):
    '''
    Find k most frequently occurring n-grams across all tweets

    Inputs:
        tweets: a list of tweets
        n: integer
        k: integer

    Returns: list of key/value pairs
    '''
    ngrams = []

    for tweet in tweets:
        ngrams = ngrams + process(tweet, n)
    
    top_k_ngrams = find_top_k(ngrams, k)

    return top_k_ngrams


def find_min_count_ngrams(tweets, n, min_count):
    '''
    Find n-grams that occur at least min_count times across all
    tweets.

    Inputs:
        tweets: a list of tweets
        n: integer
        min_count: integer

    Returns: list of ngram/value pairs
    '''

    ngrams = []

    for tweet in tweets:
        ngrams = ngrams + process(tweet, n)
    
    sortedcutofflist = find_min_count(ngrams, min_count)

    return sortedcutofflist

def find_most_salient_ngrams(tweets, n, k):
    '''
    Find k most salient n-grams for each tweet.

    Inputs:
        tweets: a list of tweets
        n: integer
        k: integer

    Returns: list of list of strings
    '''

    ngrams = []

    for tweet in tweets:
        ngrams.append(process(tweet, n, "skip"))

    ngrams_salient = find_most_salient(ngrams, k)

    return ngrams_salient
