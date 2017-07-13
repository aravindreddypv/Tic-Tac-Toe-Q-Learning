import Environment
import random
import Constants
import datetime
import numpy as np


class QASP:
    def __init__(self):
        # self.q = np.load('QAftersymmminmax.npy').item()
        self.q = {}

    def getLabel(self):
        return Constants.Ql_Label

    def getOtherLabel(self):
        if self.getLabel() == 1:
            return 2
        else:
            return 1

    def move(self, board):  # It places optimal move while playing
        action = self.MaxiAction(board)
        board.move(action, self.getLabel())
        return action

    def train_symmetry(self, state, action, value):

        """
        There are 11 other symmetrical board positions for a particular state which are updated here
        Procedure:
            ->first rotate the given board position by 90 degrees and update value
            ->next update the the value for each left-right and top-down mirror images
            ->do the same for all other rotations i.e 180 and 270 degress
            ->action list is used to find the action after rotation so action_list is also rotated respectively for each
            rotation and mirror images
            ->numpy is used for coverting list to array and vice-versa and rotation of arrays
        """

        action_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        temp_list = list(map(int, [state[x] for x in range(9)]))
        temp_list = [temp_list[3 * i:3 * (i + 1)] for i in range(3)]
        action_list = [action_list[3 * i:3 * (i + 1)] for i in range(3)]
        temp_array = np.array(temp_list)
        action_array = np.array(action_list)
        lr_array = np.fliplr(temp_array)
        ud_array = np.flipud(temp_array)
        actionlr_array = np.fliplr(action_array)
        actionud_array = np.flipud(action_array)
        lr_list1 = lr_array.tolist()
        ud_list1 = ud_array.tolist()
        actionlr_list1 = actionlr_array.tolist()
        actionud_list1 = actionud_array.tolist()
        lr_list2 = [x for sublist in lr_list1 for x in sublist]
        ud_list2 = [x for sublist in ud_list1 for x in sublist]
        actionlr_list2 = [x for sublist in actionlr_list1 for x in sublist]
        actionud_list2 = [x for sublist in actionud_list1 for x in sublist]
        present_state = ''.join(map(str, lr_list2))
        index = actionlr_list2.index(action)
        self.q[(present_state, index)] = value
        present_state = ''.join(map(str, ud_list2))
        index = actionud_list2.index(action)
        self.q[(present_state, index)] = value
        for i in range(3):
            temp_array = np.rot90(temp_array)
            lr_array = np.fliplr(temp_array)
            ud_array = np.flipud(temp_array)
            action_array = np.rot90(action_array)
            actionlr_array = np.fliplr(action_array)
            actionud_array = np.flipud(action_array)
            temp_list1 = temp_array.tolist()
            lr_list1 = lr_array.tolist()
            ud_list1 = ud_array.tolist()
            actionlr_list1 = actionlr_array.tolist()
            actionud_list1 = actionud_array.tolist()
            action_list1 = action_array.tolist()
            temp_list2 = [x for sublist in temp_list1 for x in sublist]
            lr_list2 = [x for sublist in lr_list1 for x in sublist]
            ud_list2 = [x for sublist in ud_list1 for x in sublist]
            actionlr_list2 = [x for sublist in actionlr_list1 for x in sublist]
            actionud_list2 = [x for sublist in actionud_list1 for x in sublist]
            action_list2 = [x for sublist in action_list1 for x in sublist]
            present_state = ''.join(map(str, temp_list2))
            index = action_list2.index(action)
            self.q[(present_state, index)] = value
            present_state = ''.join(map(str, lr_list2))
            index = actionlr_list2.index(action)
            self.q[(present_state, index)] = value
            present_state = ''.join(map(str, ud_list2))
            index = actionud_list2.index(action)
            self.q[(present_state, index)] = value

    def train(self, opponent):
        env = Environment.Environment(self, opponent)
        board = env.reset()
        for episodes in range(Constants.QEpisodes):
            print episodes
            past_state = None  # past state and action are required to update in Q-Learning
            past_action = None
            while True:
                if past_state is None:
                    action = self.getAction(board)

                    # converting list to string

                    past_state = ''.join(map(str, board.state))
                    past_action = action
                    self.q[(past_state, past_action)] = 0
                    self.train_symmetry(past_state, past_action, 0)
                else:

                    # updating the values using Q-Learning which requires previous state and action and curreent
                    # board position

                    self.learn(past_state, past_action, board)
                    action = self.getAction(board)
                    past_state = ''.join(map(str, board.state))
                    past_action = action

                # state,reward,game_over is returned from environment

                board, reward, game_over = env.step(action)

                if game_over:
                    # if game is over reward is given to particular state,action pair

                    self.q[(past_state, past_action)] = reward
                    self.train_symmetry(past_state, past_action, reward)
                    break

            board = env.reset()  # reset gives an empty board if Q-Learner plays first

            # Epsilon is increased from 0 to 1.3

            Constants.Epsilon = Constants.Epsilon + (1.3 / Constants.QEpisodes)

            # Learning rate in bellman equation is decreased from 0.7 to 0.2

            Constants.Lr = Constants.Lr - (0.5 / Constants.QEpisodes)

        # dictionary is saved in numpy file format
        np.save('QAftersymmminmax.npy', self.q)
        print len(self.q)
        # find the unique states visited
        self.findUnique()

    def MaxiAction(self, board):
        # get the maximum value for current board position
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
        maxi = self.maxiValue(board)
        self.q[(past_state, past_action)] += Constants.Lr * (
            Constants.gamma * maxi - self.q[(past_state, past_action)])
        self.train_symmetry(past_state, past_action, self.q[(past_state, past_action)])
        self.AfterState(past_state, past_action, maxi)

    def AfterState(self, past_state, past_action, maxi):
        temp_list = list(map(int, [past_state[x] for x in range(9)]))
        for i in range(len(temp_list)):
            if temp_list[i] == self.getLabel():
                temp_list[i] = 0
                temp_list[past_action] = self.getLabel()
                temp = ''.join(map(str, temp_list))
                if (temp, i) not in self.q:
                    self.q[(temp, i)] = Constants.Lr * (
                        Constants.gamma * maxi)
                    self.train_symmetry(temp, i, self.q[(temp, i)])
                else:
                    self.q[(temp, i)] += Constants.Lr * (
                        Constants.gamma * maxi - self.q[(temp, i)])
                    self.train_symmetry(temp, i, self.q[(temp, i)])
                temp_list[i] = self.getLabel()
                temp_list[past_action] = 0

    def maxiValue(self, board):
        maxi = -1000
        for i in range(9):
            if board.state[i] == 0:
                temp = ''.join(map(str, board.state))
                if (temp, i) not in self.q:
                    self.q[(temp, i)] = 0
                    self.train_symmetry(temp, i, 0)
                    if 0 > maxi:
                        maxi = 0
                else:
                    if self.q[(temp, i)] > maxi:
                        maxi = self.q[(temp, i)]
        return maxi

    def findUnique(self):
        l = []
        for key in self.q:
            l.append(key[0])
        l = np.unique(l)
        print len(l)

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
                    self.train_symmetry(past_state, past_action, 0)
                else:
                    self.learn(past_state, past_action, board)
                    action = self.getAction(board)
                    past_state = ''.join(map(str, board.state))
                    past_action = action

                board, reward, game_over = env.step(action)

                if game_over:
                    self.q[(past_state, past_action)] = reward
                    self.train_symmetry(past_state, past_action, reward)
                    break
            board = env.reset()
            Constants.Epsilon = Constants.Epsilon + (1.3 / Constants.QEpisodes)
            Constants.Lr = Constants.Lr - (0.5 / Constants.QEpisodes)
        np.save('Qtestall1.npy', self.q)
        print len(self.q)
        self.findUnique()
