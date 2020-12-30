from scipy import optimize
import pandas as pd
import numpy as np


# downloads the y, r matrices of the movies and return the corresponding numpy arrays
def download_yr_movies():
    # extracting the y and r matrices from the csv files
    r = pd.read_csv('data/r_movies.csv').to_numpy()
    y = pd.read_csv('data/y_movies.csv').to_numpy()

    return y, r


# downloads the y, r matrices of the books and return the corresponding numpy arrays
def download_yr_books():
    # extracting the y and r matrices from the csv files
    r = pd.read_csv('data/r_books.csv').to_numpy()
    y = pd.read_csv('data/y_books.csv').to_numpy()

    return y, r


# downloads the y, r matrices of the songs and return the corresponding numpy arrays
def download_yr_songs():
    # extracting the y and r matrices from the csv files
    r = pd.read_csv('data/r_songs.csv').to_numpy()
    y = pd.read_csv('data/y_songs.csv').to_numpy()

    return y, r


def upload_yr_movies(y, r):
    # converting numpy array to csv file
    pd.DataFrame(r).to_csv('data/r_movies.csv', index=False)
    pd.DataFrame(y).to_csv('data/y_movies.csv', index=False)


def upload_yr_books(y, r):
    # converting numpy array to csv file
    pd.DataFrame(r).to_csv('data/r_books.csv', index=False)
    pd.DataFrame(y).to_csv('data/y_books.csv', index=False)


def upload_yr_songs(y, r):
    # converting numpy array to csv file
    pd.DataFrame(r).to_csv('data/r_songs.csv', index=False)
    pd.DataFrame(y).to_csv('data/y_songs.csv', index=False)


def return_features():
    # returns the number of features
    n = 11
    return n


def mean_normal(y, r):
    # function to normalize the dataset
    temp = np.zeros(y.shape, dtype=float)
    yMean = np.zeros((y.shape[0], 1), dtype=float)
    for i in range(len(r)):
        mean = sum(y[i]) / sum(r[i])

        temp[i] = y[i] - mean
        yMean[i] = mean
    return temp * r, yMean


def f(initial_theta, *args):
    # function for calculating the cost
    # preparing required variables
    yPrime, Lambda = args
    r = (yPrime != 0) * 1
    n = return_features()
    no_of_movies = yPrime.shape[0]
    no_of_users = yPrime.shape[1]

    # mathematical calculations for computing the cost
    X, Theta = initial_theta[:no_of_movies * n, ], initial_theta[no_of_movies * n:, ]
    X = np.reshape(X, (no_of_movies, n))
    Theta = np.reshape(Theta, (no_of_users, n))
    Error = ((X.dot(np.transpose(Theta))) - yPrime).copy()
    J = (.5) * ((Error * Error) * r).sum()
    Reg_term_theta = (Lambda / 2) * ((Theta * Theta).sum())
    Reg_term_X = (Lambda / 2) * ((X * X).sum())
    J = J + Reg_term_theta + Reg_term_X
    return J


def grads(initial_theta, *args):
    # function for calculating the gradients
    # preparing required variables
    yPrime, Lambda = args
    r = (yPrime != 0) * 1
    n = return_features()
    no_of_movies = yPrime.shape[0]
    no_of_users = yPrime.shape[1]

    # mathematical calculations for calculating the gradients
    X, Theta = initial_theta[:no_of_movies * n, ], initial_theta[no_of_movies * n:, ]
    X = np.reshape(X, (no_of_movies, n))
    Theta = np.reshape(Theta, (no_of_users, n))
    Error = ((X.dot(np.transpose(Theta))) - yPrime).copy()
    X_grad = ((Error * r).dot(Theta) + Lambda * X).copy()
    Theta_grad = ((np.transpose(Error * r)).dot(X) + Lambda * Theta).copy()
    rolled_up_grads = np.concatenate((X_grad, Theta_grad), axis=None)
    return rolled_up_grads


def recommend_movies(userID, y, r):
    # creating the movie list from the movie_ids csv file
    movieList = pd.read_csv('data/movie_ids.csv')["name"].to_list()
    n = return_features()  # retrieving the number of features

    # creating the user's rating vector and r vector
    my_ratings = np.zeros((y.shape[0], 1), dtype=float)
    temp = y[:, userID]
    my_ratings = temp.reshape((y.shape[0], 1))
    my_r = (my_ratings != 0) * 1

    Lambda = 10  # regularization parameter
    n = 11  # total number of features for the movies
    no_of_movies = y.shape[0]  # total number of movies
    no_of_users = y.shape[1]   # total number of users

    # calculating normalized y values
    yPrime, yMean = mean_normal(y, r)

    # initializing the machine learning matrices
    X = np.random.rand(no_of_movies, n)
    Theta = np.random.rand(no_of_users, n)
    initial_theta = np.concatenate((X, Theta), axis=None)
    args = (yPrime, Lambda)

    # setting options for the optimizer function
    opts = {'maxiter': 30,    # non-default value.
            'disp': True,    # non-default value.
            'gtol': 1e-5,    # default value.
            'norm': np.inf,  # default value.
            'eps': 1.4901161193847656e-08}  # default value.

    # training the model
    optimal_rolled_theta = optimize.minimize(f, initial_theta, jac=grads, args=args,
                                             method='CG', options=opts)

    print(optimal_rolled_theta.x)

    # Converting the matrices to their original shape
    X, Theta = optimal_rolled_theta.x[:no_of_movies * n, ], optimal_rolled_theta.x[no_of_movies * n:, ]
    X = np.reshape(X, (no_of_movies, n))
    Theta = np.reshape(Theta, (no_of_users, n))

    # calculating the normalized predictions
    prediction = (X.dot(np.transpose(Theta))).copy()

    # calculating the actual predictions on a scale of 1.00 to 5.00
    actualPreds = np.zeros(yPrime.shape, dtype=float)
    for i in range(no_of_movies):
        temp = yMean[i]
        actualPreds[i] = prediction[i] + temp

    # predictions for the user
    my_preds = actualPreds[:, userID]

    # calculating the suggested movies for the user
    suggestedMovies = dict()  # contains the movie ids as key and ratings as values

    for i in range(no_of_movies):
        suggestedMovies[i] = my_preds[i]

    suggestedMovies = {k: v for k, v in sorted(suggestedMovies.items(), key=lambda item: item[1], reverse=True)}

    # dict to hold the top movies for the user
    suggested_movie_dict = dict()
    for key, item in suggestedMovies.items():
        if(my_r[key] == 1):  # so that already rated movies don't appear
            continue
        suggested_movie_dict[key] = movieList[key]

    return suggested_movie_dict


def recommend_books(userID, y, r):
    # creating the movie list from the movie_ids csv file
    movieList = pd.read_csv('data/book_ids.csv')["name"].to_list()
    n = return_features()  # retrieving the number of features

    # creating the user's rating vector and r vector
    my_ratings = np.zeros((y.shape[0], 1), dtype=float)
    temp = y[:, userID]
    my_ratings = temp.reshape((y.shape[0], 1))
    my_r = (my_ratings != 0) * 1

    Lambda = 10  # regularization parameter
    n = 11  # total number of features for the movies
    no_of_movies = y.shape[0]  # total number of movies
    no_of_users = y.shape[1]   # total number of users

    # calculating normalized y values
    yPrime, yMean = mean_normal(y, r)

    # initializing the machine learning matrices
    X = np.random.rand(no_of_movies, n)
    Theta = np.random.rand(no_of_users, n)
    initial_theta = np.concatenate((X, Theta), axis=None)
    args = (yPrime, Lambda)

    # setting options for the optimizer function
    opts = {'maxiter': 30,    # non-default value.
            'disp': True,    # non-default value.
            'gtol': 1e-5,    # default value.
            'norm': np.inf,  # default value.
            'eps': 1.4901161193847656e-08}  # default value.

    # training the model
    optimal_rolled_theta = optimize.minimize(f, initial_theta, jac=grads, args=args,
                                             method='CG', options=opts)

    print(optimal_rolled_theta.x)

    # Converting the matrices to their original shape
    X, Theta = optimal_rolled_theta.x[:no_of_movies * n, ], optimal_rolled_theta.x[no_of_movies * n:, ]
    X = np.reshape(X, (no_of_movies, n))
    Theta = np.reshape(Theta, (no_of_users, n))

    # calculating the normalized predictions
    prediction = (X.dot(np.transpose(Theta))).copy()

    # calculating the actual predictions on a scale of 1.00 to 5.00
    actualPreds = np.zeros(yPrime.shape, dtype=float)
    for i in range(no_of_movies):
        temp = yMean[i]
        actualPreds[i] = prediction[i] + temp

    # predictions for the user
    my_preds = actualPreds[:, userID]

    # calculating the suggested movies for the user
    suggestedMovies = dict()  # contains the movie ids as key and ratings as values

    for i in range(no_of_movies):
        suggestedMovies[i] = my_preds[i]

    suggestedMovies = {k: v for k, v in sorted(suggestedMovies.items(), key=lambda item: item[1], reverse=True)}

    # dict to hold the top movies for the user
    suggested_movie_dict = dict()
    for key, item in suggestedMovies.items():
        if(my_r[key] == 1):  # so that already rated movies don't appear
            continue
        suggested_movie_dict[key] = movieList[key]

    return suggested_movie_dict


def recommend_songs(userID, y, r):
    # creating the movie list from the movie_ids csv file
    movieList = pd.read_csv('data/song_ids.csv')["name"].to_list()
    n = return_features()  # retrieving the number of features

    # creating the user's rating vector and r vector
    my_ratings = np.zeros((y.shape[0], 1), dtype=float)
    temp = y[:, userID]
    my_ratings = temp.reshape((y.shape[0], 1))
    my_r = (my_ratings != 0) * 1

    Lambda = 10  # regularization parameter
    n = 11  # total number of features for the movies
    no_of_movies = y.shape[0]  # total number of movies
    no_of_users = y.shape[1]   # total number of users

    # calculating normalized y values
    yPrime, yMean = mean_normal(y, r)

    # initializing the machine learning matrices
    X = np.random.rand(no_of_movies, n)
    Theta = np.random.rand(no_of_users, n)
    initial_theta = np.concatenate((X, Theta), axis=None)
    args = (yPrime, Lambda)

    # setting options for the optimizer function
    opts = {'maxiter': 30,    # non-default value.
            'disp': True,    # non-default value.
            'gtol': 1e-5,    # default value.
            'norm': np.inf,  # default value.
            'eps': 1.4901161193847656e-08}  # default value.

    # training the model
    optimal_rolled_theta = optimize.minimize(f, initial_theta, jac=grads, args=args,
                                             method='CG', options=opts)

    print(optimal_rolled_theta.x)

    # Converting the matrices to their original shape
    X, Theta = optimal_rolled_theta.x[:no_of_movies * n, ], optimal_rolled_theta.x[no_of_movies * n:, ]
    X = np.reshape(X, (no_of_movies, n))
    Theta = np.reshape(Theta, (no_of_users, n))

    # calculating the normalized predictions
    prediction = (X.dot(np.transpose(Theta))).copy()

    # calculating the actual predictions on a scale of 1.00 to 5.00
    actualPreds = np.zeros(yPrime.shape, dtype=float)
    for i in range(no_of_movies):
        temp = yMean[i]
        actualPreds[i] = prediction[i] + temp

    # predictions for the user
    my_preds = actualPreds[:, userID]

    # calculating the suggested movies for the user
    suggestedMovies = dict()  # contains the movie ids as key and ratings as values

    for i in range(no_of_movies):
        suggestedMovies[i] = my_preds[i]

    suggestedMovies = {k: v for k, v in sorted(suggestedMovies.items(), key=lambda item: item[1], reverse=True)}

    # dict to hold the top movies for the user
    suggested_movie_dict = dict()
    for key, item in suggestedMovies.items():
        if(my_r[key] == 1):  # so that already rated movies don't appear
            continue
        suggested_movie_dict[key] = movieList[key]

    return suggested_movie_dict


def rate(item_id, user_id, y, r, rating):
    # allows user to rate certain items
    # updating y and r based on the user's rating on item_id
    y[item_id, user_id] = rating
    r = (y != 0) * 1
    return y, r


def filter_content_movies(user_mood, suggested_content_dict):
    df = pd.read_csv('data/movie_ids.csv')

    # filters the dataframe based on user_mood and user_likes dictionary
    filt = (df.apply(lambda row: user_mood in row["mood"], axis=1)) & (df['id'].isin(suggested_content_dict.keys()))
    df_filtered = df[["id", "name"]][filt]

    # filtered dictionary that has to be returned
    mood_filtered_dict = dict()
    mood_filtered_dict = df_filtered.set_index('id').T.to_dict('records')[0]
    return mood_filtered_dict


def filter_content_books(user_mood, suggested_content_dict):
    df = pd.read_csv('data/book_ids.csv')

    # filters the dataframe based on user_mood and user_likes dictionary
    filt = (df.apply(lambda row: user_mood in row["mood"], axis=1)) & (df['id'].isin(suggested_content_dict.keys()))
    df_filtered = df[["id", "name"]][filt]

    # filtered dictionary that has to be returned
    mood_filtered_dict = dict()
    mood_filtered_dict = df_filtered.set_index('id').T.to_dict('records')[0]
    return mood_filtered_dict


def filter_content_songs(user_mood, suggested_content_dict):
    df = pd.read_csv('data/song_ids.csv')

    # filters the dataframe based on user_mood and user_likes dictionary
    filt = (df.apply(lambda row: user_mood in row["mood"], axis=1)) & (df['id'].isin(suggested_content_dict.keys()))
    df_filtered = df[["id", "name"]][filt]

    # filtered dictionary that has to be returned
    mood_filtered_dict = dict()
    mood_filtered_dict = df_filtered.set_index('id').T.to_dict('records')[0]
    return mood_filtered_dict
