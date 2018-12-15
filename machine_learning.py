# import libraries
import pandas as pd

# load data
df = pd.read_csv('my_data.csv', delimiter=';')

#
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['stem_ing'])
print(X)

#
from sklearn import preprocessing
le = preprocessing.LabelEncoder()
le.fit(df['continent'])
df['continent'] = le.transform(df['continent'])
Y = df['continent']
print(Y)




