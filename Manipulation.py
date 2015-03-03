from pymongo import MongoClient
import pandas as pd

# Connect to the database
client = MongoClient()
db = client.Projet_Stat_L3.Users
# Retrieve all the data
data = db.find()
# Open the CSV file with the categorized data
df = pd.read_csv('data/categorized')

# Build the contingency tables
ageVSrelease = pd.crosstab(df.ageCategory, df.releaseDecade)




    
