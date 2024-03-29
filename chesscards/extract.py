import csv
import sqlite3


def remove_duplicates(tuples):
    tmp = {}
    theme_index = 7
    for tuple in tuples:
        puzzle_id = tuple[0]
        if puzzle_id in tmp:
            tmp[puzzle_id][theme_index] = " ".join([tmp[puzzle_id][theme_index], (tuple[theme_index])])
        else:
            tmp[puzzle_id] = list(tuple)

    return tmp.values()


def sql(theme: str, min_rating: int, max_rating: int, tactics_per_motif: int):
    return f"""
            SELECT * FROM main.tactics 
            WHERE "Themes" IN ("{theme}") 
            AND "Rating" >= {min_rating} 
            AND "Rating" < {max_rating} 
            AND Popularity > 90 
            LIMIT {tactics_per_motif}
        """


if __name__ == "__main__":

    # Connect to the SQLite database
    conn = sqlite3.connect("lichess_db_puzzle.db")
    cursor = conn.cursor()

    # Define the SQL query
    themes = ["fork", "capturingDefender", "discoveredAttack", "intermezzo", "pin"]
    themes.extend(["zugzwang", "mateIn2", "doubleCheck"])
    # anastasia, arabian, boden
    themes.extend(
        [
            "anastasiaMate",
            "arabianMate",
            "bodenMate",
            "smotheredMate",
            "backRankMate",
            "doubleBishopMate",
            "dovetailMate",
            "hookMate",
        ]
    )
    themes.extend(["attackingF2F7", "promotion"])
    themes.extend(
        [
            "exposedKing",
            "hangingPiece",
            "skewer",
            "trappedPiece",
            "attraction",
            "clearance",
            "defensiveMove",
            "deflection",
            "interference",
            "quietMove",
            "xRayAttack",
            "trappedPiece",
            "sacrifice",
            "castling",
        ]
    )
    # '" Legal's mate
    # '" Damiano's mate ;/ Greco's mate
    # '" Lolli's mate
    # '" Blackburne's mate '" Pillsbury's mate
    rating = 1600
    print()

    rows = []
    column_names = []

    for theme in themes:
        query = sql(theme, rating, rating + 200, 10)

        # Execute the query and fetch the results
        cursor.execute(query)
        rows.extend(cursor.fetchall())

        # Get the column names (headers)
        column_names = [description[0] for description in cursor.description]

    rows = remove_duplicates(rows)

    # Write the headers and data to a CSV file
    with open("extract.csv", "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(column_names)  # Write the headers
        csvwriter.writerows(rows)  # Write the data

    # Close the database connection
    conn.close()
