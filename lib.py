import random
import csv
import time
import os

class Board:
    def __init__(self):
        self.board = [" " for _ in range(9)]
        self.last_move = None

    def print_board(self):
        for i in range(0, 9, 3):
            print("|".join(self.board[i:i+3]))
            if i < 6:
                print("-----")

    def make_move(self, position, symbol):
        if 0 <= position < 9 and self.board[position] == " ":
            self.board[position] = symbol
            self.last_move = position  # Record the last move made
            return True
        return False

    def check_winner(self, symbol):
        # Winning combinations
        lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                 (0, 3, 6), (1, 4, 7), (2, 5, 8),
                 (0, 4, 8), (2, 4, 6)]
        return any(all(self.board[i] == symbol for i in line) for line in lines)

    def is_full(self):
        return " " not in self.board

class Player:
    def __init__(self, symbol):
        self.symbol = symbol

    def make_move(self, board):
        raise NotImplementedError("This method should be overridden by subclasses.")

class HumanPlayer(Player):
    def make_move(self, board):
        try:
            position = int(input(f"Player {self.symbol}, enter your move (0-8): "))
            return board.make_move(position, self.symbol)
        except ValueError:
            return False

class BotPlayer(Player):
    def make_move(self, board):
        position = random.choice([i for i, spot in enumerate(board.board) if spot == " "])
        return board.make_move(position, self.symbol)

class Game:
    def __init__(self, player1, player2):
        self.board = Board()
        self.players = [player1, player2]
        self.current_player_index = 0
        self.move_count = 0
        self.start_time = time.time()
        self.game_id = None
        self.first_move = None

    def switch_player(self):
        self.current_player_index = 1 - self.current_player_index

    def play(self, game_id):
        self.game_id = game_id
        self.start_time = time.time()  # Reset the start time for each game
        self.move_count = 0  # Reset move count for each game
        self.first_move = None  # Reset the first move for each game

        while True:
            self.board.print_board()
            current_player = self.players[self.current_player_index]
            if not current_player.make_move(self.board):
                print("Invalid move, try again.")
                continue

            if self.move_count == 0:
                self.first_move = self.board.last_move

            self.move_count += 1

            if self.board.check_winner(current_player.symbol):
                self.board.print_board()
                print(f"Player {current_player.symbol} wins!")
                self.record_game_result(current_player.symbol, "win")
                break

            if self.board.is_full():
                self.board.print_board()
                print("It's a tie!")
                self.record_game_result("draw", "draw")
                break

            self.switch_player()

    def record_game_result(self, winner, game_outcome):
        end_time = time.time()
        duration = end_time - self.start_time
        game_details = [
            self.game_id,
            self.start_time,
            winner,
            self.move_count,
            end_time,
            duration,
            self.first_move,
            game_outcome
        ]
        csv_file_path = 'game_results.csv'
        with open(csv_file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(game_details)

if __name__ == "__main__":
    csv_file_path = 'game_results.csv'
    headers = ['game_id', 'start_time', 'winner', 'move_count', 'end_time', 'duration', 'first_move', 'game_outcome']

    if not os.path.isfile(csv_file_path):
        with open(csv_file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)

    player1 = HumanPlayer("X")
    player2 = BotPlayer("O")

    for game_id in range(30):  # Play 30 games
        game = Game(player1, player2)
        game.play(game_id)
