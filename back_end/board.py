import numpy as np
import pandas as pd

from common.config import STARTING_PIECES, PIECE_SYMBOLS


class Piece:
    def __init__(self, color, piece_type, position=None):
        """
        Initialize a piece with its color and type.

        :param color: 'white' or 'black'
        :param piece_type: 'pawn', 'rook', 'knight', 'bishop', 'queen', or 'king'
        """
        self.color = color
        self.piece_type = piece_type
        self.is_moved = False  # Useful for specific rules like castling or en passant.
        self.position = position

    def __repr__(self):
        return f"{PIECE_SYMBOLS[self.color + '_' + self.piece_type]}"


class Board:
    def __init__(self, **kwargs):
        """
        Initialize a chess game.
        """
        self.player_color = kwargs.get("player_color", "white")
        self.board = np.empty((8, 8), dtype=object)
        self.piece_positions = {}
        self.initialize_board()

    def __repr__(self):
        board = self.board.reshape((8, 8))
        board_df = pd.DataFrame(
            board, columns=list("ABCDEFGH"), index=list(range(1, 9))
        )
        board_df = board_df.replace(np.nan, ".")
        if self.player_color == "white":
            board_df = board_df.loc[::-1]
        footer = board_df.columns.to_list()
        footer = pd.DataFrame([footer], columns=board_df.columns, index=[""])
        board_df = pd.concat([board_df, footer])
        return board_df.to_string(header=False)

    def initialize_board(self):
        """Set the pieces to their starting positions."""
        colors = ["black", "white"]
        for idx, color in enumerate(colors):
            # Set the pawns
            row = 1 if color == "white" else 6
            for col in range(8):
                position = row * 8 + col
                self.board[row, col] = Piece(color, "pawn", position)
                self.piece_positions[position] = self.board[row, col]

            row = 0 if color == "white" else 7
            for col, piece_type in enumerate(STARTING_PIECES):
                position = row * 8 + col
                self.board[row, col] = Piece(color, piece_type, position)
                self.piece_positions[position] = self.board[row, col]
        self.board = self.board.reshape(-1)  # Convert board to 1D array

    def get_piece(self, position):
        """Get the piece at a position."""

        return self.piece_positions.get(position)
