# import libraries
import pandas as pd

# load data
df = pd.read_csv('allrecipes.csv', delimiter=';')
print(df.columns.values)
print(df.head())
print(df.shape)

# clean title
df['title'].replace(['Recipe - Allrecipes.com', '[^a-zA-Z0-9 ,-./]'], '', regex=True, inplace=True)
df['title'] = df['title'].str.lower()

# dictionary
quantity_words = ['cups', 'cup', 'teaspoons', 'teaspoon', 'tablespoons', 'tablespoon', 'ounces', 'ounce', 'cans', 'can',
                  'pounds', 'pound']
descriptive_words = ['chopped', 'cut', 'half']
other_words = [' and ', ' or ', ' more ', ' to ', ' taste ', ' in ']

# clean ingredients
df['ingredients'].replace('[^a-zA-Z ,]', '', regex=True, inplace=True)
df['ingredients'].replace(quantity_words, '', regex=True, inplace=True)
df['ingredients'].replace(descriptive_words, '', regex=True, inplace=True)
df['ingredients'].replace(other_words, '', regex=True, inplace=True)
df['ingredients'].replace(['  ', '  '], ' ', regex=True, inplace=True)
df['ingredients'] = df['ingredients'].str.lower()

# clean calories
df['calories'].replace([' cals', ' '], '', regex=True, inplace=True)

# clean categories
df['categories'].replace([r'\\n', '  ', "'Home',", "'Recipes',", "Recipes", '  '], '', regex=True, inplace=True)
df['categories'].replace('[^a-zA-Z0-9 ,./]', '', regex=True, inplace=True)
df['categories'] = df['categories'].str.lower()

# remove duplicates rows
df.drop_duplicates(inplace=True)

# remove empty rows
df.dropna(subset=['title', 'url', 'ingredients'], inplace=True)

print(df.head())
print(df.shape)

# save data
df.to_csv('allrecipes.csv', index=False, sep=';')

