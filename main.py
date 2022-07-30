"""
Main file to be run
"""


from pieces import Bishop


class Board():
    """Aggregate class to store pieces and board operations

    Attributes:
        pieces (List[object]): List of the pieces on the board

    Methods:
        setup: Creates board from a fen string
        move: Take user input and call the required piece methods
        update: Update the game board with the result of the piece methods
        display: Display the game board in the terminal

    """

    def __init__(self) -> None:
        pieces = []

    def setup(self, fen) -> None:
        """Creates game board from a fen string"""

    def move(self):
        """Takes input from user and calls the corresponding methods in piece classes"""

    def update(self):
        """Updates the game board with the result of the piece methods"""

    def display(self):
        """Displays the game board in the terminal"""


if __name__ == "__main__":
    pass