import numpy as np
import pandas as pd

from .board import Board
from .config import STARTING_PIECES, PIECES_SYMBOLS


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
        return f"{PIECES_SYMBOLS[self.color + '_' + self.piece_type]}"


class ChessGame:
    def __init__(self, **kwargs):
        """
        Initialize a chess game.
        """
        self.player_color = kwargs.get("player_color", "white")
        self.board = Board(**kwargs)
