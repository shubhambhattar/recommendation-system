import sqlite3, math

# calculate Pearson's coefficient using the formula:
#                  sum[(X_i - X_mean)(Y_i - Y_mean)]
#  r(X, Y) = -------------------------------------------------
#            sqrt(sum((X_i - X_mean)^2)*sum((Y_i - Y_mean)^2))

# `common_data` is of the format `[movie_id, user1_rating, user2_rating]`
def calculate(common_data):

    user1_mean = sum([x[1] for x in common_data])/len(common_data)
    user2_mean = sum([x[2] for x in common_data])/len(common_data)
    num, den1, den2 = 0.0, 0.0, 0.0

    for item in common_data:
        num += (item[1] - user1_mean)*(item[2] - user2_mean)
        den1 += (item[1] - user1_mean)**2
        den2 += (item[2] - user2_mean)**2

    if den1 != 0 and den2 != 0:
        return float(num)/(math.sqrt(den1)*math.sqrt(den2))

    # -10 indicates that the coefficient was not calculated and this
    # computation is skipped (because denominator is 0)
    return -10


# find the common movies between `user1` and `user2`
def pearson(user1, user2):
    common_data = []
    for i in user1:
        for j in user2:
            if i[0] == j[0]:
                common_data.append((i[0], i[1], j[1], ))

    # skip if there are no common movies between the two users
    if common_data == []:
        return -10, -1

    coefficient = calculate(common_data)
    if coefficient == -10:
        return -1, -1

    # return the pearson's coefficient value and the number of common movies
    return round(coefficient, 5), len(common_data)


# comparator function for sorting the user_coef list
# It is such that (0.9, 17) will be ranked higher than values like (1.0, 2)
def cmp(a):
    return a[0]*a[1]/20.0


# Get the number of movies from the user
print 'Enter the number of movies that you like:'
mov_no = int(raw_input())
mov_id = [None]*mov_no

# Input the movie_id and the user rating out of 5.0 (minimum 0.5)
print 'Enter the movie id and movie ratings out of 5.0 (minimum rating: 0.5)'
for i in xrange(mov_no):
    a, b = map(float, raw_input().split())
    mov_id[i] = (int(a), b, )

# for i in mov_id:
#     print i

# establish a connection with the sqlite database
conn = sqlite3.connect('moviesdb2.sqlite')
cur = conn.cursor()

# number of users in the database is 670
users = 670

# this list will store the value of Pearson's coefficient for different users.
# `user_coeff` is of the format `[coefficient, len(common_movies), user_id]`
user_coeff = []
for i in xrange(2, users):
    cur.execute('SELECT movie_id, rating FROM Ratings WHERE user_id = (?)', (i, ))
    user_data = cur.fetchall()

    coeff, n = pearson(mov_id, user_data)

    # n = -1 implies that Pearson's coefficient was not calculated
    # coeff < 0.2 is ignored because the correlation is small
    # n < 5 implies that there are not a lot of common movies between two users.
    if n == -1 or coeff < 0.2 or n < 5:
        continue

    user_coeff.append((coeff, n, i, ))

# sort the user_coeff list such that the best results are on the top
user_coeff = sorted(user_coeff, key=cmp, reverse=True)
for item in user_coeff:
    print item

# create an exhaustive list of movies for which prediction will be made
movies_list = []
for item in user_coeff[:5]:
    cur.execute('SELECT movie_id, rating FROM Ratings WHERE user_id = (?)', (item[2], ))
    temp = cur.fetchall()

    # filter out the common movies between the users
    for i in temp:
        flag = False
        for j in mov_id:
            if i[0] == j[0]:
                flag = True
                break
        if flag == False:
            movies_list.append((i[0], i[1], item[2], ))
