import csv
import sqlite3
import random


def remove_duplicates(tuples):
    tmp = {}
    theme_index = 7
    for tuple in tuples:
        puzzle_id = tuple[0]
        if puzzle_id in tmp:
            tmp[puzzle_id][theme_index] = " ".join([tmp[puzzle_id][theme_index], (tuple[theme_index])])
        else:
            tmp[puzzle_id] = list(tuple)

    return list(tmp.values())


def sql(theme: str, min_rating: int, max_rating: int, popularity: int, tactics_per_motif: int):
    return f"""
            SELECT * FROM main.tactics 
            WHERE "Themes" IN ("{theme}") 
            AND "Rating" >= {min_rating} 
            AND "Rating" < {max_rating} 
            AND Popularity >= {popularity}
            LIMIT {tactics_per_motif}
        """


def extract_tactics(database_fn: str, min_rating: int, max_rating: int, popularity: int, themes: [str], tactics_per_theme: int, extract_file: str = 'extract.csv'):
    # Connect to the SQLite database
    conn = sqlite3.connect(database_fn)
    cursor = conn.cursor()
    rows = []
    column_names = []
    for theme in themes:
        query = sql(theme, min_rating, max_rating, popularity, tactics_per_theme)
        cursor.execute(query)
        rows.extend(cursor.fetchall())

        # Get the column names (headers)
        column_names = [description[0] for description in cursor.description]

    rows = remove_duplicates(rows)

    random.shuffle(rows)

    # Write the headers and data to a CSV file
    with open(extract_file, "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(column_names)  # Write the headers
        csvwriter.writerows(rows)  # Write the data

    # Close the database connection
    conn.close()


if __name__ == "__main__":
    r = 1600
    db_fn = "lichess_db_puzzle.db"

    t = ["fork", "capturingDefender", "discoveredAttack", "intermezzo", "pin"]
    t.extend(["zugzwang", "mateIn2", "doubleCheck"])
    # anastasia, arabian, boden
    t.extend(
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
    t.extend(["attackingF2F7", "promotion"])
    t.extend(
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

    extract_tactics(db_fn, r, r + 200, 90, t, 10)
