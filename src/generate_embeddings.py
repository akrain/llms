import pickle

import openai_client
import pandas as pd
import sqlite3
import os

from constants import DB_FILENAME, COMBINED, EMBEDDING



def read_data():
    df = pd.read_csv("../data/imdb_top_1000.csv")
    print(df.head())
    return df


def save_data(df):
    if os.path.exists(DB_FILENAME):
        os.remove(DB_FILENAME)

    # Connect to database
    conn = sqlite3.connect(DB_FILENAME)
    df.to_sql("imdb", conn)


def generate_embeddings():
    df = read_data()
    df[COMBINED] = ("Title: " + df["Series_Title"]
                    + " Genre: " + df["Genre"]
                    + " Summary: " + df["Overview"]
                    + " Director: " + df["Director"]
                    + " Actor: " + df["Star1"]
                    + " Actor: " + df["Star2"]
                    + " Actor: " + df["Star3"]
                    + " Actor: " + df["Star4"])
    movies_combined = df[COMBINED].to_list()
    response = openai_client.create_embeddings(movies_combined)
    df[EMBEDDING] = [item.embedding for item in response.data]
    df[EMBEDDING] = df[EMBEDDING].apply(pickle.dumps)
    save_data(df)

generate_embeddings()