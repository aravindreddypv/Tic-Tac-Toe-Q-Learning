import random
import datetime


class Board:
    def __init__(self):
        self.state = [0] * 9

    def print_board(self):
        for i in range(9):
            if self.state[i] == 0:
                print "_ ",
            elif self.state[i] == 1:
                print "X ",
            else:
                print "O ",
            if i == 2 or i == 5 or i == 8:
                print("\n")
        print("\n")

    '''
    def getTurn(self):
        random.seed(datetime.datetime.now())
        self.turn = random.choice([1, 2])
        return self.turn
    '''

    def getValidMoves(self):
        Valid = []
        for i in range(9):
            if self.state[i] == 0:
                Valid.append(i)
        return Valid

    def rowColumn(self):
        if ''.join(map(str, self.state[0:3])) == '111' or ''.join(map(str, self.state[0:3])) == '222':
            return True
        elif ''.join(map(str, self.state[3:6])) == '111' or ''.join(map(str, self.state[3:6])) == '222':
            return True
        elif ''.join(map(str, self.state[6:9])) == '111' or ''.join(map(str, self.state[6:9])) == '222':
            return True
        elif ''.join(map(str, (self.state[x] for x in [0, 3, 6]))) == '111' or ''.join(
                map(str, (self.state[x] for x in [0, 3, 6]))) == '222':
            return True
        elif ''.join(map(str, (self.state[x] for x in [1, 4, 7]))) == '111' or ''.join(
                map(str, (self.state[x] for x in [1, 4, 7]))) == '222':
            return True
        elif ''.join(map(str, (self.state[x] for x in [2, 5, 8]))) == '111' or ''.join(
                map(str, (self.state[x] for x in [2, 5, 8]))) == '222':
            return True
        elif ''.join(map(str, (self.state[x] for x in [0, 4, 8]))) == '111' or ''.join(
                map(str, (self.state[x] for x in [0, 4, 8]))) == '222':
            return True
        elif ''.join(map(str, (self.state[x] for x in [2, 4, 6]))) == '111' or ''.join(
                map(str, (self.state[x] for x in [2, 4, 6]))) == '222':
            return True

    def move(self, position,label):
        self.state[position] = label  # self.getSymbol()

    def gameOver(self):
        if self.rowColumn():
            return False
        elif self.full_Posit():
            return False
        else:
            return True

    def full_Posit(self):
        if 0 not in self.state:
            return True

    '''
    def getOnes(self):
        temp = []
        for i in range(9):
            if self.state[i] == 1:
                temp.append(i)
        return temp

    
    def getTwos(self):
        temp = []
        for i in range(9):
            if self.state[i] == 2:
                temp.append(i)
        return temp
    
    '''


if __name__ == '__main__':
    board = Board()
    board.print_board()
