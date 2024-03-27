import csv
import re
from io import BytesIO

import cairosvg
import chess.svg
import matplotlib.pyplot as plt
from PIL import Image


def read(fn: str):
    with open(fn) as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def sample():
    return read('sample.csv')


def extract():
    return read('extract.csv')


def display(board: chess.Board, flip=False):
    # display 'not board.turn' when showing the exercise
    # display 'board.turn' when showing the solution
    turn = board.turn if flip else not board.turn
    svg = chess.svg.board(flipped=turn, board=board)

    img_png = cairosvg.svg2png(svg)
    img = Image.open(BytesIO(img_png))

    plt.ion()
    plt.axis('off')
    plt.imshow(img)
    plt.show(block=False)


def solution_san(tactic: dict, board: chess.Board):
    moves_uci = tactic['Moves'].split(' ')[1:]
    moves = [chess.Move.from_uci(uci) for uci in moves_uci]
    return board.variation_san(moves)


def expected_input(solution: str):
    return re.sub(r'\d+\.\.* ?', '', solution)


def push_previous_move(tactic: dict, board: chess.Board):
    for move in [tactic['Moves'].split(' ')[0]]:
        board.push(chess.Move.from_uci(move))


def push_solution(tactic: dict, board: chess.Board):
    for move in tactic['Moves'].split(' ')[1:]:
        board.push(chess.Move.from_uci(move))


if __name__ == '__main__':
    data = extract()

    for tactic in data:
        board = chess.Board(tactic['FEN'])
        push_previous_move(tactic, board)
        player = "White" if board.turn else "Black"

        display(board)
        response = input(f'{player} to move: ')
        solution = solution_san(tactic, board)
        expected = expected_input(solution)
        print(solution)

        if response == expected:  # TODO this matching should be somewhat fuzzy to be more accurate
            print("You solved this puzzle!")
            # TODO apply 'good' rating for SRS
        else:
            input("Try again another time.")
            # TODO apply 'bad' rating for SRS

        push_solution(tactic, board)
        display(board, flip=True)
        input()


