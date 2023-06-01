'''
Analyzing Election Tweets

Test code for tweet analysis algorithms
'''

import os
import sys

import json
import pytest

import analyze

from test_helpers import read_config_file, \
    compare_tuple_lists, compare_list_of_lists

# Handle the fact that the grading code may not
# be in the same directory as analyze.py
sys.path.append(os.getcwd())

# Get the test files from the same directory as
# this file.
BASE_DIR = os.path.dirname(__file__)
TEST_DIR = os.path.join(BASE_DIR, "tests")

# Want to catch any exception thrown by student code.
#pylint: disable-msg=broad-except

######### Utilities #########

def setup_tweets(params):
    '''
    load the tweets from the file, if needed.
    '''

    try:
        recreate_msg = "To recreate this test in ipython3 run:\n"
        if "tweets_file" in params:
            recreate_msg += "  tweets = json.load(open({}))\n"
            recreate_msg = recreate_msg.format(params["tweets_file"])
            params["tweets"] = json.load(open(params["tweets_file"]))
        else:
            recreate_msg += "  tweets = {}\n".format(params["tweets"])

    except OSError as e:
        pytest.fail("{}".format(e))

    return recreate_msg

@pytest.mark.parametrize(
    "params",
    read_config_file("find_top_k_entities.json"))
def test_find_top_k_entities(params):
    '''
    test code for find_to_k_entities
    '''
    # fix the type of "entity_type"
    params["entity_type"] = tuple(params["entity_type"])

    # fix the type of expected
    params["expected"] = [tuple(t) for t in params["expected"]]

    recreate_msg = setup_tweets(params)

    call_str = "  analyze.find_top_k_entities(tweets, {}, {})"
    recreate_msg += call_str.format(params["entity_type"],
                                    params["k"])

    try:
        actual = analyze.find_top_k_entities(params["tweets"],
                                             params["entity_type"],
                                             params["k"])
    except Exception as e:
        msg = str(e) + "\n" + recreate_msg
        pytest.fail(msg)

    compare_tuple_lists(actual, params, recreate_msg)

@pytest.mark.parametrize(
    "params",
    read_config_file("find_min_count_entities.json"))
def test_find_min_count_entities(params):
    '''
    test code for find_min_count_entities
    '''

    # fix the type of "entity_type"
    params["entity_type"] = tuple(params["entity_type"])

    # fix the type of expected
    params["expected"] = [tuple(t) for t in params["expected"]]

    recreate_msg = setup_tweets(params)

    call_str = "  analyze.find_min_count_entities(tweets, {}, {})"
    recreate_msg += call_str.format(params["entity_type"],
                                    params["min_count"])
    try:
        actual = analyze.find_min_count_entities(params["tweets"],
                                                 params["entity_type"],
                                                 params["min_count"])
    except Exception as e:
        msg = str(e) + "\n" + recreate_msg
        pytest.fail(msg)

    compare_tuple_lists(actual, params, recreate_msg)


@pytest.mark.parametrize(
    "params",
    read_config_file("find_top_k_ngrams.json"))
def test_find_top_k_ngrams(params):
    '''
    test code for find_top_k_ngrams
    '''

    # fix the type of expected
    params["expected"] = [(tuple(k), v) for (k, v) in params["expected"]]

    recreate_msg = setup_tweets(params)

    call_str = "  analyze.find_top_k_ngrams(tweets, {}, {})"
    recreate_msg += call_str.format(params["n"],
                                    params["k"])
    try:
        actual = analyze.find_top_k_ngrams(params["tweets"],
                                           params["n"],
                                           params["k"])
    except Exception as e:
        msg = str(e) + "\n" + recreate_msg
        pytest.fail(msg)

    compare_tuple_lists(actual, params, recreate_msg)

@pytest.mark.parametrize(
    "params",
    read_config_file("find_min_count_ngrams.json"))
def test_find_min_count_ngrams(params):
    '''
    test code for find_min_count_ngrams
    '''

    # fix the type of expected
    params["expected"] = [(tuple(k), v) for (k, v) in params["expected"]]

    recreate_msg = setup_tweets(params)

    call_str = "  analyze.find_min_count_ngrams(tweets, {}, {})"
    recreate_msg += call_str.format(params["n"],
                                    params["min_count"])
    try:
        actual = analyze.find_min_count_ngrams(params["tweets"],
                                               params["n"],
                                               params["min_count"])
    except Exception as e:
        msg = str(e) + "\n" + recreate_msg
        pytest.fail(msg)

    compare_tuple_lists(actual, params, recreate_msg)


@pytest.mark.parametrize(
    "params",
    read_config_file("find_most_salient_ngrams.json"))
def test_find_most_salient_ngrams(params):
    '''
    test code for find_most_salient_ngrams
    '''

    # fix the type of expected
    params["expected"] = [[tuple(t) for t in l] for l in params["expected"]]

    recreate_msg = setup_tweets(params)

    call_str = "  analyze.find_most_salient_ngrams(tweets, {}, {})"
    recreate_msg += call_str.format(params["n"],
                                    params["k"])
    try:
        actual = analyze.find_most_salient_ngrams(params["tweets"],
                                                  params["n"],
                                                  params["k"])
    except Exception as e:
        msg = str(e) + "\n" + recreate_msg
        pytest.fail(msg)


    compare_list_of_lists(actual, params, recreate_msg)
