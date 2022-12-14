"""
Holds all classes for chess pieces
"""

# TODO move ASCII colours to sperate class

from shutil import move
import sys
import re
import random
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

    def __init__(self, white_turn=True, white_score=0, black_score=0,
                default_fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1") -> None:
        self.white_turn = white_turn
        self.white_score = white_score
        self.black_score = black_score
        self.board = [None] * 64
        self.white_captured = []
        self.black_captured = []
        self.castle_available = \
            {"white_kingside": True, "white_queenside": True,
             "black_kingside": True, "black_queenside": True}
        self.en_passant_targets = []
        self.default_fen = default_fen
        self.timer = Timer()
        self.move_history = MoveTracking()
        self.player_white = True
        self.game_in_progress = False
        # self.default_fen = "r1b1k1nr/p2p1pNp/n2B4/1p1NP2P/6P1/3P1Q2/P1P1K3/q5b1"

    def play(self) -> None:
        """Gets starting conditions from user and starts the game"""
        colour = input("What colour would you like to play as?\n"
            "1 - White, 2 - Black, or 3 - Random? ")
        self.player_white =  {
            "1": True,
            "2": False,
            "3": random.choice([True, False])
        }.get(colour)

        self.game_in_progress = True
        while self.game_in_progress:
            input_valid = False
            self.display_board()
            while not input_valid:
                move = input("Enter a move: ").strip()
                # use regex to check input mathes the correct format
                regex = re.search(r"([A-Ha-h][1-8]\s[A-Ha-h][1-8])", move)
                try:
                    if not regex or regex.span()[1] != len(move):
                        raise InvalidInputError(
                            "Regex issue - regex: {regex}, span: "
                            f"{regex.span()[1] if regex else 'None'}, length: {len(move)}"
                        )
                    move = move.split(" ")
                    move_from = self.square_to_id(move[0])
                    move_to = self.square_to_id(move[1])
                    if move_from == move_to:
                        raise InvalidInputError("Values equal")
                except InvalidInputError as error:
                    print("Invalid input, please try again")
                    print(f"({error})")
                else:
                    input_valid = self.move(move_from, move_to)

            # self.white_turn = not self.white_turn

    def move(self, move_from, move_to):
        """Takes input from user and calls the corresponding methods in piece classes

        Args:
            move_from (int): The id of the square containing the piece to be moved
            move_to (int): The id of the sqaure to try and move the piece to
        """

        errors = []
        if not isinstance(self.board[move_to], Empty) and self.board[move_to].is_white == self.white_turn:
            errors.append("Cannot move to a square occupied by your own piece")
        if not errors:
            errors.extend(self.board[move_from].validate_move(
                self.board, move_from, move_to, isinstance(self.board[move_to], Piece))
            )
        if errors:
            print("Error:", *errors)
            return False

        if not isinstance(self.board[move_to], Empty):
            if self.white_turn:
                self.white_captured.append(str(self.board[move_to]))
            else:
                self.black_captured.append(str(self.board[move_to]))

        self.board[move_to] = self.board[move_from]
        self.board[move_from] = Empty()

        return True

    def update(self):
        """Updates the game board with the result of the piece methods"""

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
        # check whether terminal supports unicode characters
        try:
            '????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????'.encode(sys.stdout.encoding)
            test = True
        except UnicodeEncodeError:
            test = False

        if not test:
            print('Unsupported characters in',sys.stdout.encoding)
            print("Using ASCII")
        # populate board with piece objects
        square_id = 0
        for row in fen[0].split("/"):
            for square in row:
                square = self.fen_to_obj(square)
                if isinstance(square, Piece):
                    self.board[square_id] = square
                    square_id += 1
                else:
                    for i in range(square):
                        self.board[square_id]= Empty()
                        square_id += 1

        # store who's turn it is
        self.white_turn = "w" == fen[1]

        # store who can castle and where
        self.castle_available["white_kingside"] = "K" in fen[2]
        self.castle_available["white_queenside"] = "Q" in fen[2]
        self.castle_available["black_kingside"] = "k" in fen[2]
        self.castle_available["black_queenside"] = "q" in fen[2]

        # set up list of any pawns vulnerable to en passant
        self.en_passant_targets = [fen[3][i:i+2] for i in range(0, len(fen[3]), 2)] \
            if fen[3] != "-" else []

        # store half move clock
        self.timer.halfmove_clock = fen[4]

        # store number of moves made
        self.timer.moves_made = fen[5]

    def display_board(self):
        """Displays the game board in the terminal
        This is pretty messy but it does work..."""

        # text colouring done by ASCII escape codes
        surround_colour = "\x1b[1;37;49m"
        reset_colour = "\x1b[0m"

        # print top border and black captured pieces
        print(surround_colour + "=======================")
        if len(self.black_captured) < 9:
            print(' '.join(str(i) for i in self.black_captured))
        else:
            print(' '.join(str(i) for i in self.black_captured[:8]))
            print(' '.join(str(i) for i in self.black_captured[8:]))
        print("=======================")
        # print guide letters from naming squares
        print("    a b c d e f g h    ")
        print(reset_colour)
        # create a list of items to be printed in a row showing guide numbers and the board
        for i in range(8):
            board_i = i if self.player_white else -i + 7
            row = [surround_colour + str(8 - board_i), "   "]
            for square in self.board[board_i*8:board_i*8+8]:
                if square:
                    row.append(str(square) + surround_colour)
                    row.append(' ')
            row.append("  ")
            row.append(str(8 - board_i))
            row.append("\x1b[0;36;49m")
            # print last 5 items in move history to the side of the board
            if i == 1:
                row.append("     History:")
            elif 1 < i < 7 and i - 2 < len(self.move_history.get_history(5)):
                item = i + (len(self.move_history.get_history(5)) -
                    7 if len(self.move_history.get_history(5)) > 5 else - 2)
                row.append(f"     {str(item + 1)}. {str(self.move_history.get_history(5)[item])}")
            row.append(reset_colour)
            # join list into string and print
            print(''.join(row))
        print()
        # second set of guide letters
        print(surround_colour + "    a b c d e f g h    ")
        # bottom border and white captured pieces
        print("=======================")
        if len(self.white_captured) < 9:
            print(' '.join(str(i) for i in self.white_captured))
        else:
            print(' '.join(str(i) for i in self.white_captured[:8]))
            print(' '.join(str(i) for i in self.white_captured[8:]))
        print("=======================")
        print(reset_colour)

    def export_fen(self) -> str:
        """Returns a string containing fen notation representing the current state
            of the game"""

    @staticmethod
    def square_to_id(square: str) -> int:
        """Converts and returns a square identified by row and column to the id in the board list

        Args:
            square (str): The square to convert
        """
        # intuitive method
        # return((ord(square[0]) - 97) + ((8 - int(square[1])) * 8))
        # simplified maths
        return ord(square[0]) - 33 - (8 * int(square[1]))

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
        self.is_white = is_white
        self.value = None
        self.fen = "None"
        self.white_unicode_icon = "None"
        self.black_unicode_icon = "None"
        self.white_colour = "\x1b[1;34;49m"
        self.black_colour = "\x1b[1;31;49m"
        self.reset_colour = "\x1b[0m"

    def validate_move(self, board: list, move_from: int, move_to: int, capture: bool):
        """Handles move validation that applies to all pieces

        Args:
            move_from (int): The id of the square containing the piece to be moved
            move_to (int): The id of the sqaure to try and move the piece to
        """
        # TODO think of and do general checks here


    def __str__(self, ascii_compatibility_mode=True) -> str:
        if ascii_compatibility_mode:
            if self.is_white:
                return self.white_colour + self.fen.upper() + self.reset_colour

            return self.black_colour + self.fen + self.reset_colour

        if self.is_white:
            return self.white_colour + self.white_unicode_icon + self.reset_colour

        return self.black_colour + self.black_unicode_icon + self.reset_colour


class Empty():
    """All the squares with no pieces"""

    def __init__(self) -> None:
        self.colour = "\x1b[1;37;49m"
        self.reset_colour = "\x1b[0m"

    def validate_move(self, move_from, move_to):
        """Returns error message as player has selected a square with no pieces"""
        return ["First square must contain a piece of your colour"]

    def __str__(self) -> str:
        return self.colour + "x" + self.reset_colour


class Pawn(Piece):
    """Class to represent a Pawn chess piece
    """
    def __init__(self, is_white: bool, has_moved=False) -> None:
        super().__init__(is_white)
        self.has_moved = has_moved
        self.white_unicode_icon = "\u2659"
        self.black_unicode_icon = "\u265F"
        self.value = 1
        self.fen = "p"

    def validate_move(self, board:list, move_from: int, move_to: int, capture: bool) -> list:
        """Moves piece to an empty position

        Args:
            move_to (str): Position to move the piece to
        """
        errors = []
        if capture:
            # possible = [(-1, -1), (-1, 1)]
            # actual = [move for move in possible if (move_from, (8 * move[0] + move[1])) not in
            #     {(7, 8), (15, 16), (23, 24), (31, 32), (39, 40), (47, 48), (55, 56)}]
            # for move in actual:
            #     if move_to == move_from + (8 * move[0] + move[1]):
            #         return errors
            possible = [(-1, -1), (-1, 1)] if self.is_white else [(1, -1), (1, 1)]
            actual = {move_from + (8 * move[0] + move[1]) for move in possible if
                (move_from, move_from + (8 * move[0] + move[1])) not in
                {(7, 8), (15, 16), (23, 24), (31, 32), (39, 40), (47, 48), (55, 56)}}
            if move_to not in actual:
                errors.append("Cannot capture there")
                return errors
        else:
            possible = [(-1, 0)] if self.is_white else [(1, 0)]
            # TODO check for obstruction here
            if not self.has_moved and isinstance(board[move_from + 8 * -1 if self.is_white else 1], Empty):
                possible.append((-2, 0) if self.is_white else (2, 0))
            actual = {move_from + (8 * move[0] + move[1]) for move in possible}
            if move_to not in actual:
                errors.append("Cannot move pawn there")
                return errors
        self.has_moved = True
        return errors


    def validate_en_passant(self) -> bool:
        """Checks whether an en passant capture is available"""

    def promote(self) -> None:
        """Handles pawn promotion"""


class Rook(Piece):
    """Class to represent a Rook chess piece
    """

    def __init__(self, is_white: bool) -> None:
        super().__init__( is_white)
        self.white_unicode_icon = "\u2656"
        self.black_unicode_icon = "\u265C"
        self.value = 5
        self.fen = "r"

    def validate_move(self, board: list, move_from: int, move_to: int, capture: bool) -> None:
        """Moves piece to an empty position

        Args:
            move_to (str): Position to move the piece to
        """
        return []


class Knight(Piece):
    """Class to represent a Knight chess piece
    """

    def __init__(self, is_white: bool) -> None:
        super().__init__(is_white)
        self.white_unicode_icon = "\u2658"
        self.black_unicode_icon = "\u265E"
        self.value = 3
        self.fen = "n"

    def validate_move(self, board: list, move_from: int, move_to: int, capture: bool) -> None:
        """Moves piece to an empty position

        Args:
            move_to (str): Position to move the piece to
        """
        return []


class Bishop(Piece):
    """Class to represent a Bishop chess piece
    """

    def __init__(self, is_white: bool) -> None:
        super().__init__(is_white)
        self.white_unicode_icon = "\u2657"
        self.black_unicode_icon = "\u265D"
        self.value = 3
        self.fen = "b"

    def validate_move(self, move_from: int, move_to: int) -> None:
        """Moves piece to an empty position

        Args:
            move_to (str): Position to move the piece to
        """


class Queen(Piece):
    """Class to represent a Queen chess piece
    """

    def __init__(self, is_white: bool) -> None:
        super().__init__(is_white)
        self.white_unicode_icon = "\u2655"
        self.black_unicode_icon = "\u265B"
        self.value = 9
        self.fen = "q"

    def validate_move(self, move_from: int, move_to: int) -> None:
        """Moves piece to an empty position

        Args:
            move_to (str): Position to move the piece to
        """


class King(Piece):
    """Class to represent a King chess piece
    """
    def __init__(self, is_white: bool, check=False) -> None:
        super().__init__(is_white)
        self.white_unicode_icon = "\u2654"
        self.black_unicode_icon = "\u265A"
        self.check = check
        self.value = None
        self.fen = "k"

    def validate_move(self, move_from: int, move_to: int) -> None:
        """Moves piece to an empty position

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


# TODO implement this
class Timer():
    """Handles timing the game"""

    def __init__(self, start=None, finish=None) -> None:
        self.start_time = start
        self.finish_time = finish
        self.delta = 0

    def start_timer(self):
        """Starts the timer"""

    def stop_timer(self):
        """Stops the timer"""

    def get_time(self) -> str:
        """Returns the current timer value"""

    def set_time(self, time):
        """Sets timer to value of 'time'

        Args:
            time: value to set timer to
        """

# TODO implement this
class MoveTracking():
    """Keeps track of moves made during the game"""

    def __init__(self, moves_made=0, halfmove_clock=0) -> None:
        self.moves_made = moves_made
        self.halfmove_clock = halfmove_clock
        self.move_history = [1, 2, 3, 4, 5, 6, 7]

    def add_move(self, move) -> None:
        """Updates attributes according to move made

        Args:
            move (str): The move that was made
        """

    def get_history(self, amount) -> list:
        """Returns a selection of values from the move history

        Args:
            amount (int): How many values to return. If not enough values are present
                as many as possible will be returned
        """
        return [1, 2, 3, 4, 5]


class InvalidInputError(Exception):
    """Will be raised in response to invalid user input to prevent program crashing"""

if __name__ == "__main__":
    pass
