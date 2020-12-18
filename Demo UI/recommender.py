from scipy import optimize
import pandas as pd
import numpy as np

# downloads the y, r matrices of the movies and return the corresponding numpy arrays
def download_yr_movies():
    # extracting the y and r matrices from the csv files
    r = pd.read_csv('data/r_movies.csv').to_numpy()
    y = pd.read_csv('data/y_movies.csv').to_numpy()

    return y, r