import csv
import sqlite3
import random


def sql(theme: str, min_rating: int, max_rating: int, popularity: int, tactics_per_motif: int):
    return f"""
            SELECT tactics.* FROM tactics, themes
            WHERE tactics.PuzzleId = themes.PuzzleId
            AND themes.themes = '{theme}'
            AND tactics.rating >= {min_rating}
            AND tactics.rating < {max_rating}
            AND tactics.popularity >= {popularity}
            AND tactics.PuzzleId NOT IN
                (
                    SELECT puzzleid
                    FROM themes
                    WHERE themes IN ('veryLong')
                )
            LIMIT {tactics_per_motif}
        """


def extract_tactics(
    database_fn: str,
    min_rating: int,
    max_rating: int,
    popularity: int,
    themes: [str],
    tactics_per_theme: int,
    extract_file: str = "extract.csv",
):
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

    rows = list(set(rows))  # remove duplicates
    random.shuffle(rows)

    # Write the headers and data to a CSV file
    with open(extract_file, "w", newline="") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(column_names)  # Write the headers
        csvwriter.writerows(rows)  # Write the data

    # Close the database connection
    conn.close()


if __name__ == "__main__":
    t = ["fork", "capturingDefender", "discoveredAttack", "intermezzo", "pin"]
    t.extend(['skewer', 'interference'])

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
            "trappedPiece",
            "attraction",
            "clearance",
            "defensiveMove",
            "deflection",
            "quietMove",
            "xRayAttack",
            "trappedPiece",
            "sacrifice",
            "castling",
        ]
    )

    r = 1600
    extract_tactics("lichess_db_puzzle.db", r, r + 200, 90, t, 10)
