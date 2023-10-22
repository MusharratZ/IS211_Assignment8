import random
import argparse
import sys
import time


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.turn_total = 0

    def roll_die(self):
        roll = random.randint(1, 6)
        if roll == 1:
            self.turn_total = 0
        else:
            self.turn_total += roll
            self.score += roll
        return roll

    def hold(self):
        self.score += self.turn_total
        self.turn_total = 0


class ComputerPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

    # def roll_die(self):
    #     if self.turn_total < 25 or self.score + self.turn_total >= 100:
    #         return super().roll_die()
    #     else:
    #         self.hold()
    #         return 0
    def decide(self):
        remaining_to_win = 100 - self.score
        return "r" if self.turn_total < min(25, remaining_to_win) else "h"


class PlayerFactory:
    @staticmethod
    def create_player(player_type, name):
        if player_type == "human":
            return Player(name)
        elif player_type == "computer":
            return ComputerPlayer(name)
        else:
            raise ValueError("Invalid player type")


class Game:
    def __init__(self, players, winning_score):
        self.players = players
        self.current_player = 0
        self.winning_score = winning_score
        random.seed(0)

    def switch_player(self):
        self.current_player = (self.current_player + 1) % len(self.players)

    def play(self):
        while all(player.score < self.winning_score for player in self.players):
            player = self.players[self.current_player]
            print(f"\n{player.name}'s turn")
            while True:
                decision = input(
                    "Enter 'r' to roll or 'h' to hold or 'q' to quit: "
                ).lower()
                if decision == "r":
                    roll = player.roll_die()
                    print(f"Rolled a {roll}")
                    print(
                        f"Turn total: {player.turn_total}, Total score: {player.score}"
                    )
                    if roll == 1:
                        print("Turn over, no points gained.")
                        break
                elif decision == "h":
                    player.hold()
                    print(
                        f"{player.name} held. Turn total: {player.turn_total}, Total score: {player.score}"
                    )
                    break
                elif decision == "q":
                    print("Goodbye!")
                    sys.exit()
                else:
                    print("Invalid input. Enter 'r' to roll or 'h' to hold.")
            if player.score >= 100:
                winning_players = [player.name]
                print(f"Player(s) {', '.join(winning_players)} wins!")
                return  # End the game

            elif all(p.score >= self.winning_score for p in self.players):
                winning_players = [
                    p.name for p in self.players if p.score >= self.winning_score
                ]
                print(f"Player(s) {', '.join(winning_players)} wins!")
                return  # End the game
            # if any(player.score >= self.winning_score for player in self.players):
            #     winning_players = [
            #         player.name
            #         for player in self.players
            #         if player.score >= self.winning_score
            #     ]

            # print(f"Player(s) {', '.join(winning_players)} wins!")
            # break

            self.switch_player()


class TimedGameProxy(Game):
    def __init__(self, players, winning_score, timed):
        super().__init__(players, winning_score)
        self.timed = timed
        self.start_time = None

    def play(self):
        self.start_time = time.time()
        super().play()

    def switch_player(self):
        if self.timed:
            elapsed_time = time.time() - self.start_time
            if elapsed_time >= 60:
                self.end_game()
                return
        super().switch_player()

    def end_game(self):
        max_score = max(player.score for player in self.players)
        winning_players = [
            player.name for player in self.players if player.score == max_score
        ]
        print(f"\nTime is up! Player(s) {', '.join(winning_players)} wins!")
        play_again = input("Do you want to play another game? (yes/no): ").lower()
        if play_again != "yes":
            print("Goodbye!")
            sys.exit()


def main():
    while True:
        num_players = int(input("Enter the number of players (minimum 2): "))
        if num_players < 2:
            print("Number of players must be at least 2.")
            return

        player_types = []
        for i in range(num_players):
            player_type = input(
                f"Enter the type of player {i + 1} (human/computer): "
            ).lower()
            if player_type not in ["human", "computer"]:
                print("Invalid player type. Please enter 'human' or 'computer'.")
                return
            player_types.append(player_type)

        players = [
            PlayerFactory.create_player(player_type, f"Player {i + 1}")
            for i, player_type in enumerate(player_types)
        ]

        # timed = input("Do you want to enable the timed version? (yes/no): ").lower()
        timed_game = "yes"

        game = TimedGameProxy(players, 140, timed_game)
        game.play()

        play_again = input("Do you want to play another game? (yes/no): ").lower()
        if play_again != "yes":
            print("Goodbye!")
            break  # Exit the loop if the answer is not "yes"


if __name__ == "__main__":
    main()