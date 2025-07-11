import pickle

import numpy as np

from openai_client import create_embeddings
import pandas as pd
from pandas.core.frame import DataFrame
import sqlite3

from llms.constants import DB_FILENAME, EMBEDDING, SERIES_TITLE, RELEASED_YEAR, GENRE, IMDB_RATING, OVERVIEW, SIMILARITY, EXIT_CMD


def main():
    df = load_data()
    df[EMBEDDING] = df[EMBEDDING].apply(pickle.loads)
    
    while True:
        query = input("Enter your search query: ( /exit to Exit").strip()
        if query == EXIT_CMD:
            break
        else:
            search(query, df)


def search(query: str, df: DataFrame):
    query_embedding = create_embeddings([query]).data[0].embedding
    df[SIMILARITY] = df[EMBEDDING].apply(lambda x: cosine_similarity(x, query_embedding))
    result_df = df.sort_values(SIMILARITY, ascending=False)[:10]
    print_df_rows(result_df)



def load_data() -> DataFrame:
    conn = sqlite3.connect(DB_FILENAME)
    return pd.read_sql_query("SELECT * FROM imdb", conn)


def cosine_similarity(a, b):
    return np.dot(a,b) / (np.linalg.norm(a) * np.linalg.norm(b))


def print_df_rows(df: DataFrame):
    columns = [SERIES_TITLE, RELEASED_YEAR, GENRE, IMDB_RATING, OVERVIEW, SIMILARITY]
    existing_columns = [col for col in columns if col in df.columns]
    
    # Print header
    for col in existing_columns:
        print(f"{col:20}", end=" | ")
    print()
    print("-" * (21 * len(existing_columns)))
    
    # Print rows
    for index, row in df.iterrows():
        for col in existing_columns:
            value = str(row[col])
            if len(value) > 20:
                value = value[:17] + "..."
            print(f"{value:20}", end=" | ")
        print()

if __name__ == "__main__":
    main()