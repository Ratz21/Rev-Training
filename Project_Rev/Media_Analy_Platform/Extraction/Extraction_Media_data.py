"""
pathlib.Path is a modern, OS-independent way of handling file paths. Much cleaner than using ugly '../Dataset/Hbo-dataset/titles.csv' strings everywhere.
ROOT → the folder where your current script
ROOT.parent → the parent directory (Media_Analy_Platform).
This path logic ensures the code works even if you move the project to another computer — it doesn’t depend on your local desktop path.

"""

# section 1: extract--
import pandas as pd

# Read HBO titles dataset (adjust path if needed)
df = pd.read_csv("../Dataset/Hbo-dataset/titles.csv") # add double dot file reading . means current folder and .. means im currently in this folder go to the parent

# Check what you got
print("Total rows:", len(df))
print("Columns:", df.columns.tolist())
print(df.head(4))


# section 2 : transform--

#  1: drop duplicate rows
df = df.drop_duplicates()
print("after removing duplicates:", len(df))
print(df.duplicated().sum()) # to print total values if removed duplicates


# 2: Rename columns (keep them consistent)

df = df.rename(columns={
    'id': 'title_id',
    'name': 'title',
    'type': 'content_type',
    'release_year': 'release_year',
    'runtime': 'runtime',
    'genres': 'genres',
    'production_countries': 'production_countries',
    'imdb_id': 'imdb_id',
    'tmdb_id': 'tmdb_id',
    'imdb_score': 'imdb_score',
    'imdb_votes': 'imdb_votes',
    'tmdb_score': 'tmdb_score',
    'tmdb_popularity': 'tmdb_popularity',
    'description': 'description',
    'number_of_seasons': 'seasons',
})

print("Renamed columns:", df.columns.tolist())


# 3 Handle missing values
# filling missing scores with 0 or mark missing years as nan

df['imdb_score'] = pd.to_numeric(df.get('imdb_score'),errors='coerce').fillna(0) #df.get -> retrieves colmn name , pd.to_numeric -> converts value in that series to numeric type int or float
df['tmdb_score'] = pd.to_numeric(df.get('tmdb_score'),errors='coerce').fillna(0) # .fillna replaces all nan values in the result with 0


# 4 Fix runtime (turn text to numbers)

df['runtime'] = pd.to_numeric(df['runtime'], errors='coerce') #elects the column called runtime_minutes from ur df , errors='coerce' If a value can’t be converted to a number, don’t throw an error just turn it into NaN


#5  small clean up remove spaces from titles
df['title'] = df['title'].str.strip() # removes accidental spaces

print("Data types after cleanup:")
print(df.dtypes)

# section 3: Load to BigQuery

from google.cloud import bigquery

