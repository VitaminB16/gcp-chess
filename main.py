from back_end.game import ChessGame

if __name__ == "__main__":
    board = ChessGame(player_color="white")
    board.get_valid_moves(10)
    