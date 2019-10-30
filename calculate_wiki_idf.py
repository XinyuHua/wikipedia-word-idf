"""
Author: Xinyu Hua
This script reads unzipped Wikipedia dump as plain text. It first builds
a vocabulary of all alphabetical words appeared in the corpus, alongside
document frequency for each word.
"""
import os
import sys
import time
import glob
import numpy as np
from collections import Counter
from tqdm import tqdm
import multiprocessing as mp
from nltk import word_tokenize
import bs4
from bs4 import BeautifulSoup as bs

WIKIPEDIA_RAW_PATH = "data/wikipedia/"

cased = False
if len(sys.argv) > 1 and sys.argv[1] == "cased":
    cased = True

all_file_paths = glob.glob(WIKIPEDIA_RAW_PATH + "*/wiki_*")


def calculate_word_doc_freq(doc_raw):
    parsed = bs(doc_raw, 'html.parser')
    docs = list(parsed.children)
    word_doc_freq = Counter()
    total_doc = 0
    for ix, doc in enumerate(docs):
        if doc == "\n":
            continue

        if isinstance(doc, bs4.element.NavigableString):
            continue

        doc_text_split = doc.text.split('\n')
        if len(doc_text_split) <= 3:
            continue

        doc_words = set()
        total_doc += 1
        for ln_id, ln in enumerate(doc_text_split):
            if ln.strip() == 0:
                continue

            #for word in word_tokenize(ln):
            for word in ln.split():
                if not cased:
                    word = word.lower()

                if str.isalpha(word):
                    doc_words.add(word)

        for word in doc_words:
            word_doc_freq[word] += 1

    return word_doc_freq, total_doc


total_word_doc_freq = Counter()
total_doc_num = 0

## single process
'''
for file_path in tqdm(all_file_paths):
    doc_raw = open(file_path).read()
    cur_doc_freq, cur_doc_num = calculate_word_doc_freq(doc_raw)
    total_word_doc_freq += cur_doc_freq
    total_doc_num += cur_doc_num
'''

## multi processes
all_doc_raw = [open(fpath).read() for fpath in tqdm(all_file_paths)]
pool = mp.Pool(mp.cpu_count())
results = pool.map(calculate_word_doc_freq, all_doc_raw)
pool.close()

for ln in tqdm(results):
    cur_doc_freq, cur_doc_num = ln
    total_word_doc_freq += cur_doc_freq
    total_doc_num += cur_doc_num

if cased:
    fout = open("doc_freq_cased.txt", 'w')
else:
    fout = open("doc_freq.txt", 'w')

fout.write("total doc: {:d}\n\n".format(total_doc_num))
sorted_doc_freq = sorted(total_word_doc_freq.items(), key=lambda x:x[1],
                         reverse=True)
for item in sorted_doc_freq:
    idf = np.log((total_doc_num/(1 + item[1])))
    fout.write(item[0] + '\t' + str(item[1]) + '\t' + str(idf) + '\n')
fout.close()


