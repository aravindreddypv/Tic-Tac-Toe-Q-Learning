import numpy as np
import random
import datetime
import Constants


class BestPlayer:
    def __init__(self):
        self.m = np.load('Mvalue.npy').item()
        # self.m = {}

    def getLabel(self):
        return Constants.Bp_Label

    def move(self, board):
        action = self.m[(''.join(map(str, board.state)),self.getLabel())]
        random.seed(datetime.datetime.now())
        board.move(random.choice(action), self.getLabel())

    def train(self):
        mboard = [0] * 9
        self.player1(mboard)
        mborad = [0] * 9
        self.player2(mboard)
        print len(self.m)
        np.save('Mvalue', self.m)

    def getValidMoves(self, mboard):
        Valid = []
        for i in range(9):
            if mboard[i] == 0:
                Valid.append(i)
        return Valid

    def rowColumn(self, mboard):
        if ''.join(map(str, mboard[0:3])) == '111' or ''.join(map(str, mboard[0:3])) == '222':
            return True
        elif ''.join(map(str, mboard[3:6])) == '111' or ''.join(map(str, mboard[3:6])) == '222':
            return True
        elif ''.join(map(str, mboard[6:9])) == '111' or ''.join(map(str, mboard[6:9])) == '222':
            return True
        elif ''.join(map(str, (mboard[x] for x in [0, 3, 6]))) == '111' or ''.join(
                map(str, (mboard[x] for x in [0, 3, 6]))) == '222':
            return True
        elif ''.join(map(str, (mboard[x] for x in [1, 4, 7]))) == '111' or ''.join(
                map(str, (mboard[x] for x in [1, 4, 7]))) == '222':
            return True
        elif ''.join(map(str, (mboard[x] for x in [2, 5, 8]))) == '111' or ''.join(
                map(str, (mboard[x] for x in [2, 5, 8]))) == '222':
            return True
        elif ''.join(map(str, (mboard[x] for x in [0, 4, 8]))) == '111' or ''.join(
                map(str, (mboard[x] for x in [0, 4, 8]))) == '222':
            return True
        elif ''.join(map(str, (mboard[x] for x in [2, 4, 6]))) == '111' or ''.join(
                map(str, (mboard[x] for x in [2, 4, 6]))) == '222':
            return True

    def gameOver(self, mboard):
        if self.rowColumn(mboard):
            return False
        elif 0 not in mboard:
            return False
        else:
            return True

    def player1(self, mboard):
        tempboard = mboard[:]
        if self.rowColumn(mboard):
            return -1
        if 0 not in mboard:
            return 0
        vm = self.getValidMoves(mboard)
        value = -100
        action = 0
        tt = {}
        action_list = []
        for i in range(len(vm)):
            tempboard[vm[i]] = 1
            temp = self.player2(tempboard)
            tempboard[vm[i]] = 0
            if temp > value:
                value = temp
                action = vm[i]
            if temp in tt:
                tt[temp].append(vm[i])
            else:
                tt[temp] = [vm[i]]
        self.m[(''.join(map(str, tempboard)), 1)] = tt[value]
        return value

    def player2(self, mboard):
        tempboard = mboard[:]
        if self.rowColumn(mboard):
            return 1
        if 0 not in mboard:
            return 0
        vm = self.getValidMoves(mboard)
        tt = {}
        value = 100
        action = 0
        for i in range(len(vm)):
            tempboard[vm[i]] = 2
            temp = self.player1(tempboard)
            tempboard[vm[i]] = 0
            if temp < value:
                value = temp
                action = vm[i]
            if temp in tt:
                tt[temp].append(vm[i])
            else:
                tt[temp] = [vm[i]]
        self.m[(''.join(map(str, tempboard)), 2)] = tt[value]
        return value


if __name__ == '__main__':
    Bp = BestPlayer()
    Bp.train()
