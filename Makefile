FILE_NAME := lichess_db_puzzle.csv.zst
URL := https://database.lichess.org/$(FILE_NAME)

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