FILE_NAME := lichess_db_puzzle.csv.zst
URL := https://database.lichess.org/$(FILE_NAME)

# TODO pass deck variable to python commands to not have to configure deck in multiple py files
DECK := selection_1600_1800

.PHONY: download extract_lines
download: $(FILE_NAME)

$(FILE_NAME):
	@if [ ! -f $(FILE_NAME) ]; then \
		echo "Downloading $(FILE_NAME) from $(URL)"; \
		wget $(URL); \
	else \
		echo "$(FILE_NAME) already exists. Skipping download."; \
	fi

sample:
	@echo "Extracting the first two lines from $(FILE_NAME) and storing to sample.csv"
	@zstd -dc $(FILE_NAME) | head -n 2 > sample.csv

database:
	poetry run python chesscards/prepare_sqlite.py

extract:
	poetry run python chesscards/extract.py

deck:
	poetry run python chesscards/prepare_deck.py

train:
	poetry run python chesscards/main.py

due:
	poetry run python chesscards/show_due.py

fen:
	open "https://lichess.org/analysis/standard/$$(jq -r .fen  decks/${DECK}/cards/${id}.json | sed 's/ /_/g')"

push:
	cd decks && git add . && git commit -m "practice" && git push

pull:
	cd decks && git pull

revlog:
	poetry run python chesscards/create_revlog.py

anki:
	poetry run python chesscards/prepare_anki_deck.py
	cp anki_export/*png "/Users/oschlueter/Library/Application Support/Anki2/Olli/collection.media/"
