import Environment
import random
import Constants
import datetime
import numpy as np
import BestPlayer


class RandomPlayer:
    def __init__(self):
        random.seed(datetime.datetime.now())

    def getLabel(self):
        return Constants.Rp_Label

    def move(self, board):
        random.seed(datetime.datetime.now())
        random_choice = random.choice(board.getValidMoves())
        board.move(random_choice, self.getLabel())


class DeepQPlayer:
    def __init__(self):
        random.seed(datetime.datetime.now())


class SafePlayer:
    def __init__(self):
        pass

    def getLabel(self):
        return Constants.Sp_Label

    def move(self, board):
        turn = self.getLabel()
        rturn = self.getOtherLabel()
        vm = board.getValidMoves()
        final_moves = []
        block_moves = []
        for i in range(len(vm)):
            board.state[vm[i]] = turn
            if board.rowColumn():
                final_moves.append(vm[i])
            board.state[vm[i]] = 0
            board.state[vm[i]] = rturn
            if board.rowColumn():
                block_moves.append(vm[i])
            board.state[vm[i]] = 0
        if len(final_moves) == 0:
            if len(block_moves) == 0:
                random.seed(datetime.datetime.now())
                board.move(random.choice(vm), self.getLabel())
            else:
                random.seed(datetime.datetime.now())
                board.move(random.choice(block_moves), self.getLabel())
        else:
            random.seed(datetime.datetime.now())
            board.move(random.choice(final_moves), self.getLabel())

    def getOtherLabel(self):
        if self.getLabel() == 1:
            return 2
        else:
            return 1


class HumanPlayer:
    def __init__(self):
        pass

    def getLabel(self):
        return Constants.Hp_Label

    def move(self, board):
        position = int(raw_input("Enter your position to move:"))
        if position in board.getValidMoves():
            board.move(position,self.getLabel())
            return position
        else:
            self.move(board)

class MyPlayer:
    def __init__(self):
        pass
    def getLAbel(self):
        return Constants.Mp_Label

    def move(self,board):
        Rp = RandomPlayer()
        Sp = SafePlayer()
        Bp = BestPlayer.BestPlayer()
        random.seed(datetime.datetime.now())
        r=random.uniform(0,3)
        if r<1:
            Rp.move(board)
        elif r<2:
            Sp.move(board)
        else:
            Bp.move(board)


if __name__ == '__main__':
    pass
