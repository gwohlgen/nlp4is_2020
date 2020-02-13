from __future__ import print_function
import nltk
import sys
from nltk.corpus import gutenberg
from operator import itemgetter
from pprint import pprint

"""
    here we do text-book style index generation
"""


# create vocabulary

# step 1 -- create token list
token_list = []

for i, fileid in enumerate( gutenberg.fileids() ):
   
    file_tokens = [(w,i) for w in gutenberg.words(fileid)] 
    print("first 5 tokens of fileid", fileid, ":"); pprint(file_tokens[:5]) 

    ## for boolean index we don't need duplicates
    file_tokens = list(set(file_tokens)) 

    token_list.extend(file_tokens)


# step 2, sort
token_list = sorted(token_list, key=itemgetter(0,1))
print("first 50 tokens of final token_list: "); pprint(token_list[:50])


# step 3, create the index     
inv_index = {}

for (word, doc_no) in token_list:
 
    if not word in inv_index:
        inv_index[word] = {'postings': set(), 'df': 0}

    inv_index[word]['postings'].add(doc_no)

## set document frequency (df)
for word, vals in inv_index.items():
    inv_index[word]['df'] = len(inv_index[word]['postings'])


print ('Number of words in the index:', len(inv_index))
#pprint(inv_index)


print('Some test entries from the inverted index:')
print('Jane', inv_index['Jane'])
print('man', inv_index['man'])
print('zoology', inv_index['zoology'])
print('Caesar', inv_index['Caesar'])
print('Brutus', inv_index['Brutus'])
print('\n\n')



### query -- AND
def process_query(query_words):
   
    res = inv_index[query_words[0]]['postings']
    for qw in query_words:
        res = res & inv_index[qw]['postings']
    return res


print("search ['Caesar','Brutus','hand']", process_query(['Caesar','Brutus','hand']))
print("search ['Caesar']", process_query(['Caesar']))
print("search ['Caesar', 'Jane']", process_query(['Caesar', 'Jane']))



## Exercise .. manually code the merge process for according to INTERSECT algorithm
## make your own process_query function

