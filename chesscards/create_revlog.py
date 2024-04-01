import csv
import json
from datetime import datetime
from pathlib import Path


def create_revlog(deck_name, outfile, parent_dir='decks'):
    revlog = []

    for x in Path(f"{parent_dir}/{deck_name}/logs/").iterdir():
        if x.is_file() and x.suffix == ".jsonl":
            with x.open() as f:
                for line in f.readlines():
                    entry = json.loads(line)
                    entry['card_id'] = x.name[:-6]
                    dt = datetime.strptime(entry['review'], '%Y-%m-%d %H:%M:%S.%f')

                    if 'duration' in entry:  # skip old entries w/o duration
                        revlog.append({
                            'card_id': x.name[:-6],
                            'review_time': int(dt.timestamp() * 1000),
                            'review_rating': entry['rating'],
                            'review_state': entry['state'],
                            'review_duration': int(entry['duration'] * 1000)
                        })

    revlog.sort(key=lambda entry: entry['review_time'])

    # Open the CSV file in write mode
    with open(outfile, 'w', newline='') as csvfile:
        # Create a DictWriter object
        fieldnames = revlog[0].keys()  # Assuming all dictionaries have the same keys
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        # Write the dictionaries
        writer.writerows(revlog)


if __name__ == '__main__':
    create_revlog(deck_name='selection_1600_1800', outfile='revlog.csv')