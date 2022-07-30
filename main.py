"""
Main file to be run
"""


from pieces import Pawn, Rook, Knight, Bishop, Queen, King


class Board():
    """Aggregate class to store pieces and board operations

    Attributes:
        pieces (List[object]): List of the pieces on the board

    Methods:
        move: Take user input and call the required piece methods
        update: Update the game board with the result of the piece methods
        display: Display the game board in the terminal
        setup: Creates game board from fen notation string

    """

    def __init__(self, white_turn=True, moves_made=0, white_score=0, black_score=0) -> None:
        self.white_turn = white_turn
        self.moves_made = moves_made
        self.white_score = white_score
        self.black_score = black_score
        self.board = []
        self.captured = []

    def move(self):
        """Takes input from user and calls the corresponding methods in piece classes"""

    def update(self):
        """Updates the game board with the result of the piece methods"""

    def display(self):
        """Displays the game board in the terminal"""

    def setup(self, fen: str, pawn, rook, knight, bishop, queen, king) -> None:
        """Creates game board contaning piece objects from a fen notation string template"""


if __name__ == "__main__":
    board = Board()
