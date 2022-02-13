import random
import sys


class TicTacToe:

    HUMAN = 'X'
    COMPUTER = 'O'
    BLANK = ' '

    players = [HUMAN, COMPUTER]
    scores = {HUMAN: -1, COMPUTER: 1, 'tie': 0}  # Computer want to maximize its score (minimax method only)

    def __init__(self):
        # main board (list comprehension)
        self.board = [self.BLANK for i in range(9)]

    def is_move_available(self, pos):
        # check if pos is empty
        if 0 <= pos <= 8:
            if self.board[pos] == self.BLANK:
                return True
        return False

    def is_board_full(self):
        ######################################
        # TODO 1
        # check if game board is full
        ######################################
        return False

    def get_available_move(self):
        # create a list with only available index position
        return [i for i in range(9) if self.is_move_available(i)]

    def is_player_win(self, symbol):
        ######################################
        # TODO 2
        # check if a player win
        ######################################
        # horizontal
        # vertical
        # diagonal
        return False

    @staticmethod
    def print_message(message):
        # print game message
        print(f'*** {message.upper()} ***')

    def print_board(self):
        ######################################
        # TODO 3
        # print game board
        ######################################
        print(f'\n   |  |  ')
        print(f'   |  |  ')
        print(f'   |  |  \n')

    def find_winner(self):
        # find the winner

        ######################################
        # TODO 4
        # return winner symbol
        ######################################

        # there is no winner AND board is full, it is a tie game
        if self.is_board_full():
            return 'tie'  # draw game
        else:
            return None   # game Not finished AND no winner

    def find_random_move(self):
        ######################################
        # TODO 5
        # find random available move for COMPUTER
        ######################################
        return 0

    def find_win_move(self):
        ######################################
        # TODO 6
        # Complete strategy 2a, 2b,
        # return the best move
        ######################################

        # find computer move
        return 0

    def find_minimax_move(self):
        # find the best move for COMPUTER: 0-8
        # with minimax algorithm
        best_move = 0
        best_score = -99999

        # maximize COMPUTER score
        for pos in self.get_available_move():
            self.board[pos] = self.COMPUTER
            score = self.minimax(False)  # get minimax score
            self.board[pos] = self.BLANK

            if score > best_score:
                best_score = score
                best_move = pos

        return best_move  # 0-8

    def minimax(self, is_computer_turn):
        winner = self.find_winner()
        if winner in self.scores:  # base case: game finished, get score (human win / computer win / tie game)
            return self.scores[winner]  # -1, +1, 0
        else:
            # No winner
            # method 1: easier to read
            if is_computer_turn:
                # computer turn: maximize score
                best_score = -99999
                for pos in self.get_available_move():
                    self.board[pos] = self.COMPUTER  # make the move
                    score = self.minimax(False)  # check score (recursive)
                    self.board[pos] = self.BLANK  # reset it
                    best_score = max(best_score, score)  # maximize score
                return best_score
            else:
                # human turn: minimize score
                best_score = 99999
                for pos in self.get_available_move():
                    self.board[pos] = self.HUMAN  # make the move
                    score = self.minimax(True)  # check score  (recursive)
                    self.board[pos] = self.BLANK  # reset it
                    best_score = min(best_score, score)  # minimize score
                return best_score

    def start_game(self):
        # game loop
        while not self.is_board_full():  # while it is not full

            # step 1: print the board and ask for input
            self.print_board()
            try:
                move = input('> X (1-9): ')
            except KeyboardInterrupt:
                sys.exit()  # quit

            move = move.strip()

            # step 2: make sure the input is valid
            is_valid_input = False
            if move.isdigit():
                pos = int(move)  # convert the digit
                pos = pos - 1
                is_valid_input = self.is_move_available(pos)  # if user input is available AND valid

            # step 3:
            if is_valid_input:
                # make user move
                self.board[pos] = self.HUMAN  # user move

                # if player win the game, exit the game loop
                winner = self.find_winner()

                if winner == self.HUMAN:   # human win
                    self.print_board()
                    self.print_message('you win')
                    break
                elif winner == 'tie':  # tie game
                    self.print_board()
                    self.print_message('tie game')
                    break
                else:
                    # the board is not full AND there is no winner (game is not finished)

                    # Generate computer move
                    # method 1
                    # choice = self.find_random_move()

                    # method 2
                    # choice = self.find_win_move()

                    # method 3
                    choice = self.find_minimax_move()
                    self.board[choice] = self.COMPUTER  # make computer move

                    print(f'> Computer: {choice+1}')

                    winner = self.find_winner()

                    # if computer win the game
                    if winner == self.COMPUTER:
                        self.print_board()
                        self.print_message("You lose")
                        break  # exit the game loop
                    elif winner == 'tie':  # tie game
                        self.print_board()
                        self.print_message('tie game')
                        break
            else:
                self.print_message("Invalid input")


game = TicTacToe()
game.start_game()