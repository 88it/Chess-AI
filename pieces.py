"""
Holds all classes for chess pieces
"""

from colorama import init
init()


class Board():
    """Aggregate class to store pieces and board operations

    Attributes:
        pieces (List[object]): List of the pieces on the board
        default_fen (str): Fen to be used every time a new game is started. Reccomended
            to leave as default which is a standard setup

    Methods:
        move: Take user input and call the required piece methods
        update: Update the game board with the result of the piece methods
        display: Display the game board in the terminal
        setup: Creates game board from fen notation string

    """

    def __init__(self, white_turn=True, moves_made=0, white_score=0, black_score=0,
                default_fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") -> None:
        self.white_turn = white_turn
        self.moves_made = moves_made
        self.halfmove_clock = 0
        self.white_score = white_score
        self.black_score = black_score
        self.board = [None] * 64
        self.captured = []
        self.default_fen = default_fen
        self.white_kingside = True
        self.white_queenside = True
        self.black_kingside = True
        self.black_queenside = True
        self.en_passant_targets = []
        # self.default_fen = "r1b1k1nr/p2p1pNp/n2B4/1p1NP2P/6P1/3P1Q2/P1P1K3/q5b1"

    def move(self):
        """Takes input from user and calls the corresponding methods in piece classes"""

    def update(self):
        """Updates the game board with the result of the piece methods"""

    def display(self):
        """Displays the game board in the terminal"""
        print("\x1b[1;33;49m=======================")
        print("    a b c d e f g h    ")
        print()
        for i in range(8):
            row = [str(8 - i), "   "]
            for square in self.board[i*8:i*8+8]:
                if square:
                    if square.colour:
                        row.append("\x1b[1;34;49m" + str(square) + "\x1b[33;49m")
                    else:
                        row.append("\x1b[1;31;49m" + str(square) + "\x1b[33;49m")
                    row.append(' ')
                else:
                    row.append("x ")
            row.append("  ")
            row.append(str(8 - i))
            print(''.join(row))
        print()
        print("    a b c d e f g h    ")
        print("=======================\x1b[0m")

    def setup(self, fen: str=None) -> None:
        """Creates game board contaning piece objects from a fen notation string template

        Args:
            fen (str): Fen notation to be used as a template for the board.
                Defaults to 'None' and the self.default_fen value will be used
                but if a value is supplied that overrides it for instance to
                play a pre-started game
        """
        # use default fen string for a new game if none supplied
        if fen is None:
            fen = self.default_fen
        fen = fen.split(" ")
        print(f"Initialising with fen {fen}")
        # populate board with piece objects
        square_id = 0
        for row in fen[0].split("/"):
            for square in row:
                square = self.fen_to_obj(square)
                if isinstance(square, Piece):
                    self.board[square_id] = square
                    square_id += 1
                else:
                    square_id += square

        self.white_turn = "w" == fen[1]

        self.white_kingside = "K" in fen[2]
        self.white_queenside = "Q" in fen[2]
        self.black_kingside = "k" in fen[2]
        self.black_queenside = "q" in fen[2]

        self.en_passant_targets = [fen[3][i:i+2] for i in range(0, len(fen[3]), 2)] \
            if fen[3] != "-" else []

        self.halfmove_clock = fen[4]

        self.moves_made = fen[5]


    def export_fen(self) -> str:
        """Returns a string containing fen notation representing the current state
            of the game"""

    @staticmethod
    def fen_to_obj(char: str) -> object:
        """Takes a single letter from a fen string and creates the corresponding piece object

        Args:
            char (str): The letter to use
        """

        piece = None
        is_white = char.isupper()
        char = char.lower()
        if char == "p":
            piece = Pawn(is_white)
        elif char == "r":
            piece = Rook(is_white)
        elif char == "n":
            piece = Knight(is_white)
        elif char == "b":
            piece = Bishop(is_white)
        elif char == "q":
            piece = Queen(is_white)
        elif char == "k":
            piece = King(is_white)
        else:
            return int(char)  # TODO deal with with badly formatted fen strings

        return piece


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

    def __init__(self, is_white: bool) -> None:
        self.colour = is_white
        self.value = None
        self.fen = "None"

    def __str__(self) -> str:
        return self.fen.upper() if self.colour else self.fen

class Pawn(Piece):
    """Class to represent a Pawn chess piece
    """
    def __init__(self, is_white: bool, has_moved=False) -> None:
        super().__init__(is_white)
        self.has_moved = has_moved
        self.value = 1
        self.fen = "p"

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

    def __init__(self, is_white: bool) -> None:
        super().__init__( is_white)
        self.value = 5
        self.fen = "r"

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

    def __init__(self, is_white: bool) -> None:
        super().__init__(is_white)
        self.value = 3
        self.fen = "n"

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

    def __init__(self, is_white: bool) -> None:
        super().__init__(is_white)
        self.value = 3
        self.fen = "b"

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

    def __init__(self, is_white: bool) -> None:
        super().__init__(is_white)
        self.value = 9
        self.fen = "q"

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
    def __init__(self, is_white: bool, check=False) -> None:
        super().__init__(is_white)
        self.check = check
        self.value = None
        self.fen = "k"

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
