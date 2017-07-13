import Board
import datetime
import random
import numpy as np


class Environment:
    def __init__(self, player, opponent):
        self.board = Board.Board()
        self.opponent = opponent
        self.player = player

    def reset(self):
        random.seed(datetime.datetime.now())
        turn = random.choice([1, 2])
        self.board = Board.Board()
        if turn == 2:
            self.opponent.move(self.board)
        return self.board

    def step(self, action):

        # Do the action and return the state,reward,game_over after opponents move

        self.board.move(action, self.player.getLabel())
        if self.board.rowColumn():
            return self.board, 1, True
        elif self.board.full_Posit():
            return self.board, 0, True
        else:
            self.opponent.move(self.board)
            if self.board.rowColumn():
                return self.board, -1, True
            elif self.board.full_Posit():
                return self.board, 0, True
            else:
                return self.board, 0, False

    def resetall(self):
        self.board = Board.Board()


class EnvironmentAll:  # Environment for Ensemble
    def __init__(self, player, opponent1, opponent2, opponent3):
        self.board = Board.Board()
        self.opponent1 = opponent1
        self.opponent2 = opponent2
        self.opponent3 = opponent3
        self.player = player

    def reset(self):
        random.seed(datetime.datetime.now())
        turn = random.choice([1, 2])
        self.board = Board.Board()
        if turn == 2:
            random.seed(datetime.datetime.now())
            r = random.uniform(0, 3)
            if r < 1:
                opponent = self.opponent1
            elif r < 2.5:
                opponent = self.opponent2
            else:
                opponent = self.opponent3
            opponent.move(self.board)
        return self.board

    def step(self, action):
        self.board.move(action, self.player.getLabel())
        if self.board.rowColumn():
            return self.board, 1, True
        elif self.board.full_Posit():
            return self.board, 0, True
        else:
            random.seed(datetime.datetime.now())
            r = random.uniform(0, 3)
            if r < 1:
                opponent = self.opponent1
            elif r < 2.5:
                opponent = self.opponent2
            else:
                opponent = self.opponent3
            opponent.move(self.board)
            if self.board.rowColumn():
                return self.board, -1, True
            elif self.board.full_Posit():
                return self.board, 0, True
            else:
                return self.board, 0, False

    def resetall(self):
        self.board = Board.Board()
