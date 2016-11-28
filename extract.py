# Extract data from the csv files and organise them as tables in a databse.

import csv
import sqlite3

###############################################################################
###############              For data/movies.csv             ##################
###############################################################################

# values from "data/movies.csv" file stored as list of tuples in data
data = []
with open('data/movies.csv', 'rb') as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        data.append(tuple(row))

# delete the row that contains metadata (id, title, genre).
del data[0]

# movie_table stores the list of all the movies from "data/movies.csv"
# it stores tuples of the form (movie_id, movie_name).
movie_table = []
for item in data:
    movie_table.append((int(item[0]), item[1], ))

# this dictionary is used to find the corresponding id of the movie when the
# title of the movie is known.
movie_table_dict = {}
for item in movie_table:
    movie_table_dict[item[1]] = item[0]


# genre_table_temp used to extract all the unique genres from "data/movies.csv"
genre_table_temp = set()
for item in data:
    values = item[2].split('|')
    for value in values:
        genre_table_temp.add(value)


# genre_table stores the final list of all genres as a list of values
genre_table = list(genre_table_temp)


# movie_genre is a many-many relationship between movies and genre. Because
# each movie can have multiple genre and each genre can have multiple movies.

movie_genre = []
for item in data:
    # genre_list contains the index of all the genres of a particular movie.
    genre_list = [genre_table.index(value)+1 for value in item[2].split('|')]
    movie_index = movie_table_dict[item[1]]
    for value in genre_list:
        movie_genre.append((movie_index, value, ))


#### Creating the database

# establish a connection between the sqlite database
conn = sqlite3.connect('moviesdb.sqlite')
# this is used because of encoding issues between unicode and 8-bit stringvalue.
conn.text_factory = str
cur = conn.cursor()


# remove the tables if they already exist, so that we don't have to delete them
# manually each time this script is run.
cur.executescript('''
    DROP TABLE IF EXISTS Movies;
    DROP TABLE IF EXISTS Genres;
    DROP TABLE IF EXISTS Movies_Genres;
    CREATE TABLE Movies (
        id INTEGER NOT NULL PRIMARY KEY,
        name TEXT
    );
    CREATE TABLE Genres (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name TEXT
    );
    CREATE TABLE Movies_Genres (
        movie_id INTEGER NOT NULL,
        genre_id INTEGER NOT NULL
    );
''')


# insert data in the Movies (id, name) table
for movie in movie_table:
    cur.execute('''
        INSERT INTO Movies VALUES (?, ?)''', (movie[0], movie[1], ))

# save the changes made in the databse
conn.commit()

# insert data in the Genres (id, name) table
for genre in genre_table:
    cur.execute('''
        INSERT INTO Genres (name) VALUES (?)''', (genre, ))

# save the changes made in the databse
conn.commit()

# insert data in the Movies_Genres (movie_id, genre_id) table
for value in movie_genre:
    cur.execute('''
        INSERT INTO Movies_Genres (movie_id, genre_id) VALUES (?, ?)''',
        (value[0], value[1],))

# save the changes made in the databse
conn.commit()


###############################################################################
###############              For data/ratings.csv            ##################
###############################################################################


data = []
with open('data/ratings.csv', 'rb') as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        # ignored the 4th "timestamp" column, thus "[:3]".
        data.append(row[:3])


# delete the row that contains metadata (userId, movieId, rating, timestamp).
del data[0]

# convert the strings to the required format (user_id, movie_id, rating).
data = [(int(i[0]), int(i[1]), float(i[2]), ) for i in data]

# remove the tables if they already exist, so that we don't have to delete them
# manually each time this script is run.
cur.executescript('''
    DROP TABLE IF EXISTS Ratings;
    CREATE TABLE Ratings (
        user_id INTEGER NOT NULL,
        movie_id INTEGER NOT NULL,
        rating REAL NOT NULL
    );
''')

# insert data in Ratings (user_id, movie_id, rating) table.
for row in data:
    cur.execute('''
        INSERT INTO Ratings (user_id, movie_id, rating) VALUES (?, ?, ?)''',
        (row[0], row[1], row[2], ))

# commit the changes made in the database.
conn.commit()

# close the connection
conn.close()
