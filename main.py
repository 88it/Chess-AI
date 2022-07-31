"""
Main file to be run
"""


from pieces import Board


if __name__ == "__main__":
    board = Board()
    board.setup()
    for i in range(8):
        j = i * 8
        print(board.board[j:j+8])
