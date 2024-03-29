import sqlite3

import pandas as pd


def prepare_sqlite(csv_fn: str, sqlite_fn: str):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_fn)

    # Connect to SQLite database
    conn = sqlite3.connect(sqlite_fn)

    # Write DataFrame to SQLite table
    df.to_sql("tactics", conn, if_exists="replace", index=False)

    # Split the 'Themes' column into a list of themes and explode it
    df_themes = df[["PuzzleId", "Themes"]]
    df_themes = df_themes.copy()
    df_themes["Themes"] = df["Themes"].str.split(" ")
    df_themes = df_themes.explode("Themes")

    # Write Themes to SQLite table
    df_themes.to_sql("themes", conn, if_exists="replace", index=False)

    cursor = conn.cursor()

    indices = {"tactics": ["puzzleid", "popularity", "rating", "nbplays"], "themes": ["puzzleid", "themes"]}

    for table, column_list in indices.items():
        for column in column_list:
            cursor.execute(f"CREATE INDEX idx_{table}_{column} ON {table}({column})")

    # Close the connection
    conn.close()


if __name__ == "__main__":
    prepare_sqlite("lichess_db_puzzle.csv", "lichess_db_puzzle.db")
    # prepare_sqlite("tests/data/sample.csv", "sample.db")
