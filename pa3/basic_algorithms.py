'''
Analyzing Election Tweets

Jerry Shi

Algorithms for efficiently counting and sorting distinct `entities` or
unique values, are widely used in data analysis. Functions to
implement: count_tokens, find_top_k, find_min_count, find_frequent
'''

import math

from util import sort_count_pairs

def count_tokens(tokens):
    '''
    Counts each distinct token (item or entity) in a list of tokens

    Inputs:
        tokens: list of tokens (must be hashable/comparable)

    Returns: list of tuples, (token, number of occurrences).
    '''

    d = {}
    countlist = []
    
    for token in tokens:
        d[token] = d.get(token, 0) + 1

    for token in d:
        countlist.append((token, d.get(token)))

    return countlist


def find_top_k(tokens, k):
    '''
    Find the k most frequently occurring tokens

    Inputs:
        tokens: list of tokens (must be hashable/comparable)
        k: a non-negative integer

    Returns: sorted list of the top k tuples

    '''

    # Error checking (DO NOT MODIFY)
    err_msg = "In find_top_k, k must be a non-negative integer"
    assert k >= 0, err_msg

    countlist = count_tokens(tokens)

    sortedlist = sort_count_pairs(countlist)

    return sortedlist[0:k]


def find_min_count(tokens, min_count):
    '''
    Find the tokens that occur at least min_count times

    Inputs:
        tokens: a list of tokens (must be hashable/comparable)
        min_count: integer

    Returns: sorted list of tuples
    '''

    countlist = count_tokens(tokens)

    cutofflist = []

    for count in countlist:
        (token, value) = count
        if value >= min_count:
            cutofflist.append(count)

    sortedcutofflist = sort_count_pairs(cutofflist)

    return sortedcutofflist

def find_most_salient_helper(docs):
    '''
    Helps find_most_salient function by creating a dictionary
    of doc counts.

    Inputs:
        docs: a list of lists of tokens

    Outputs:
        dic_doc_counts: a dictionary of how many documents
          each term appears in, calculated across all documents
    '''
    dict_doc_counts = {}
    for doc in docs:
        doc_counts = count_tokens(doc)
        for token, count in doc_counts:
            dict_doc_counts[token] = dict_doc_counts.get(token, 0) + 1
            # dictionary of number of documents each token is present in

    return dict_doc_counts

def find_most_salient(docs, k):
    '''
    Find the k most salient tokens in each document

    Inputs:
        docs: a list of lists of tokens
        k: integer

    Returns: list of sorted list of tokens
     (inner lists are in decreasing order of tf-idf score)
    '''

    dict_doc_counts = find_most_salient_helper(docs)
    tf_idf_scores_cutoff = []
 
    for doc in docs:
        if len(doc) == 0:
            tf_idf_scores_cutoff.append([])
        # add empty lists for empty docs
        else:
            sorted_doc_counts = sort_count_pairs(count_tokens(doc))
            tf_idf_scores = []
            max_count = sorted_doc_counts[0][1]
            for token, count in sorted_doc_counts:
                tf = 0.5 + (0.5 * count / max_count)
                idf = math.log(len(docs)/ dict_doc_counts.get(token))
                tf_idf_scores.append((token, tf * idf))
            sorted_tf_idf_scores = sort_count_pairs(tf_idf_scores)
            for i, token_and_count in enumerate(sorted_tf_idf_scores):
                (token, count) = token_and_count
                sorted_tf_idf_scores[i] = token
            
            tf_idf_scores_cutoff.append(sorted_tf_idf_scores[:k])

    return tf_idf_scores_cutoff
