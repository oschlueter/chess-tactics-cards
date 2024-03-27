import pandas as pd
import sqlite3

if __name__ == '__main__':
    # Read the CSV file into a DataFrame
    df = pd.read_csv('lichess_db_puzzle.csv')

    # Split the 'Themes' column into a list of themes and explode it
    df['Themes'] = df['Themes'].str.split(' ')
    df = df.explode('Themes')

    # Connect to SQLite database
    conn = sqlite3.connect('lichess_db_puzzle.db')

    # Write DataFrame to SQLite table
    df.to_sql('tactics', conn, if_exists='replace', index=False)

    # TODO create indices for
    # themes
    # rating

    # Close the connection
    conn.close()
