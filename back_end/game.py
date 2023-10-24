import numpy as np
import pandas as pd

from back_end.board import Board, Piece
from config import STARTING_PIECES, PIECES_SYMBOLS


class ChessGame:
    def __init__(self, **kwargs):
        """
        Initialize a chess game.
        """
        self.player_color = kwargs.get("player_color", "white")
        self.board = Board(**kwargs)
