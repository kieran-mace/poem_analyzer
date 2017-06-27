import sys
import os
import random
import math
import itertools
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

def load_poem(poem_path):
    poem_file = open(poem_path,'rt')
    poem = ' '.join(poem_file.readlines())
    return poem

def load_poems(dir):
    poem_files = os.listdir(dir)
    poems = list()
    for poem_filename in poem_files:
        # Load up source file
        poems.append(load_poem(dir + '/' + poem_filename))
    return poems

def get_similarity(poems):
    tfidf_vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 3))
    tfidf_matrix = tfidf_vectorizer.fit_transform(poems)
    return cosine_similarity(tfidf_matrix, tfidf_matrix)

def get_most_similar_indexes(scores, num):
    order, vals = zip(*sorted(enumerate(scores), key=lambda x:x[1], reverse=True)[0:num])
    return order

def main(argv):
    if len(argv) != 4:
        sys.stderr.write("Usage: %s reference_poems_dir query_poem num_most_similar\n" % argv[0])
        return 1

    #load poems
    reference_poems_dir = sys.argv[1]
    query_poem_path = sys.argv[2]
    num_sim = int(sys.argv[3])

    reference_poems = load_poems(reference_poems_dir)
    query_poem = load_poem(query_poem_path)

    all_poems = list()
    all_poems.append(query_poem)
    all_poems.extend(reference_poems)
    all_scores = get_similarity(all_poems)
    ref_scores = all_scores[0,1:]
    top_hits = get_most_similar_indexes(ref_scores,num_sim)
    poem_files = os.listdir(reference_poems_dir)
    best_files = [poem_files[top_hits[i]] for i in range(num_sim)]
    print 'The most similar files to that are:'
    for f in best_files:
        print f


if __name__=='__main__':
    sys.exit(main(sys.argv))
