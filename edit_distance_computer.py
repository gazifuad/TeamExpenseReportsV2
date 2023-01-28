import editdistance as ed
import re

SUB_RE = r'[!-&*-\-:-@\[-_()]+'
SPLIT_RE = r' +'

def tokenize(string):
    '''
    Tokenizes input string.
    '''
    return re.split(SPLIT_RE, re.sub(SUB_RE,' ', string).lower())

def find_distance(pattern_str, text_str):
    '''
    Computes the minimum Levenshtein distance between input pattern tokens and each of the input text tokens
    INPUT
        pattern_str; pattern string
        text_str; text string to match substrings against
    RETURN
        the minimum distance between pattern_str and each n-gram of text_str tokens
    '''
    pattern = tokenize(pattern_str)
    text = tokenize(text_str)
    tokens_in_pattern = len(pattern)
    nearest_dist = float('inf')
    for ind in (range(len(text))):
        pattern_candidate = ''.join(pattern[ind: ind+tokens_in_pattern])
        text_candidate = ''.join(text[ind: ind+tokens_in_pattern])
        nearest_dist = min(nearest_dist, ed.eval(pattern_candidate, text_candidate))
    return nearest_dist