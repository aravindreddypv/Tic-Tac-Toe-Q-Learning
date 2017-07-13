import Environment
import random
import Constants
import datetime
import numpy as np


class QPlayer:
    def __init__(self):
        self.q = np.load('Qnormalall.npy').item()
        # self.q = {}

    def getLabel(self):
        return Constants.Ql_Label

    def getOtherLabel(self):
        if self.getLabel() == 1:
            return 2
        else:
            return 1

    def move(self, board):
        action = self.MaxiAction(board)
        board.move(action, self.getLabel())
        return action

    def train(self, opponent):
        env = Environment.Environment(self, opponent)
        board = env.reset()
        for episodes in range(Constants.QEpisodes):
            print episodes
            past_state = None
            past_action = None
            while True:
                if past_state is None:
                    action = self.getAction(board)
                    past_state = ''.join(map(str, board.state))
                    past_action = action
                    self.q[(past_state, past_action)] = 0
                else:
                    self.learn(past_state, past_action, board)
                    action = self.getAction(board)
                    past_state = ''.join(map(str, board.state))
                    past_action = action

                board, reward, game_over = env.step(action)

                if game_over:
                    self.q[(past_state, past_action)] = reward
                    break
            board = env.reset()
            Constants.Epsilon = Constants.Epsilon + (1.3 / Constants.QEpisodes)
            Constants.Lr = Constants.Lr - (0.5 / Constants.QEpisodes)
        np.save('Qnormalmm.npy', self.q)
        print len(self.q)
        self.findUnique()

    def MaxiAction(self, board):
        maxi = self.maxiValue(board)
        action_list = []
        for i in range(9):
            if board.state[i] == 0:
                temp = ''.join(map(str, board.state))
                if self.q[(temp, i)] == maxi:
                    action_list.append(i)
        random.seed(datetime.datetime.now())
        return random.choice(action_list)

    def getAction(self, board):
        random.seed(datetime.datetime.now())
        r = random.uniform(0, 1)
        if r < Constants.Epsilon:
            return self.MaxiAction(board)

        else:
            random.seed(datetime.datetime.now())
            return random.choice(board.getValidMoves())

    def learn(self, past_state, past_action, board):
        self.q[(past_state, past_action)] += Constants.Lr * (
            Constants.gamma *self.maxiValue(board) - self.q[(past_state, past_action)])

    def maxiValue(self, board):
        maxi = -1000
        for i in range(9):
            if board.state[i] == 0:
                temp = ''.join(map(str, board.state))
                if (temp, i) not in self.q:
                    self.q[(temp, i)] = 0
                    if 0 > maxi:
                        maxi = 0
                else:
                    if self.q[(temp, i)] > maxi:
                        maxi = self.q[(temp, i)]
        return maxi

    def trainAll(self, opponent1, opponent2, opponent3):
        env = Environment.EnvironmentAll(self, opponent1, opponent2, opponent3)
        board = env.reset()
        for episodes in range(Constants.QEpisodes):
            print episodes
            past_state = None
            past_action = None
            while True:
                if past_state is None:
                    action = self.getAction(board)
                    past_state = ''.join(map(str, board.state))
                    past_action = action
                    self.q[(past_state, past_action)] = 0
                else:
                    self.learn(past_state, past_action, board)
                    action = self.getAction(board)
                    past_state = ''.join(map(str, board.state))
                    past_action = action

                board, reward, game_over = env.step(action)

                if game_over:
                    self.q[(past_state, past_action)] = reward
                    break
            board = env.reset()
            Constants.Epsilon = Constants.Epsilon + (1.3 / Constants.QEpisodes)
            Constants.Lr = Constants.Lr - (0.5 / Constants.QEpisodes)
        np.save('Qnormalall.npy', self.q)
        print len(self.q)
        self.findUnique()


    def findUnique(self):
        l = []
        for key in self.q:
            l.append(key[0])
        l = np.unique(l)
        print len(l)
