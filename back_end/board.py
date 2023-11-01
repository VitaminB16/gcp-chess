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
        self.cost = {
            "pawn": 1,
            "knight": 3,
            "bishop": 3,
            "rook": 5,
            "queen": 9,
            "king": 10000,
        }.get(piece_type)

    def __repr__(self):
        return f"{PIECE_SYMBOLS[self.color + '_' + self.piece_type]}"


class Board:
    def __init__(self, **kwargs):
        """
        Initialize a chess game.
        """
        self.player_color = kwargs.get("player_color", "white")
        self.board = np.empty((8, 8), dtype=object)
        self.piece_positions = np.empty(64, dtype=Piece)
        self.all_pieces = {
            "white": np.zeros(64, dtype=bool),
            "black": np.zeros(64, dtype=bool),
        }
        self.pawns = {
            "white": np.array([], dtype=int),
            "black": np.array([], dtype=int),
        }
        self.costs = np.zeros(64, dtype=int)
        self.initialize_board()

    def __repr__(self):
        board = self.board.reshape((8, 8))
        board = np.where(board == None, ".", board)
        return self.print_board_layout(board, "Chess Board")

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
                self.all_pieces[color][position] = True
                self.pawns[color] = np.append(self.pawns[color], position)
                self.costs[position] = self.board[row, col].cost

            row = 0 if color == "white" else 7
            for col, piece_type in enumerate(STARTING_PIECES):
                position = row * 8 + col
                self.board[row, col] = Piece(color, piece_type, position)
                self.piece_positions[position] = self.board[row, col]
                self.all_pieces[color][position] = True
                self.costs[position] = self.board[row, col].cost
        r, c = 2, 4
        self.board[r, c] = Piece("white", "queen", r * 8 + c)
        self.piece_positions[r * 8 + c] = self.board[r, c]
        self.all_pieces["white"][r * 8 + c] = True
        self.costs[r * 8 + c] = self.board[r, c].cost
        self.board = self.board.reshape(-1)  # Convert board to 1D array

    def get_piece(self, position):
        """Get the piece at a position."""

        return self.piece_positions[position]

    def print_board_layout(self, layout, title="", header=True, *kwargs):
        """Prints a given board layout with an optional title."""
        if layout.size == 64:  # If the layout is a 1D array
            layout = layout.reshape((8, 8))

        layout_df = pd.DataFrame(
            layout, columns=list("ABCDEFGH"), index=list(range(1, 9))
        )
        if self.player_color == "white":
            layout_df = layout_df.loc[::-1]
            layout_df = layout_df._append(pd.Series(name=""))
            layout_df.iloc[len(layout_df) - 1] = layout_df.columns
            header = False

        layout_str = f"{title}\n{layout_df.to_string(header=header, index=True)}"
        return layout_str

    def print_bool(self, layout, *kwargs):
        """Prints the boolean board."""
        pieces_layout = np.where(layout.reshape((8, 8)), "X", ".")
        layout = self.print_board_layout(pieces_layout, "Boolean Board")
        return print(layout)

    def print_pieces(self, color, *kwargs):
        """Prints the pieces for the given color."""
        assert color in ["white", "black"], "Color must be 'white' or 'black'"
        pieces_layout = np.where(self.all_pieces[color].reshape((8, 8)), "X", ".")
        layout = self.print_board_layout(pieces_layout, f"{color.title()} Pieces")
        return print(layout)

    def print_white_pieces(self):
        """Prints the white pieces on the board."""
        return self.print_pieces("white")

    def print_black_pieces(self):
        """Prints the black pieces on the board."""
        return self.print_pieces("black")
