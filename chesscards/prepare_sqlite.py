import sqlite3

import pandas as pd


def prepare_sqlite(csv_fn: str, sqlite_fn: str):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_fn)

    # Split the 'Themes' column into a list of themes and explode it
    df["Themes"] = df["Themes"].str.split(" ")
    df = df.explode("Themes")

    # Connect to SQLite database
    conn = sqlite3.connect(sqlite_fn)

    # Write DataFrame to SQLite table
    df.to_sql("tactics", conn, if_exists="replace", index=False)

    # TODO create indices for
    # themes
    # rating

    # Close the connection
    conn.close()


if __name__ == "__main__":
    prepare_sqlite("lichess_db_puzzle.csv", "lichess_db_puzzle.db")
