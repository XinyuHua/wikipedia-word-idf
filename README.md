# wikipedia-word-idf

This repository contains scripts to compute word IDF statistics on Wikipedia.
The unzipped Wikipedia dump is assumed to be stored at `data/wikipedia/`.

To run:

```
python calculate_wiki_idf.py [--cased]
```

The flag `--cased` indicates case sensitive dictionary, otherwise all tokens
will be lowercased. The result will be saved to `doc_freq.txt` or `doc_freq_cased.txt`.
The first line shows the total number of documents processed, and the dictionary
is sorted by descending order on document frequency.

Currently the script finishes in about 2 hours and 20 minutes. 
The file `doc_freq.min10.txt` contains the uncased version with words that
appear at least ten times in the entire corpus.
