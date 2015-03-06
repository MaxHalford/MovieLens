from pymongo import MongoClient
import pandas as pd

'''
Release Decades
'''
# Open the CSV file with the categorized data
df = pd.read_csv('data/categorized')
males = df[df['gender'] == 'M']
females = df[df['gender'] == 'F']
# Build the contingency tables
M_releaseVSoccupation = pd.crosstab(males.occupation, males.releaseDecade)
M_releaseVSage = pd.crosstab(males.ageCategory, males.releaseDecade)
M_releaseVSregion = pd.crosstab(males.region, males.releaseDecade)
F_releaseVSoccupation = pd.crosstab(females.occupation, females.releaseDecade)
F_releaseVSage = pd.crosstab(females.ageCategory, females.releaseDecade)
F_releaseVSregion = pd.crosstab(females.region, females.releaseDecade)
# Save the dataframes
M_releaseVSoccupation.to_csv('data/male/releaseVSoccupation')
M_releaseVSage.to_csv('data/male/releaseVSage')
M_releaseVSregion.to_csv('data/male/releaseVSregion')
F_releaseVSoccupation.to_csv('data/female/releaseVSoccupation')
F_releaseVSage.to_csv('data/female/releaseVSage')
F_releaseVSregion.to_csv('data/female/releaseVSregion')
'''
Genres
'''

# Connect to the database
client = MongoClient()
db = client.Projet_Stat_L3.Users
# Retrieve all the data
users = db.find()
# We split the genres of a film, let's use the database
genres = ('Action', 'Adventure', 'Animation',
          'Children', 'Comedy', 'Crime', 'Documentary',
          'Drama', 'Fantasy', 'Film-Noir', 'Horror',
          'Musical', 'Mystery', 'Romance', 'Sci-Fi',
          'Thriller', 'War', 'Western')
# Get the values of each attribute
occupations = set(df['occupation'].get_values())
genders = set(df['gender'].get_values())
ageCategories = set(df['ageCategory'].get_values())
regions = set(df['region'].get_values())
# Create the contingency tables
M_genreVSoccupation = F_genreVSoccupation = pd.DataFrame(index = genres, columns = occupations).fillna(0)
M_genreVSage = F_genreVSage = pd.DataFrame(index = genres, columns = ageCategories).fillna(0)
M_genreVSregion = F_genreVSregion = pd.DataFrame(index = genres, columns = regions).fillna(0)
# Fill the contingency tables
for user in users:
    if user['gender'] == 'M':
        for film in user['ratings']:
            for genre in film['genres']:
                M_genreVSoccupation[user['occupation']][genre] += 1
                M_genreVSage[user['ageCategory']][genre] += 1
                M_genreVSregion[user['region']][genre] += 1
    else:
        for film in user['ratings']:
            for genre in film['genres']:
                F_genreVSoccupation[user['occupation']][genre] += 1
                F_genreVSage[user['ageCategory']][genre] += 1
                F_genreVSregion[user['region']][genre] += 1
# Save the dataframes
M_genreVSoccupation.to_csv('data/male/genreVSoccupation')
M_genreVSage.to_csv('data/male/genreVSage')
M_genreVSregion.to_csv('data/male/genreVSregion')
F_genreVSoccupation.to_csv('data/female/genreVSoccupation')
F_genreVSage.to_csv('data/female/genreVSage')
F_genreVSregion.to_csv('data/female/genreVSregion')
