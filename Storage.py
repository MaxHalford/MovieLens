import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import re
import numpy as np
import json
from six.moves.urllib.request import urlopen
from unidecode import unidecode

# Connect to the database
client = MongoClient()
db = client.MovieLens
db.Users.drop()

# Get the data
genres = ('Unknown', 'Action', 'Adventure', 'Animation',
          'Children', 'Comedy', 'Crime', 'Documentary',
          'Drama', 'Fantasy', 'Film-Noir', 'Horror',
          'Musical', 'Mystery', 'Romance', 'Sci-Fi',
          'Thriller', 'War', 'Western')

ratings = pd.read_table('ml-100k/u.data',
                        delimiter = r'\s+',
                        names = ('userID', 'filmID', 'score', 'timeStamp'))
films = pd.read_table('ml-100k/u.item',
                      delimiter = '|',
                      encoding = 'latin-1',
                      index_col = False,
                      names = ('filmID', 'title', 'releaseDate',
                               'videoReleaseDate', 'IMDbURL',
                               'Unknown', 'Action', 'Adventure', 'Animation',
                               'Children', 'Comedy', 'Crime', 'Documentary',
                               'Drama', 'Fantasy', 'Film-Noir', 'Horror',
                               'Musical', 'Mystery', 'Romance', 'Sci-Fi',
                               'Thriller', 'War', 'Western'))
users = pd.read_table('ml-100k/u.user',
                      delimiter = '|',
                      names = ('userID', 'age', 'gender', 'occupation', 'zip'))
                      
# Convert the UNIX timestamps to datetimes
ratings['timeStamp'] = ratings['timeStamp'].apply(datetime.fromtimestamp)
# Get the genre of each movie
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
data['ageCategory'] = data['age'].apply(lambda age: str(age)[0] + '0s')
# Classify the release dates
data['releaseDecade'] = data['releaseDate'].apply(lambda date: '19' + re.search('(\d{4})', date).group(0)[2] + "0s")
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
                response = urlopen('http://api.zippopotam.us/us/' + zip)
                info = json.loads(response.read().decode('utf8'))
                states[zip] = info['places'][0]['state']
                return (states[zip])
            # Not a valid zipcode
            except Exception:
                return 'Other'
        # We already have the zipcodes state
        else:
            return states[zip]
    # Not a valid zipcode
    else:
        return 'Other'
data['state'] = data['zip'].apply(lambda zip: zipState(zip))
# Get the US region (http://www.wikiwand.com/en/U.S._state)
regions = {
    'Washington' : 'West',
    'Oregon' : 'West',
    'California' : 'West',
    'Idaho' : 'West',
    'Nevada' : 'West',
    'Utah' : 'West',
    'Arizona' : 'West',
    'Montana' : 'West',
    'Wyoming' : 'West',
    'Colorado' : 'West',
    'New Mexico' : 'West',
    'North Dakota' : 'Midwest',
    'South Dakota' : 'Midwest',
    'Nebraska' : 'Midwest',
    'Kansas' : 'Midwest',
    'Minnesota' : 'Midwest',
    'Iowa' : 'Midwest',
    'Missouri' : 'Midwest',
    'Wisconsin' : 'Midwest',
    'Illinois' : 'Midwest',
    'Michigan' : 'Midwest',
    'Indiana' : 'Midwest',
    'Ohio' : 'Midwest',
    'Oklahoma' : 'South',
    'Texas' : 'South',
    'Arkansas' : 'South',
    'Louisiana' : 'South',
    'Kentucky' : 'South',
    'Tennessee' : 'South',
    'Mississippi' : 'South',
    'Alabama' : 'South',
    'Florida' : 'South',
    'Georgia' : 'South',
    'South Carolina' : 'South',
    'North Carolina' : 'South',
    'Virginia' : 'South',
    'West Virginia' : 'South',
    'Maryland' : 'South',
    'Delaware' : 'South',
    'Maine' : 'North-East',
    'New Hampshire' : 'North-East',
    'Vermont' : 'North-East',
    'New York' : 'North-East',
    'Pennsylvania' : 'North-East',
    'New Jersey' : 'North-East',
    'Massachusetts' : 'North-East',
    'Connecticut' : 'North-East',
    'Rhode Island' : 'North-East',
    'District of Columbia' : 'North-East',
    'Other' : 'Other',
    'Alaska' : 'Other',
    'Hawaii' : 'Other'
}
data['region'] = data['state'].apply(lambda state: regions[state])

# Save the data
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
        user['region'] = row['region']
        users[row['userID']] = user
    else:
        users[row['userID']]['ratings'].append(film)

# Store the data
for key in users.keys():
    user = users[key]
    db.save({'_id' : key, 'ageCategory' : user['ageCategory'], 'age' : user['age'],
             'gender' : user['gender'], 'occupation' : user['occupation'],
             'state' : user['state'], 'region' : user['region'],
             'ratings' : user['ratings']})
