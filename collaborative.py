import sqlite3
from sklearn.neighbors import NearestNeighbors
import numpy as np

n = int(raw_input('Enter the number of friends: '))
friends_list = [None]*n
for i in xrange(n):
    idd = int(raw_input())
    friends_list[i] = idd

friends_data = []

# connect with the database
conn = sqlite3.connect('moviesdb.sqlite')
cur = conn.cursor()

# get all the movies rated by each of your friends
for friend in friends_list:
    cur.execute('''
        SELECT user_id, movie_id, rating from Ratings WHERE user_id
        = (?)''', (friend, ))
    temp_data = cur.fetchall()
    for value in temp_data:
        friends_data.append(value)

q = 0
for value in friends_data:
    print q, value
    q += 1

training_data = [[value[2]] for value in friends_data]
print training_data
train = np.array(training_data)
nbrs = NearestNeighbors(n_neighbors=5)
nbrs.fit(train)
indices = nbrs.kneighbors([[0], [5]], n_neighbors=5, return_distance=False)

print '---------------------------------'
for index in indices:
    for i in index:
        print friends_data[i]
