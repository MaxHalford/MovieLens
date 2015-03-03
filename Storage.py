import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import re
import numpy as np
import json
from six.moves.urllib.request import urlopen
from unidecode import unidecode

client = MongoClient()
db = client.Projet_Stat_L3.Users
db.Users.drop()

# Get the data
ratings = pd.read_table('ml-100k/u.data',
                        delimiter = r'\s+',
                        names = ('userID', 'filmID', 'score', 'timeStamp'))
films = pd.read_table('ml-100k/u.item',
                      delimiter = '|',
                      encoding = 'latin-1',
                      index_col = False,
                      names = ('filmID', 'title', 'releaseDate',
                               'videoReleaseDate', 'IMDbURL', 'unknown',
                               'Action', 'Adventure', 'Animation',
                               'Children', 'Comedy', 'Crime', 'Documentary',
                               'Drama', 'Fantasy', 'Film-Noir', 'Horror',
                               'Musical', 'Mystery', 'Romance', 'Sci-Fi',
                               'Thriller', 'War', 'Western'))
users = pd.read_table('ml-100k/u.user',
                      delimiter = '|',
                      names = ('userID', 'age', 'gender', 'occupation', 'zip'))
# Convert the UNIX timestamps to a datetimes
ratings['timeStamp'] = ratings['timeStamp'].apply(datetime.fromtimestamp)
# Get the genre of every movie
genres = ('unknown', 'Action', 'Adventure', 'Animation',
          'Children', 'Comedy', 'Crime', 'Documentary',
          'Drama', 'Fantasy', 'Film-Noir', 'Horror',
          'Musical', 'Mystery', 'Romance', 'Sci-Fi',
          'Thriller', 'War', 'Western')
filmGenres = {}
filmsRows = films.iterrows()
for i, film in filmsRows:
    filmGenres[film['filmID']] = [genre for genre in genres if film[genre]]

# Join the dataframes
tmp = pd.merge(ratings, films[['filmID', 'title', 'releaseDate']])
df = pd.merge(tmp, users)
# Add the concatenated genres of a movie to the dataframe
df['genre'] = None
for i in range(df.shape[0]):
    genre = '/'.join(filmGenres[df.ix[i]['filmID']])
    df['genre'][i] = genre
# Only keep scores above 3
df = df[df['score'] > 3]

# Categorize all the data
data = df.dropna().copy()
# Classify the ages
def ageCategory(age):
    if age < 20: return 'Teenage'
    elif age < 30: return 'Twenties'
    elif age < 40: return 'Thirties'
    elif age < 50: return 'Forties'
    else: return 'Over fifty'
data['ageCategory'] = data['age'].apply(lambda age: ageCategory(age))
# Classify the release dates
def releaseDateYear(date):
    year = int(re.search('(\d{4})', date).group(0))
    if year > 1989: return '90s'
    elif year > 1979: return '80s'
    elif year > 1969: return '70s'
    elif year > 1959: return '60s'
    elif year > 1949: return '50s'
    elif year > 1939: return '40s'
    elif year > 1929: return '30s'
    elif year > 1919: return '20s'
    elif year > 1909: return '10s'
    else: return '1900s'
data['releaseDecade'] = data['releaseDate'].apply(lambda date: releaseDateYear(date))
# Classify the zip codes
states = {}
def zipState(zip):
    # Some of the zip are not part of the US
    if zip.isdigit() and len(zip) == 5:
        # Don't do an API request more than once
        if zip not in states.keys():
            # Some 5 digit zipcodes are not valid
            try:
                # Use the zippopotam API
                '''
This can be improved by using a database and not an API (bottleneck here)
'''
                response = urlopen('http://api.zippopotam.us/us/' + zip)
                info = json.loads(response.read().decode('utf8'))
                states[zip] = info['places'][0]['state']
                return (states[zip])
            # Not a valid zipcode
            except Exception:
                return np.nan
        # We already have the zipcodes state
        else:
            return states[zip]
    # Not a valid zipcode
    else:
        return np.nan
data['state'] = data['zip'].apply(lambda zip: zipState(zip))
data = data.dropna()
data.to_csv('data/categorized', index = False)

# Iterate over every row on the new dataframe
users = {}
rows = data.iterrows()
for i, row in rows:
    film = {}
    film['title'] = row['title']
    film['releaseDecade'] = row['releaseDecade']
    film['releaseDate'] = row['releaseDate']
    film['genres'] = filmGenres[row['filmID']]
    film['score'] = row['score']
    film['time'] = row['timeStamp']
    # Avoid redundancy
    if row['userID'] not in users.keys():
        user = {}
        user['ageCategory'] = row['ageCategory']
        user['age'] = row['age']
        user['gender'] = row['gender']
        user['occupation'] = row['occupation']
        user['state'] = row['state']
        user['zip'] = row['zip']
        user['ratings'] = [film]
        users[row['userID']] = user
    else:
        users[row['userID']]['ratings'].append(film)

# Store the data
for key in users.keys():
    user = users[key]
    db.save({'_id' : key, 'ageCategory' : user['ageCategory'], 'age' : user['age'],
             'gender' : user['gender'], 'occupation' : user['occupation'],
             'state' : user['state'], 'ratings' : user['ratings']})
