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
