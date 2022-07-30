"""
Holds all classes for chess pieces
"""


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
