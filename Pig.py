import argparse
import random


class Player:
    """ A class representing a player. """

    # constructor that sets player's default values
    def __init__(self, name):
        self.name = name
        self.hold = False
        self.roll = False
        self.score = 0

    def hold_or_roll(self):
        """ Player method to manage the holding or rolling of a die."""

        # get player's choice on what they want to do
        choice = input('\nDo you want to HOLD ("h") or ROLL ("r") the die?: ')

        # check the choice and update the player hold and role values, or ask for a valid choice
        if choice.lower() == 'h':
            self.hold = True
            self.roll = False
        elif choice.lower() == 'r':
            self.hold = False
            self.roll = True
        else:
            print('\n\tINVALID choice! Please enter "h" or "r".')
            self.hold_or_roll()

    def check_win(self):
        """ Player method that checks if the player has won the game."""
        if self.score >= 100:
            return True


class Die:
    """ A class representing a die. """

    # initial constructor setting the default rolled value, range of numbers on the die, and initial seed
    def __init__(self):
        self.rolled = 0
        self.values = list(range(1, 7))
        random.seed(0)

    def roll(self):
        """ Die method that rolls the die. """
        self.rolled = random.choice(list(range(1, 7)))
        return self.rolled


class Game:
    """ A class that represent a game of Pig. """

    # initial constructor setting the default values for the game
    def __init__(self, num_of_players):
        self.num_of_players = num_of_players
        self.players = []
        self.die = Die()
        self.max_score = 100
        self.highest_score = 0
        self.running_score = 0

        # create players and store them in the players list, setting their name attribute
        for num in range(1, num_of_players + 1):
            self.players.append(Player('Player {}'.format(num)))

        # create counter to track current player
        self.counter = 0

        # set current player
        self.current_player = self.players[self.counter]

        # loop to keep game running until a player wins, while currently player hasn't won
        while not self.current_player.check_win():

            # print statements that display game stats
            print('\nCurrent Player: {}'.format(self.current_player.name))
            print('*' * 25)
            print('Current Stats:')
            print('\tCurrent Score: {}\n\tPotential Score: {}\n\tHighest Score: {}'.format(
                self.current_player.score, self.current_player.score + self.running_score, self.highest_score))
            print('*' * 25)
            print('Scoreboard:')

            # loop to print all current player scores
            for player in self.players:
                print('\t{}\'s Score: {}'.format(player.name, player.score))

            # call current player's method to hold or roll the die
            self.current_player.hold_or_roll()

            # if current player decides to roll the die
            if self.current_player.roll:

                # call function to clear the screen
                clear()

                # roll the die and display the details
                self.die.roll()
                print('\n\t** {} rolled a {} **'.format(self.current_player.name, self.die.rolled))

                # check to see if a 1 was rolled, display a message if yes, then set the current player to the next one
                if self.die.rolled == 1:
                    self.running_score = 0
                    self.counter += 1

                    # check to see if counter value is less than the number of players
                    if self.counter < len(self.players):

                        # set current player to the next player's index and print message
                        self.current_player = self.players[self.counter]
                        print('\tRolling a "1" ends your turn. It\'s now {}\'s turn'.format(self.current_player.name))

                    # if counter is greater than number of player, set counter and player back to first player in list
                    else:
                        self.counter = 0
                        self.current_player = self.players[self.counter]
                        print('\tRolling a "1" ends your turn. It\'s now {}\'s turn'.format(self.current_player.name))

                # for all other die values, add the rolled value to the running score
                else:
                    self.running_score += self.die.rolled
                    print('\tHolding will add {} to your score.'.format(self.running_score))

            # if current player decides to hold, clear screen, update player and highest score, and reset running score
            else:
                clear()
                self.current_player.score += self.running_score
                self.running_score = 0

                # check if player has the highest score
                if self.current_player.score > self.highest_score:
                    self.highest_score = self.current_player.score

                # check to see if player wins and print message if True, then prompt to play again
                if self.current_player.check_win():
                    print('\n\tGAME OVER, {} WINS with {} points!\n'.format(
                        self.current_player.name, self.current_player.score))

                    print('Would you like to play again with same number of players?')
                    answer = input('Enter "Y", or else the game will exit: ')

                    # if yes, clear screen and call Game with same number of players
                    if answer.lower() == 'y':
                        clear()
                        Game(self.num_of_players)

                # update player values for the next players turn
                else:
                    self.counter += 1

                    # check to see if counter value is less than the number of players
                    if self.counter < len(self.players):

                        # set current player to the next player's index
                        self.current_player = self.players[self.counter]

                    # if counter value is not less than number of player, set counter and player back to first player
                    else:
                        self.counter = 0
                        self.current_player = self.players[self.counter]


def clear():
    """ Function that adds 100 new lines to clear the screen. """
    print('\n' * 100)


def main():
    """ Function that calls the Pig Game """

    # initialize the argument parser
    parser = argparse.ArgumentParser(description='Parser for number of players playing the Pig game.')
    parser.add_argument('--numPlayers', default=2, type=int, help='Number of players playing Pig.')
    args = parser.parse_args()

    # if number of players is 1 or less, print message
    if args.numPlayers <= 1:
        print('\n\tPlaying Pig is more fun when you have 2 or more players.')
        print('\tPlease play again when you have at least 2 players.\n')
    else:
        # call Game() and pass in number of players
        Game(args.numPlayers)


if __name__ == '__main__':

    main()
