
import pandas as pd
from bs4 import BeautifulSoup
import requests as rq
import json
from time import sleep
from random import randint

'''
# test
url = "https://www.imdb.com/title/tt0368343"
headers = {"Accept-Languaje": "en-US, en;q=0.5"}
response = rq.get(url, headers = headers)
# class_='TitleBlockMetaData__ListItemText-sc-12ein40-2 jedhex'
html_soup = BeautifulSoup(response.text, 'html.parser')
film_year = html_soup.find('li', attrs = {"data-testid":"title-details-releasedate"})
film_year = film_year.find("a", class_ = "ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link")

# print(film_year)
film_year= film_year.text
film_year = film_year.rpartition(',')[2]
film_year = film_year.rpartition('(')[0]
film_year = film_year.strip()

print(film_year)

genres_container = html_soup.find("div", attrs = {"data-testid":"genres"})
# print(genres_container)
film_genres = genres_container.find_all(class_='ipc-chip__text')
temp_genres = []
for genre in film_genres:
        temp_genres.append(genre.text)
print(temp_genres)

film_actors = html_soup.find_all("a", attrs ={"data-testid":"title-cast-item__actor"})
# print(film_actors)
temp_actors = []

for actor in film_actors:
    temp_actors.append(actor.text)
# print(temp_actors)

film_loc = html_soup.find("li", attrs={"data-testid": "title-details-filminglocations"})
temp_locs = []
# print(film_loc)

film_loc = film_loc.find("a", class_= "ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link")
film_loc = film_loc.text
print(film_loc)

dic1 = {"index": {"_index": "movies", "_type": "film", "_id":"0\\n"}}
dic2 = {"film_year":film_year, "genres":temp_genres, "actors":temp_actors, "location":film_loc}

with open("test.json", 'a') as f:
    json.dump(dic1, f)
    f.write('\n')
    json.dump(dic2, f)
'''





# pandas options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

# read excel file
data = pd.read_excel("data.xlsx")

data = data[['imdbId', 'Imdb Link', 'Title', 'Genre']]
test_data = data.head(10)

# drop duplicated rows
data.drop_duplicates(inplace=True)


# List of url
url_list = data['Imdb Link'].tolist()
id_list = data['imdbId'].tolist()
title_list = data['Title'].tolist()
genre_list = data['Genre'].tolist()

index = url_list.index('http://www.imdb.com/title/tt0466909')

# Lists to store scrapped data
imdb_id = []
production_year = []
genres = []
actors = []
locations = []

# queremos obtener los campos en ingles
headers = {"Accept-Languaje": "en-US, en;q=0.5"}

i = 0
index_id = 0
isString = False

for url in url_list:

    id = id_list[i]
    title = title_list[i]
    film_year_excel = title.rpartition('(')[2]
    film_year_excel = film_year_excel.rpartition(')')[0]
    film_year_excel = film_year_excel.strip()
    print("a??o excel", film_year_excel)
    title = title.rpartition('(')[0]
    title = title.strip()

    genre = genre_list[i]
    if isinstance(genre, str):
        genre = genre.split('|')
    else:
        genre = ['unknown']


    print(i,"  ",url)
    # print(id)

    # recorremos todas las url
    response = rq.get(url, headers=headers)

    # temp lists
    temp_actors = []
    temp_genres = []
    i = i + 1

    if response.status_code != 200:
        print("url incorrecta. Codigo distinto de 200")
        continue



    page_html = BeautifulSoup(response.text, 'html.parser')

    # scrape the year
    film_year = page_html.find('li', attrs = {"data-testid":"title-details-releasedate"})
    if film_year is not None:
        film_year = film_year.find("a", class_ = "ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link")
        film_year = film_year.text
        film_year = film_year.rpartition(',')[2]
        film_year = film_year.rpartition('(')[0]
        film_year = film_year.strip()
    else:
        film_year = film_year_excel
    


    # scrape the genres

    genres_container = page_html.find('div', attrs = {"data-testid":"genres"})
    if genres_container is not None:
        film_genres = genres_container.find_all(class_='ipc-chip__text')
        for genre in film_genres:
            temp_genres.append(genre.text)
    else:
        temp_genres = genre.copy()


    # scrape the actors
    film_actors = page_html.find_all("a", attrs ={"data-testid":"title-cast-item__actor"})
    for actor in film_actors:
        temp_actors.append(actor.text)



    # scrape the locations
    film_loc = page_html.find("li", attrs={"data-testid": "title-details-filminglocations"})
    # some films dont have filming locations
    if film_loc is not None:
        film_loc = film_loc.find("a", class_= "ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link")
        film_loc = film_loc.text

    else:
        film_loc = "unknown"
        

    dic_1 = {"index": {"_index": "movies", "_type": "film", "_id":index_id}}
    dic_2 = {"imdb_id":id, "title":title, "film_year":film_year, "genres": temp_genres, "actors": temp_actors, "location":film_loc}

    with open("movies2.json", 'a', encoding = 'UTF-8') as f:
        json.dump(dic_1, f)
        f.write('\n')
        json.dump(dic_2, f)
        f.write('\n')
        f.close()

    index_id = index_id + 1









