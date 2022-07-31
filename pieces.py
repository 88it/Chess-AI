"""
Holds all classes for chess pieces
"""


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
        self.board = [None] * 64
        self.captured = []

    def move(self):
        """Takes input from user and calls the corresponding methods in piece classes"""

    def update(self):
        """Updates the game board with the result of the piece methods"""

    def display(self):
        """Displays the game board in the terminal"""

    def setup(self, fen: str) -> None:
        """Creates game board contaning piece objects from a fen notation string template"""


class Piece:
    """Base piece type

    Attributes:
        name (str): The name of the piece
        position (str): The position the piece is in on the board
        value (int): How many points the piece is worth when captured
        colour (bool): The piece colour represented by 'True' for white
            and 'False' for black

    Methods:
    """

    def __init__(self, position: str, value: int, colour: bool) -> None:
        self.position = position
        self.value = value
        self.colour = colour

    def __str__(self) -> str:
        return f"{'White' if self.colour else 'Black'}"\
               f" in position {self.position}, Value: {self.value}"

class Pawn(Piece):
    """Class to represent a Pawn chess piece
    """
    def __init__(self, position: str, value: int, colour: bool, has_moved=False) -> None:
        super().__init__(position, value, colour)
        self.has_moved = has_moved

    def move(self, move_to: str) -> None:
        """Moves piece to an empty position

        Args:
            move_to (str): Position to move the piece to
        """

    def capture(self, move_to: str) -> None:
        """Moves piece to position containing another piece and captures it

        Args:
            move_to (str): Position to move the piece to
        """

    def validate_en_passant(self) -> bool:
        """Checks whether an en passant capture is available"""

    def promote(self) -> None:
        """Handles pawn promotion"""


class Rook(Piece):
    """Class to represent a Rook chess piece
    """

    def move(self, move_to: str) -> None:
        """Moves piece to an empty position

        Args:
            move_to (str): Position to move the piece to
        """

    def capture(self, move_to: str) -> None:
        """Moves piece to position containing another piece and captures it

        Args:
            move_to (str): Position to move the piece to
        """


class Knight(Piece):
    """Class to represent a Knight chess piece
    """

    def move(self, move_to: str) -> None:
        """Moves piece to an empty position

        Args:
            move_to (str): Position to move the piece to
        """

    def capture(self, move_to: str) -> None:
        """Moves piece to position containing another piece and captures it

        Args:
            move_to (str): Position to move the piece to
        """

class Bishop(Piece):
    """Class to represent a Bishop chess piece
    """

    def move(self, move_to: str) -> None:
        """Moves piece to an empty position

        Args:
            move_to (str): Position to move the piece to
        """

    def capture(self, move_to: str) -> None:
        """Moves piece to position containing another piece and captures it

        Args:
            move_to (str): Position to move the piece to
        """


class Queen(Piece):
    """Class to represent a Queen chess piece
    """

    def move(self, move_to: str) -> None:
        """Moves piece to an empty position

        Args:
            move_to (str): Position to move the piece to
        """

    def capture(self, move_to: str) -> None:
        """Moves piece to position containing another piece and captures it

        Args:
            move_to (str): Position to move the piece to
        """


class King(Piece):
    """Class to represent a King chess piece
    """
    def __init__(self, position: str, value: int, colour: bool, check=False) -> None:
        super().__init__(position, value, colour)
        self.check = check

    def move(self, move_to: str) -> None:
        """Moves piece to an empty position

        Args:
            move_to (str): Position to move the piece to
        """

    def capture(self, move_to: str) -> None:
        """Moves piece to position containing another piece and captures it

        Args:
            move_to (str): Position to move the piece to
        """

    def validate_castle(self, left=True) -> bool:
        """Checks whether the move to castle can be made

        Args:
            direction (bool): If true we wish to move left, if false
                we wish to move right
        """

    def check_check(self) -> bool:
        """Checks whether in check and if so whether it is checkmate
            by checking for any available moves

            If in check check_checkmate() will be called
        """

    def check_checkmate(self) -> bool:
        """Checks for any available moves, returns 'False' if
            moves available and 'True' if none are available"""


if __name__ == "__main__":
    pass
