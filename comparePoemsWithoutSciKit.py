import sys
import os
import random

from collections import Counter
import re
import string
import math
import ipdb
import itertools
import numpy as np


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

def get_all_similarity(freqs):
    num_freqs = len(freqs)
    sim_matrix = np.zeros((num_freqs, num_freqs))
    for r,c in itertools.combinations(range(num_freqs),2):
        similarity = counter_cosine_similarity(freqs[r],freqs[c])
        sim_matrix[r,c] = similarity
        sim_matrix[c,r] = similarity
    return sim_matrix

def counter_cosine_similarity(c1, c2):
    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    return dotprod / (magA * magB)

def word_frequency(word_counter, stop_words=list()):
    for word in stop_words:
        word_counter[word] = 0;
    total = float(sum(word_counter.values()))
    for key in word_counter:
        word_counter[key] /= total
    return word_counter

def count_words(text):
    exclude = set(string.punctuation)
    text = ''.join(ch for ch in text if ch not in exclude)
    return Counter(w.lower() for w in re.findall(r"\w+", text))

def get_similarity(poems):
    stop_words = [word.strip() for word in open('stop_words.txt','rt').readlines()]
    poem_frequencies = [word_frequency(count_words(p),stop_words) for p in poems]
    sims = get_all_similarity(poem_frequencies)
    return sims

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
