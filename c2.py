import sqlite3
from sklearn.neighbors import NearestNeighbors
import numpy as np

conn = sqlite3.connect('moviesdb2.sqlite')
cur = conn.cursor()

print 'Enter the movie id: '
movie_id = int(raw_input())
print 'Enter the rating: '
rating = int(raw_input())

genres_list = []
cur.execute('SELECT genre_id FROM Movies_Genres WHERE movie_id = (?)', (movie_id, ))
temp = cur.fetchall()
print temp
