import editdistance as ed
import re
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

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
    for ind in (range(len(text) - tokens_in_pattern)):
        pattern_candidate = ''.join(pattern)
        text_candidate = ''.join(text[ind: ind+tokens_in_pattern])
        nearest_dist = min(nearest_dist, ed.eval(pattern_candidate, text_candidate))
        # print(pattern_candidate)
        # print(text_candidate)
        # print(ed.eval(pattern_candidate, text_candidate))
    return nearest_dist


def cos_sim(pattern_str, text_str):
    # Initialize vectorizer
    vectorizer = CountVectorizer().fit_transform([pattern_str, text_str])

    # compute and cosine similarity of texts
    similarity = cosine_similarity(vectorizer[0:1], vectorizer[1:2])
    
    return similarity[0][0]

# print(find_distance('RESTTORAN WAN SHENG', 'Hello there Obi Wan This is some sample text'))