from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

def cos_sim(pattern_str, text_str):
    # Initialize vectorizer
    vectorizer = CountVectorizer().fit_transform([pattern_str, text_str])
    # compute and cosine similarity of texts
    similarity = cosine_similarity(vectorizer[0:1], vectorizer[1:2])
    
    return similarity[0][0]
