import numpy as np
import pandas as pd

from .config import STARTING_PIECES


class Piece:
    def __init__(self, color, piece_type):
        """
        Initialize a piece with its color and type.

        :param color: 'white' or 'black'
        :param piece_type: 'pawn', 'rook', 'knight', 'bishop', 'queen', or 'king'
        """
        self.color = color
        self.piece_type = piece_type
        self.is_moved = False  # Useful for specific rules like castling or en passant.

    def __repr__(self):
        return f"{self.color[0].upper()}_{self.piece_type.upper()}"


class ChessGame:
    def __init__(self):
        """
        Initialize a chess game.
        """
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.initialize_board()

    def initialize_board(self):
        """Set the pieces to their starting positions."""
        colors = ["black", "white"]
        for idx, color in enumerate(colors):
            # Set the pawns
            row = 1 if color == "black" else 6
            for col in range(8):
                self.board[row][col] = Piece(color, "pawn")

            row = 0 if color == "black" else 7
            for col, piece_type in enumerate(STARTING_PIECES):
                self.board[row][col] = Piece(color, piece_type)

    def display_board(self):
        """Display the board."""
        board_df = pd.DataFrame(
            self.board, columns=list("ABCDEFGH"), index=list(range(1, 9))
        )
        board_df = board_df.replace(np.nan, "")
        print(board_df)
