import numpy as np

from back_end.utils import (
    binary_array_to_int,
    int_to_binary_array,
    reverse_binary_array_int,
    compute_line_attacks,
)


class MovesMeta(type):
    def __call__(cls, piece, board, move_data):
        # When Moves is instantiated, redirect to the appropriate subclass
        if piece is None:
            piece_type = "default"
        else:
            piece_type = piece.piece_type.lower()
        piece_type = {"queen": "slider", "rook": "slider", "bishop": "slider"}.get(
            piece_type, piece_type
        )
        subclass = Moves.subclasses.get(piece_type)
        if subclass:
            return super(MovesMeta, subclass).__call__(piece, board, move_data)
        else:
            raise ValueError(f"No movement logic defined for {piece.name}")


class Moves(metaclass=MovesMeta):
    subclasses = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Moves.subclasses[cls.__name__.lower()] = cls

    def __init__(self, piece, board, move_data):
        self.piece = piece
        self.board = board
        self.move_data = move_data
        self.color = piece.color
        self.opposite_color = "black" if piece.color == "white" else "white"
        self.position = piece.position
        self.opposite_color_pieces = board.all_pieces[self.opposite_color]
        self.occupied = self.board.all_pieces["white"] | self.board.all_pieces["black"]
        self.occupied[self.position] = False
        self.position_array = np.zeros(64, dtype=bool)
        self.position_array[self.position] = True
        self.valid_moves = np.zeros(64, dtype=bool)
        self.moves = self.move_data[piece.piece_type]

    def get_valid_moves(self):
        raise NotImplementedError("Should be implemented in subclasses")


class Default(Moves):
    def get_valid_moves(self):
        return []


class Slider(Moves):
    def get_valid_moves(self):
        """Logic for queen movement."""

        directions = self.moves[:, self.position]
        for direction in directions:
            o = self.occupied[direction]
            if not any(o):
                self.valid_moves[direction] = True
                continue

            s = self.position_array[direction]
            o = self.occupied[direction]

            line_attacks = compute_line_attacks(o=o, s=s)

            self.valid_moves[direction] = line_attacks

        self.valid_moves = self.valid_moves & ~self.board.all_pieces[self.color]

        self.board.print_bool(self.valid_moves)
        print(self.board)

        return self.valid_moves


class Knight(Moves):
    def get_valid_moves(self):
        """Logic for knight movement."""

        moves = self.moves[:, self.position]
        self.valid_moves = moves & ~self.board.all_pieces[self.color]

        return self.valid_moves


class King(Moves):
    def get_valid_moves(self):
        """Logic for king movement."""

        moves = self.moves[:, self.position]
        self.valid_moves = moves & ~self.board.all_pieces[self.color]

        # TODO: Logic for filtering out attacked squares
        # TODO: Logic for castling

        return self.valid_moves


class Pawn(Moves):
    def get_valid_moves(self):
        """Logic for pawn movement."""
        # Select the correct move and attack patterns based on color
        if self.color == "white":
            moves = self.moves["white"][self.position]
            attacks = self.moves["white_attack"][self.position]
        elif self.color == "black":
            moves = self.moves["black"][self.position]
            attacks = self.moves["black_attack"][self.position]

        attacks = attacks & self.opposite_color_pieces
        moves = (
            moves & ~self.board.all_pieces["white"] & ~self.board.all_pieces["black"]
        )
        valid_moves = moves | attacks

        # TODO: Logic for en passant

        return valid_moves
