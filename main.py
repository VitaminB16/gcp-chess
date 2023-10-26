from back_end.game import ChessGame

if __name__ == "__main__":
    game = ChessGame(player_color="white")
    game.get_valid_moves(36)
    