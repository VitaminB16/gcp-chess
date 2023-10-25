class MovesMeta(type):
    def __call__(cls, piece, board):
        # When Moves is instantiated, redirect to the appropriate subclass
        subclass = Moves.subclasses.get(piece.piece_type.lower())
        if subclass:
            return super(MovesMeta, subclass).__call__(piece, board)
        else:
            raise ValueError(f"No movement logic defined for {piece.name}")


class Moves(metaclass=MovesMeta):
    subclasses = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Moves.subclasses[cls.__name__.lower()] = cls

    def __init__(self, piece, board):
        self.piece = piece
        self.board = board

    def get_valid_moves(self):
        raise NotImplementedError("Should be implemented in subclasses")


class Pawn(Moves):
    def get_valid_moves(self):
        """Logic for pawn movement."""


class Rook(Moves):
    def get_valid_moves(self):
        """Logic for rook movement."""


class Knight(Moves):
    def get_valid_moves(self):
        """Logic for knight movement."""


class Bishop(Moves):
    def get_valid_moves(self):
        """Logic for bishop movement."""


class Queen(Moves):
    def get_valid_moves(self):
        """Logic for queen movement."""


class King(Moves):
    def get_valid_moves(self):
        """Logic for king movement."""
