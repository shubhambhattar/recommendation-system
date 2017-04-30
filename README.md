# recommendation-system
Recommendation Systems using Machine Learning

## extract2.py
The data is extracted from CSV files. The following tables are formed:

### Movies

Attributes:

- id: Movie id
- name: Movie name
- rating: Average rating of that movie

Snapshot of data:

| id    | name                  | rating    |
|-------|-----------------------|-----------|
| 2959  | Fight Club (1999)     | 4.17822   |
| 48780 | Prestige, The (2006)  | 4.125     |
| 74458 | Shutter Island (2010) | 3.97412   |
| ...   | ...                   | ...       |

### Genres

Attributes:

- id: Genre id
- name: Genre name

Snapshot of data:

| id    | name      |
|-------|-----------|
| 1     | Mystery   |
| 2     | Drama     |
| 19    | Thriller  |
| ...   | ...       |

### Movies_Genres

Attributes:

- movie_id: movie id
- genre_id: genre id

Snapshot of data:

| movie_id  | genre_id  |
|-----------|-----------|
| 2959      | 14        |
| 2959      | 7         |
| 2959      | 2         |
| 2959      | 19        |
| 48780     | 2         |
| 48780     | 1         |
| 48780     | 4         |
| 48780     | 19        |
| ...       | ...       |


### Ratings

Attributes:

- user_id: id of the user who has rated the movies
- movie_id: id of the movie that the user has rated
- rating: rating given by `user_id` to `movie_id`

Snapshot of data:

| user_id   | movie_id  | rating    |
|-----------|-----------|-----------|
| 1         | 31        | 2.5       |
| 1         | 1029      | 3.0       |
| 2         | 17        | 5.0       |
| ...       | ...       | ...       |


## content.py

This is the content based filtering approach. The following things are done:

1. Get a list of favourite movies from the user.
2. Get the ratings of all the movies liked by the user.
3. Make an exhaustive Genre set that encompasses all the favourite movies.
4. Build a movie list that has those genres. Sort the movies in such a way that the movie with most genre match will be on top.
5. Get the top 50 movies from the above list and apply k-NN to get top `k` movies.
6. Present the names of the `k` movies in the end result.
