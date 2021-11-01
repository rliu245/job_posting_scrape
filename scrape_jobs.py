# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 18:43:20 2018

@author: Ray
"""

# lowercase text
def lower_case(text):
    return [word.lower() for word in text]

# remove punctuations for text
def remove_punctuation(text):
    import string
    
    remove_punctuations = str.maketrans("", "", string.punctuation)
    return [w.translate(remove_punctuations) for w in text]

def remove_numbers(text):
    return [word for word in text if word.isalpha()]
    
def remove_stopwords(text):
    from nltk.corpus import stopwords
    
    extra_stopwords = ['machine', 'learning', 'experience', 'work', 'new', 'ericsson', 'world', 'skills', 'data', 'science', 'company', 'working', 'help', 'build', 'people', \
                       'status', 'key', 'information', 'development', 'one', 'using', 'insights', 'scientist', 'product', 'business', 'client', 'looking', 'strong', 'etc',\
                       'ability', 'including', 'opportunity', 'analysis', 'models', 'develop', 'analytics', 'develop', 'knowledge', 'like', 'role', 'employees', 'drive', 'computer',\
                       'time', 'scientists', 'global', 'technology', 'platform', 'us', 'technologies', 'environment', 'large', 'apply', 'methods', 'make', 'use', 'san', 'problems',\
                       'network', 'eg', 'responsibility', 'way', 'preferred', 'expertise', 'technique', 'part', 'customer', 'deep', 'service', 'project', 'job', 'u', 'want', 'location',\
                       'state', 'set', 'need', 'solution', 'need', 'understanding', 'feature', 'impact', 'ha', 'system', 'field', 'next', 'vevo', 'building', 'across', 'create', \
                       'partner', 'process', 'francisco', 'take', 'level', 'disability', 'city', 'mission', 'enjoy', 'position', 'join']
    
    stop_words = set(stopwords.words('english'))
    stop_words.update(extra_stopwords)
    return [w for w in text if not w in stop_words]

def lemma(text):
    from nltk.stem import WordNetLemmatizer
    
    lemmatizer = WordNetLemmatizer()

    return [lemmatizer.lemmatize(word) for word in text]

def stemming(text):
    from nltk.stem.porter import PorterStemmer
    
    porter = PorterStemmer()
    return [porter.stem(word) for word in text]

import requests
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize

USER_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
times = 5

found_results = []
word_tokens = []

for i in range(10, 10*(1+times), 10):
    url = 'https://www.google.com/search?vet=10ahUKEwjs5rueotndAhVzIjQIHboUC2YQ06ACCIUF..i&ei=n8urW6ybMPPE0PEPuqmssAY&yv=3&rciv=jb&nfpr=0&chips=job_family_1:learning%20engineer,' + \
    'job_family_1:data%20scientist&q=data+science+entry+level&start={page}&asearch=tl_af&async=_id:gws-horizon-textlists__tl-af,_pms:hts,_fmt:pc'.format(page = i)
    response = requests.get(url, headers = USER_AGENT)
    t = response.text

    soup = BeautifulSoup(t, 'lxml')

    result_block = soup.find_all('li', attrs = {'class': 'PaEvOc gws-horizon-textlists__li-ed'})

    for result in result_block:
        title = result.find('div', attrs = {'class': 'BjJfJf gsrt LqLjSc'})
        description = result.find('span', attrs = {'class': 'Cyt8W HBvzbc'})
        
        title = title.get_text()
        description = description.get_text()
        
        found_results.append((title, description))
        
        for description in found_results:
            word_tokens.append(word_tokenize(description[1]))

    j = 0
    for words in word_tokens:
        word_tokens[j] = lower_case(words)
        word_tokens[j] = lemma(word_tokens[j])
        word_tokens[j] = remove_stopwords(word_tokens[j])
        word_tokens[j] = remove_punctuation(word_tokens[j])
        word_tokens[j] = remove_numbers(word_tokens[j])
    
        j = j + 1
    j = 0

import collections
import itertools
one_giant_list = list(itertools.chain(*word_tokens))
c = collections.Counter(one_giant_list)
    
final = [(k, v) for k, v in c.items()]
final.sort(key = lambda x: x[1])
final[-50:]