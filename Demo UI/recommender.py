from scipy import optimize
import pandas as pd
import numpy as np


def download_y_movies():
    """ Reads the y matrix from the y_movies csv file.

    Returns:
    y (numpy array): y matrix that was read from the file.

    """

    y = pd.read_csv('data/y_movies.csv').to_numpy()
    return y


def download_y_books():
    """ Reads the y matrix from the y_books csv file.

    Returns:
    y (numpy array): y matrix that was read from the file.

    """

    y = pd.read_csv('data/y_books.csv').to_numpy()
    return y


def download_y_songs():
    """ Reads the y matrix from the y_songs csv file.

    Returns:
    y (numpy array): y matrix that was read from the file.

    """

    y = pd.read_csv('data/y_songs.csv').to_numpy()
    return y


def upload_y_movies(y):
    """ Saves the y matrix to the y_movies csv file.

    Parameters:
    y (numpy array): Matrix to be saved to the csv file.

    """

    pd.DataFrame(y).to_csv('data/y_movies.csv', index=False)


def upload_y_books(y):
    """ Saves the y matrix to the y_books csv file.

    Parameters:
    y (numpy array): Matrix to be saved to the csv file.

    """

    pd.DataFrame(y).to_csv('data/y_books.csv', index=False)


def upload_y_songs(y):
    """ Saves the y matrix to the y_songs csv file.

    Parameters:
    y (numpy array): Matrix to be saved to the csv file.

    """

    pd.DataFrame(y).to_csv('data/y_songs.csv', index=False)


def return_features():
    """ Returns the number of features needed for training.

    Returns:
    n (int): Number of features that is to be returned.

    """

    n = 11
    return n


def mean_normal(y, r):
    """ Normalizes the values of y and r.

    Parameters:
    y (numpy array): The matrix to be normalized.
    r (numpy array): Helper matrix.

    Returns:
    temp*r (numpy array): Normalized y matrix.
    yMean (numpy array): Mean vector of the y matrix

    """

    temp = np.zeros(y.shape, dtype=float)
    yMean = np.zeros((y.shape[0], 1), dtype=float)
    for i in range(len(r)):
        mean = sum(y[i]) / sum(r[i])

        temp[i] = y[i] - mean
        yMean[i] = mean
    return temp * r, yMean


def f(initial_theta, *args):
    """ Calculates the cost.

    Parameters:
    initial_theta (numpy array): Initial value of the parameters.
    *args: Any other set of arguments required.

    Returns:
    J (float): Calculated cost.

    """

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
    """ Calculates the gradients.

    Paramters:
    initial_theta (numpy array): Initial value of the parameters.
    *args: Any other set of arguments required.

    Returns:
    rolled_up_grads (numpy array): Calculated vector of gradients.

    """
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


def rate(item_id, user_id, y, rating):
    """ Updates the y matrix according to a given rating.

    Parameters:
    item_id (int): ID of the item to be rated.
    user_id (int): ID of the user who is rating the item.
    rating (int): Rating given to the item by the user.

    Returns:
    y (numpy array): Updated numpy array.

    """

    y[item_id, user_id] = rating
    return y


def filter_content_movies(user_mood, suggested_content_dict):
    """ Filters the content dictionary of movies based on a mood.

    Parameters:
    user_mood (str): Mood based on which the dictionary is to be filtered.
    suggested_content_dict (dictionary): The dictionary based on which the content is to be filtered.

    """

    df = pd.read_csv('data/movie_ids.csv')

    # filters the dataframe based on user_mood and user_likes dictionary
    filt = (df.apply(lambda row: user_mood in row["mood"], axis=1)) & (df['id'].isin(suggested_content_dict.keys()))
    df_filtered = df[["id", "name"]][filt]

    # filtered dictionary that has to be returned
    mood_filtered_dict = dict()
    mood_filtered_dict = df_filtered.set_index('id').T.to_dict('records')[0]
    return mood_filtered_dict


def filter_content_books(user_mood, suggested_content_dict):
    """ Filters the content dictionary of books based on a mood.

    Parameters:
    user_mood (str): Mood based on which the dictionary is to be filtered.
    suggested_content_dict (dictionary): The dictionary based on which the content is to be filtered.

    """

    df = pd.read_csv('data/book_ids.csv')

    # filters the dataframe based on user_mood and user_likes dictionary
    filt = (df.apply(lambda row: user_mood in row["mood"], axis=1)) & (df['id'].isin(suggested_content_dict.keys()))
    df_filtered = df[["id", "name"]][filt]

    # filtered dictionary that has to be returned
    mood_filtered_dict = dict()
    mood_filtered_dict = df_filtered.set_index('id').T.to_dict('records')[0]
    return mood_filtered_dict


def filter_content_songs(user_mood, suggested_content_dict):
    """ Filters the content dictionary of songs based on a mood.

    Parameters:
    user_mood (str): Mood based on which the dictionary is to be filtered.
    suggested_content_dict (dictionary): The dictionary based on which the content is to be filtered.

    """

    df = pd.read_csv('data/song_ids.csv')

    # filters the dataframe based on user_mood and user_likes dictionary
    filt = (df.apply(lambda row: user_mood in row["mood"], axis=1)) & (df['id'].isin(suggested_content_dict.keys()))
    df_filtered = df[["id", "name"]][filt]

    # filtered dictionary that has to be returned
    mood_filtered_dict = dict()
    mood_filtered_dict = df_filtered.set_index('id').T.to_dict('records')[0]
    return mood_filtered_dict


def create_movies_dict():
    """ Creates a dictionary out of the list of movies in the movie_ids csv file.

    Returns:
    demo_dict (dictionary): Dictionary containing the id and names of all the movies in the file.

    """

    movieList = pd.read_csv('data/movie_ids.csv')["name"].to_list()
    demo_dict = dict()
    for i in range(len(movieList)):
        demo_dict[movieList[i]] = i
    return demo_dict


def create_songs_dict():
    """ Creates a dictionary out of the list of songs in the song_ids csv file.

    Returns:
    demo_dict (dictionary): Dictionary containing the id and names of all the songs in the file.

    """

    songList = pd.read_csv('data/song_ids.csv')["name"].to_list()
    demo_dict = dict()
    for i in range(len(songList)):
        demo_dict[songList[i]] = i
    return demo_dict


def create_books_dict():
    """ Creates a dictionary out of the list of books in the book_ids csv file.

    Returns:
    demo_dict (dictionary): Dictionary containing the id and names of all the books in the file.

    """

    bookList = pd.read_csv('data/book_ids.csv')["name"].to_list()
    demo_dict = dict()
    for i in range(len(bookList)):
        demo_dict[bookList[i]] = i
    return demo_dict


def recommend(y_movies_df, merged, moviemat, movie_dict, movies_rated, movies_liked, filt_good_rating_count, filt_rating_count):
    """ Generates the dictionary of recommendations for the user.

    Parameters:
    y_movies_df (dataframe): Dataframe calculated from the y matrix.
    merged (dataframe): Merged table containing all the users' ratings for all items.
    movie_dict (dictionary): Dictionary containing the id and names of all items (not just movies).
    movies_rated (int): Number of items of a certain content rated by the user (not just movies).
    movies_liked (int): Number of items of a certain content liked (rated equal of above 3 stars)
                        by the user (not just movies).
    filt_good_rating_count: Filtered rating count of the liked items (not just movies).
    filt_rating_count: Filtered rating count of the rated items (not just movies).

    Returns:
    suggestion (dictionary): Dictionary containing the suggestions for a user.

    """

    # create the average rating dataframe
    ratings = pd.DataFrame(merged.groupby(['id', 'name'])['rating'].mean()).reset_index().sort_values('rating', ascending=False)

    # finds out if user has rated any movies or not
    if movies_rated == 0:
        # returns a dictionary of the 25 top rated movies
        return ratings[['id', 'name']].head(25).set_index('id').T.to_dict('records')[0]
    else:
        if movies_liked >= 4:
            # selects 4 random samples from movies rated more than 3 stars
            liked_movie_sample = merged[filt_good_rating_count].sample(n=4)['name']
            suggestion_df = list()
            suggestion = dict()

            for i in range(4):
                suggestion_df.append(find_correlation(liked_movie_sample.iloc[i], moviemat, False).reset_index())
            for i in range(4):
                movie_count = 0
                while movie_count < 6:
                    selected_movie = suggestion_df[i].sample(n=1)['name'].values[0]
                    if selected_movie not in suggestion.values():
                        suggestion[movie_dict[selected_movie]] = selected_movie
                        movie_count += 1
            return suggestion
        elif movies_liked > 0:
            # selects all the movies that are rated more than 3 stars
            liked_movie_sample = merged[filt_good_rating_count]['name']
            suggestion_df = list()
            suggestion = dict()

            for i in range(movies_liked):
                suggestion_df.append(find_correlation(liked_movie_sample.iloc[i], moviemat, False).reset_index())
            for i in range(movies_liked):
                movie_count = 0
                while movie_count < 24 / movies_liked:
                    selected_movie = suggestion_df[i].sample(n=1)['name'].values[0]
                    if selected_movie not in suggestion.values():
                        suggestion[movie_dict[selected_movie]] = selected_movie
                        movie_count += 1
            return suggestion
        else:
            liked_movie_sample = merged[filt_rating_count].sample(n=1)['name']
            suggestion = dict()
            selected_movie = find_correlation(liked_movie_sample.iloc[0], moviemat, True).reset_index().sample(n=24)['name']
            for i in range(24):
                suggestion[movie_dict[selected_movie.values[i]]] = selected_movie.values[i]
            return suggestion


def find_correlation(name, moviemat, asc):
    """ Calculates the correlation matrix of a certain item.

    Parameters:
    name (str): Name of the item for which the correlation is to be calculated.
    moviemat (dataframe): Pivot table to find the correlation.
    asc (bool): True if the sorting is to be done in ascending order.

    Returns:
    corr_movie.sort_values('Correlation', ascending=asc).iloc[1:27] (dataframe):
    Dataframe containing the correlated items to the given item.

    """

    movie_ratings = moviemat[name]
    similar_to_movie = moviemat.corrwith(movie_ratings)
    corr_movie = pd.DataFrame(similar_to_movie, columns=['Correlation'])
    corr_movie.dropna(inplace=True)
    return corr_movie.sort_values('Correlation', ascending=asc).iloc[1:27]
