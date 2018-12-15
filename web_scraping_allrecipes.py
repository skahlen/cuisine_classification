# import libraries
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


def create_df(df_name):
    # create dataframe
    columns = ["title", "url", "ingredients", "calories", "servings", "prep_time", "categories"]
    df = pd.DataFrame(columns=columns)

    # save data
    df.to_csv(df_name, index=False, sep=';')


def get_next_link(url):
    # load page
    page = requests.get(url)
    print(page.status_code)  # 200 means load successfully

    # get page content
    soup = BeautifulSoup(page.content, 'html.parser')

    # get link
    link = soup.find('link', attrs={'rel': 'next'}).get('href')
    print(link)

    return link


def get_recipes(url):
    # load page
    page = requests.get(url)
    print(page.status_code)  # 200 means load successfully

    # get page content
    soup = BeautifulSoup(page.content, 'html.parser')

    # get links
    links = []
    for url in soup.findAll('a', attrs={'href': re.compile("^https://www.allrecipes.com/recipe/")}):
        links.append(url.get('href'))
        clean_links = list(set(links))

    print(clean_links)

    return clean_links


def get_ingredients(url, df_name):
    # load page
    page = requests.get(url)

    # get page content
    soup = BeautifulSoup(page.content, 'html.parser')

    # get recipe
    recipe = soup.findAll('span', attrs={'class': 'recipe-ingred_txt added'})

    if recipe:
        # get title
        title = soup.title.text
        print(title)

        # get ingredients
        ingredients = []
        for a in recipe:
            ingredients.append(a.text)

        # get calories
        if isinstance(soup.find('span', attrs={'class': 'calorie-count'}), type(None)):
            calories = 'NaN'
        else:
            calories = soup.find('span', attrs={'class': 'calorie-count'}).text

        # get servings
        if isinstance(soup.find('meta', attrs={'id': 'metaRecipeServings'}), type(None)):
            servings = 'NaN'
        else:
            servings = soup.find('meta', attrs={'id': 'metaRecipeServings'}).get('content')

        # get prep_time
        if isinstance(soup.find('span', attrs={'class': 'ready-in-time'}), type(None)):
            prep_time = 'NaN'
        else:
            prep_time = soup.find('span', attrs={'class': 'ready-in-time'}).text

        # get categories
        cats = soup.findAll('span', attrs={'class': 'toggle-similar__title'})
        categories = []
        for a in cats:
            categories.append(a.text)

        # read dataframe
        df = pd.read_csv(df_name, delimiter=';')

        # add data into our dataframe
        y = {"title": title,
             "url": url,
             "ingredients": ingredients,
             "calories": calories,
             "servings": servings,
             "prep_time": prep_time,
             "categories": categories}
        df = df.append(y, ignore_index=True)

        # save data
        df.to_csv(df_name, index=False, sep=';')


df_name = 'allrecipes222.csv'
create_df(df_name)

url = 'https://www.allrecipes.com/recipes/?page=1000'

while url:
    url_recipes = get_recipes(url)
    for recipe_link in url_recipes:
        get_ingredients(recipe_link, df_name)
    url = get_next_link(url)
