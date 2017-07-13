import Environment
import Constants
import random
import datetime


class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def getMoves(self, board, turn, rturn):
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
        return final_moves, block_moves

    def playGame(self):
        env = Environment.Environment(self.player1,self.player2)
        env.resetall()
        # present = 1  # env.board.getTurn()
        # temp_present = present
        p1 = 0
        p2 = 0
        count1 = 0
        count2 = 0
        for i in range(Constants.Games):
            random.seed(datetime.datetime.now())
            present = random.choice([1, 2])  # env.board.getTurn()  # temp_present
            while env.board.gameOver():
                if present == 1:
                    # print "player1 turn\n"
                    final_moves, block_moves = self.getMoves(env.board, self.player1.getLabel(),
                                                             self.player1.getOtherLabel())
                    action = self.player1.move(env.board)
                    if len(final_moves) != 0:
                        if action not in final_moves:
                            count1 += 1
                    else:
                        if len(block_moves) != 0:
                            if action not in block_moves:
                                count2 += 1
                    if env.board.rowColumn():
                        p1 += 1
                else:
                    # print "player2 turn\n"
                    self.player2.move(env.board)
                    if env.board.rowColumn():
                        p2 += 1
                        # print "won  the game\n"
                # env.board.print_board()
                if present == 1:
                    present = 2
                else:
                    present = 1
            env.resetall()
        print p1, p2, Constants.Games - p1 - p2
        print "count=", count1, count2
