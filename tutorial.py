import json
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

ps = PorterStemmer()
file = 'train.json'
with open(file) as train_file:
    dict_train = json.load(train_file)

#print(dict_train[0])
#len(dict_train)
#print(dict_train[0]['ingredients'])

id_ = []
cuisine = []
ingredients = []
for i in range(len(dict_train)):
    id_.append(dict_train[i]['id'])
    cuisine.append(dict_train[i]['cuisine'])
    ingredients.append(dict_train[i]['ingredients'])

import pandas as pd

df = pd.DataFrame({'id': id_, 'cuisine': cuisine, 'ingredients': ingredients})
#print(df.head(5))
#print(df['cuisine'].value_counts())

new = []
for s in df['ingredients']:
    s = ' '.join(s)
    new.append(s)

df['ing'] = new
#print(df['ing'])

import re

l = []
for s in df['ing']:

    # Remove punctuations
    s = re.sub(r'[^\w\s]', '', s)

    # Remove Digits
    s = re.sub(r"(\d)", "", s)

    # Remove content inside paranthesis
    s = re.sub(r'\([^)]*\)', '', s)

    # Remove Brand Name
    s = re.sub(u'\w*\u2122', '', s)

    # Convert to lowercase
    s = s.lower()

    # Remove Stop Words
    stop_words = set(stopwords.words('english'))
    word_tokens = word_tokenize(s)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    filtered_sentence = []
    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)
    s = ' '.join(filtered_sentence)

    # Remove low-content adjectives

    # Porter Stemmer Algorithm
    words = word_tokenize(s)
    word_ps = []
    for w in words:
        word_ps.append(ps.stem(w))
    s = ' '.join(word_ps)

    l.append(s)

df['ing_mod'] = l
#print(df.head(10))

from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['ing_mod'])

#print(X)
#print(vectorizer.get_feature_names())
#print(len(new))
#print(type(df['ing'][0]))



