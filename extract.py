# Extract data from the csv files and organise them as tables in a databse.

import csv

# Values from "data/movies.csv" file stored as list of tuples in data
data = []
with open('data/movies.csv', 'rb') as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        data.append(tuple(row))

"""
for item in data[:60]:
    print item
"""

# movie_table stores the list of all the movies from "data/movies.csv"
movie_table = []
for item in data[1:]:
    movie_table.append(item[1])

"""
for item in movie_table:
    print item
print len(movie_table)
"""

# genre_table_temp used to extract all the unique genres from "data/movies.csv"
genre_table_temp = set()
for item in data:
    values = item[2].split('|')
    for value in values:
        genre_table_temp.add(value)

# genre_table stores the final list of all genres as a list of values
genre_table = []
for item in genre_table_temp:
    genre_table.append(item)

"""
for item in genre_table:
    print item
"""

# movie_genre is a many-many relationship between movies and genre. Because
# each movie can have multiple genre and each genre can have multiple movies.
movie_genre = []
movie_genre_temp = []
for item in data[1:]:
    movie_genre_temp.append((item[1], item[2].split('|'), ))

for item in movie_genre_temp:
    genre_list = []
    for value in item[1]:
        genre_list.append(genre_table.index(value)+1)
    movie_index = movie_table.index(item[0])+1
    for value in genre_list:
        movie_genre.append((movie_index, value, ))


"""
for item in movie_genre:
    print item
"""

#### Creating the database

import sqlite3

# establish a connection between the sqlite database
conn = sqlite3.connect('moviesdb.sqlite')
# this is used because of encoding issues between unicode and 8-bit stringvalue.
conn.text_factory = str
cur = conn.cursor()


# Remove the tables if they already exist, so that we don't have to delete them
# manually each time this script is run.
cur.executescript('''
    DROP TABLE IF EXISTS Movies;
    DROP TABLE IF EXISTS Genres;
    DROP TABLE IF EXISTS Movies_Genres;
    CREATE TABLE Movies (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
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


# Insert data in the Movies (id, name) table
for movie in movie_table:
    cur.execute('''
        INSERT INTO Movies (name) VALUES (?)''', (movie, ))

# save the changes made in the databse
conn.commit()

# Insert data in the Genres (id, name) table
for genre in genre_table:
    cur.execute('''
        INSERT INTO Genres (name) VALUES (?)''', (genre, ))

# save the changes made in the databse
conn.commit()

# Insert data in the Movies_Genres (movie_id, genre_id) table
for value in movie_genre:
    cur.execute('''
        INSERT INTO Movies_Genres (movie_id, genre_id) VALUES (?, ?)''',
        (value[0], value[1],))

# save the changes made in the databse
conn.commit()

# close the connection
conn.close()
