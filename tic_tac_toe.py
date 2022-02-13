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
        # check if game board is full
        for i in range(9):
            if self.is_move_available(i):
                return False
        return True

    def get_available_move(self):
        # create a list with only available index position
        return [i for i in range(9) if self.is_move_available(i)]

    def is_player_win(self, symbol):
        # check if a player win
        # horizontal
        if self.board[0] == self.board[1] and self.board[1] == self.board[2] and self.board[0] == symbol:
            return True
        if self.board[3] == self.board[4] and self.board[4] == self.board[5] and self.board[3] == symbol:
            return True
        if self.board[6] == self.board[7] and self.board[7] == self.board[8] and self.board[6] == symbol:
            return True

        # vertical
        if self.board[0] == self.board[3] and self.board[3] == self.board[6] and self.board[0] == symbol:
            return True
        if self.board[1] == self.board[4] and self.board[4] == self.board[7] and self.board[1] == symbol:
            return True
        if self.board[2] == self.board[5] and self.board[5] == self.board[8] and self.board[2] == symbol:
            return True

        # diagonal
        if self.board[0] == self.board[4] and self.board[4] == self.board[8] and self.board[0] == symbol:
            return True
        if self.board[2] == self.board[4] and self.board[4] == self.board[6] and self.board[2] == symbol:
            return True

        return False

    @staticmethod
    def print_message(message):
        # print game message
        print(f'*** {message.upper()} ***')

    def print_board(self):
        # print game board
        print(f'\n  {self.board[0]} | {self.board[1]} | {self.board[2]}')
        print(f'  {self.board[3]} | {self.board[4]} | {self.board[5]}')
        print(f'  {self.board[6]} | {self.board[7]} | {self.board[8]}\n')

    def find_winner(self):
        # return winner symbol
        for symbol in self.players:
            if self.is_player_win(symbol):
                return symbol

        # there is no winner AND board is full, it is a tie game
        if self.is_board_full():
            return 'tie'  # draw game
        else:
            return None   # game Not finished AND no winner

    def find_random_move(self):
        # find random available move for COMPUTER
        choice = random.randint(0, 8)
        while not self.is_move_available(choice):
            choice = random.randint(0, 8)

        return choice

    def find_win_move(self):
        # find computer move
        best_move = -1
        best_move_found = False

        # 1: if computer move to pos, and computer wins (or tie game)
        for pos in self.get_available_move():
            self.board[pos] = self.COMPUTER
            winner = self.find_winner()
            if winner == self.COMPUTER or winner == 'tie':
                best_move = pos
                best_move_found = True

            self.board[pos] = self.BLANK

            if best_move_found:
                break
            else:
                best_move = pos

        if not best_move_found:
            # 2: if human move to certain position, and human wins
            for pos in self.get_available_move():
                self.board[pos] = self.HUMAN
                winner = self.find_winner()
                if winner == self.HUMAN or winner == 'tie':
                    best_move = pos
                    best_move_found = True
                self.board[pos] = self.BLANK

                if best_move_found:
                    break
                else:
                    best_move = pos

        return best_move

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