# import libraries
import pandas as pd
from nltk.stem import PorterStemmer
from nltk import word_tokenize

# load data
df = pd.read_csv('allrecipes.csv', delimiter=';')

# keep only world recipe cuisine recipes
df = df[df['categories'].str.contains(''.join('world cuisine'))]

# create continent column
continent = []
for row in df['categories']:
    words = row.split(',')
    continent.append(words[1])
df['continent'] = continent

# value count
print(df['continent'].value_counts())

# words stemming
ps = PorterStemmer()
y = []
for row in df['ingredients']:
    words = word_tokenize(row)
    stem_ing = []
    for word in words:
        stem_ing.append(ps.stem(word))
    x = ' '.join(stem_ing)
    y.append(x)
df['stem_ing'] = y
print(df[['stem_ing', 'continent']].head())

# save data
df[['stem_ing', 'continent']].to_csv('my_data.csv', index=False, sep=';')




