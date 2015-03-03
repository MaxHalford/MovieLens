from pymongo import MongoClient
import pandas as pd

# Connect to the database
client = MongoClient()
db = client.Projet_Stat_L3.Users
# Retrieve all the data
users = db.find()
# Open the CSV file with the categorized data
df = pd.read_csv('data/categorized')

# Build the contingency tables
releaseVSoccupation = pd.crosstab(df.occupation, df.releaseDecade)
releaseVSgender = pd.crosstab(df.gender, df.releaseDecade)
releaseVSage = pd.crosstab(df.ageCategory, df.releaseDecade)
releaseVSstate = pd.crosstab(df.state, df.releaseDecade)
# We split the genres of a film, let's use the database
genres = ('Action', 'Adventure', 'Animation',
          'Children', 'Comedy', 'Crime', 'Documentary',
          'Drama', 'Fantasy', 'Film-Noir', 'Horror',
          'Musical', 'Mystery', 'Romance', 'Sci-Fi',
          'Thriller', 'War', 'Western')
occupations = set(df['occupation'].get_values())
genders = set(df['gender'].get_values())
ageCategories = set(df['ageCategory'].get_values())
states = set(df['state'].get_values())
# Create the contingency tables
genreVSoccupation = pd.DataFrame(index = genres, columns = occupations).fillna(0)
genreVSgender = pd.DataFrame(index = genres, columns = genders).fillna(0)
genreVSage = pd.DataFrame(index = genres, columns = ageCategories).fillna(0)
genreVSstate = pd.DataFrame(index = genres, columns = states).fillna(0)
# Fill the contingency tables
for user in users:
    for film in user['ratings']:
        for genre in film['genres']:
            # Occupation
            genreVSoccupation[user['occupation']][genre] += 1
            # Gender
            genreVSgender[user['gender']][genre] += 1
            # Age category
            genreVSage[user['ageCategory']][genre] += 1
            # State
            genreVSstate[user['state']][genre] += 1

releaseVSoccupation.to_csv('data/releaseVSoccupation', index = False)
releaseVSgender.to_csv('data/releaseVSgender', index = False)
releaseVSage.to_csv('data/releaseVSage', index = False)
releaseVSstate.to_csv('data/releaseVSstate', index = False)
genreVSoccupation.to_csv('data/genreVSoccupation', index = False)
genreVSgender.to_csv('data/genreVSgender', index = False)
genreVSage.to_csv('data/genreVSage', index = False)
genreVSstate.to_csv('data/genreVSstate', index = False)
