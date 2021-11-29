
import pandas as pd
from bs4 import BeautifulSoup
import requests as rq
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
'''


# pandas options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

# read excel file
data = pd.read_excel("data.xlsx")

# print(data.shape)
# drop duplicated rows
data.drop_duplicates(inplace=True)
# print(data.shape)

# List of url
url_list = data['Imdb Link'].tolist()
# print(url_list)

# Lists to store scrapped data

production_year = []
genres = []
actors = []
locations = []

# queremos obtener los campos en ingles
headers = {"Accept-Languaje": "en-US, en;q=0.5"}

# En primer lugar, tendremos que controlar la tasa de crawl para que no veten nuestra IP
# Tambien tenemos que ver el status code de las peticiones
i = 0
for url in url_list:
    print(i,"  ",url)
    i = i+1

    # recorremos todas las url
    response = rq.get(url, headers=headers)

    # temp lists
    temp_actors = []
    temp_genres = []

    if response.status_code != 200:
        print("url incorrecta. Codigo distinto de 200")
        continue

    page_html = BeautifulSoup(response.text, 'html.parser')

    # scrape the year
    film_year = page_html.find('li', attrs = {"data-testid":"title-details-releasedate"})
    film_year = film_year.find("a", class_ = "ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link")
    film_year = film_year.text
    
    production_year.append(film_year)

    # scrape the genres
    # class_="ipc-chip-list GenresAndPlot__OffsetChipList-cum89p-5 dMcpOf"
    genres_container = page_html.find('div', attrs = {"data-testid":"genres"})
    film_genres = genres_container.find_all(class_='ipc-chip__text')
    for genre in film_genres:
        temp_genres.append(genre.text)
    
    genres.append(temp_genres)

    # scrape the actors
    film_actors = page_html.find_all("a", attrs ={"data-testid":"title-cast-item__actor"})
    for actor in film_actors:
        temp_actors.append(actor.text)
    
    actors.append(temp_actors)

    # scrape the locations
    film_loc = page_html.find("li", attrs={"data-testid": "title-details-filminglocations"})
    # some films dont have filming locations
    if film_loc is not None:
        film_loc = film_loc.find("a", class_= "ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link")
        film_loc = film_loc.text

    else:
        film_loc = "unknown"
        
    locations.append(film_loc)


cleaned_imdb = pd.DataFrame({'production_year': production_year,
                             'genres': genres,
                             'actors': actors,
                             'filming_locations': locations
                             })
print(cleaned_imdb.info())
print(data.info())


