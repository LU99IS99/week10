from lib import *
import pandas as pd

# Assuming 'lib' contains the necessary classes (Board, Player, HumanPlayer, BotPlayer, Game)
# If 'lib' does not exist, you should define these classes directly in this script

# Mapping positions to their categories
position_category = {0: 'corner', 1: 'middle', 2: 'corner', 3: 'middle', 4: 'center', 5: 'middle', 6: 'corner', 7: 'middle', 8: 'corner'}

game_data = []

# Play 30 games
for x in range(30):
    data = {"game_id": x}
    num_human_players = input("How many human players? (0/1/2): ")
    player1 = HumanPlayer("X") if num_human_players in ["1", "2"] else BotPlayer("X")
    player2 = BotPlayer("O") if num_human_players in ["0", "1"] else HumanPlayer("O")

    game = Game(player1, player2)
    move_count = 0

    while True:
        move_count += 1
        game.board.print_board()
        if not game.current_player.make_move(game.board):
            print("Invalid move, try again.")
            continue

        if move_count == 1:
            data['first_move'] = game.board.last_move
            data['first_move_position'] = position_category[game.board.last_move]

        if game.board.check_winner(game.current_player.symbol):
            game.board.print_board()
            print(f"Player {game.current_player.symbol} wins!")
            data['winner'] = game.current_player.symbol
            data['result'] = 'win' if game.current_player == game.players[0] else 'loss'
            data['move_count'] = move_count
            break

        if game.board.is_full():
            game.board.print_board()
            print("It's a tie!")
            data['winner'] = "draw"
            data['result'] = "draw"
            data['move_count'] = move_count
            break

        game.switch_player()

    game_data.append(data)

# Print and save the game data
print(pd.DataFrame(game_data))
pd.DataFrame(game_data).to_csv("./logs/database.csv")
