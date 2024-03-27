import sqlite3
import csv

if __name__ == '__main__':

    # Connect to the SQLite database
    conn = sqlite3.connect('lichess_db_puzzle.db')
    cursor = conn.cursor()

    # Define the SQL query
    query = """
    SELECT * FROM main.tactics 
    WHERE "Themes" LIKE "%fork%" 
    AND "Rating" > 1000 
    AND "Rating" < 1200 
    AND Popularity > 90 
    LIMIT 10;
    """

    # Execute the query and fetch the results
    cursor.execute(query)
    rows = cursor.fetchall()

    # Get the column names (headers)
    column_names = [description[0] for description in cursor.description]

    # Write the headers and data to a CSV file
    with open('extract.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(column_names) # Write the headers
        csvwriter.writerows(rows) # Write the data

    # Close the database connection
    conn.close()
