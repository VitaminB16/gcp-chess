class MovesMeta(type):
    def __call__(cls, piece, board, move_data):
        # When Moves is instantiated, redirect to the appropriate subclass
        subclass = Moves.subclasses.get(piece.piece_type.lower())
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

    def get_valid_moves(self):
        raise NotImplementedError("Should be implemented in subclasses")


class Pawn(Moves):
    def get_valid_moves(self):
        """Logic for pawn movement."""
        color = self.piece.color
        position = self.piece.position
        # Select the correct move and attack patterns based on color
        if color == "white":
            moves = self.move_data["pawn"]["white"][position]
            attacks = self.move_data["pawn"]["white_attack"][position]
        elif color == "black":
            moves = self.move_data["pawn"]["black"][position]
            attacks = self.move_data["pawn"]["black_attack"][position]

        # TODO: attacks = attacks & opposite_color_pieces
        #       valid_moves = moves + attacks

        return None


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
