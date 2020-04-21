from typing import List
from random import randrange
import copy
import numpy as np


class Hill_Climbing:
    board: List[list] = []
    global_max: int
    flag: int = 1
    count_i = 0
    col = int(input("Enter the number of Queens\n"))
    board: List = []
    pos_list: List = []
    temp_list: List = []
    heuristic_board: List = []
    new_state: List = []
    success: int = 0
    failure: int = 0
    status: int = 0
    counter: int = 1
    input_count = int(input("Enter the number of iterations\n"))
    board_x: int = 0
    s_count: int = 0
    f_count: int = 0
    w_count: int = 0
    side_count: int = 0

    # Acts as the driver function used to call other functions
    # and keeps track of iteration number
    def HC_initial(self):

        while Hill_Climbing.counter <= Hill_Climbing.input_count:
            print("Iteration no ", Hill_Climbing.counter, "\n")
            if Hill_Climbing.status == 0:
                Hill_Climbing.status = 1
                self.initial_state()

                while Hill_Climbing.status == 1:
                    Hill_Climbing.w_count = Hill_Climbing.w_count + 1

                    if Hill_Climbing.counter <= 3:  # Prints 3 search sequences
                        print("Search sequence ", Hill_Climbing.counter, "\n")
                        a = np.array(Hill_Climbing.board)
                        print(a.reshape((Hill_Climbing.col, Hill_Climbing.col)))
                        print("\n")

                    Hill_Climbing.global_max = self.heuristic(Hill_Climbing.board)

                    # Checks if the goal is found i.e if a board configuration
                    # with zero attacks has been created
                    if Hill_Climbing.global_max == 0:
                        Hill_Climbing.s_count = Hill_Climbing.s_count + Hill_Climbing.w_count - 1
                        Hill_Climbing.success = Hill_Climbing.success + 1

                        if Hill_Climbing.counter <= 3:
                            print("Success")

                        Hill_Climbing.status = 0
                    else:
                        self.hb()
                        self.selection(Hill_Climbing.heuristic_board)

            Hill_Climbing.w_count = 0
            Hill_Climbing.counter = Hill_Climbing.counter + 1

        success_rate = (Hill_Climbing.success / (Hill_Climbing.success + Hill_Climbing.failure)) * 100
        failure_rate = 100 - success_rate
        print("Success rate ", success_rate)
        print("Failure rate ", failure_rate)
        print("Average no. of steps when it succeeds ", Hill_Climbing.s_count / Hill_Climbing.success)
        print("Average no. of steps when it fails ", Hill_Climbing.f_count / Hill_Climbing.failure)

    # Generates a new board
    def initial_state(self):
        Hill_Climbing.board = []
        for i in range(0, Hill_Climbing.col):
            row: List = [0] * Hill_Climbing.col
            j = randrange(0, Hill_Climbing.col)
            row[j] = 1
            Hill_Climbing.board.insert(i, row)
        Hill_Climbing.board = list(map(list, np.transpose(Hill_Climbing.board)))

    # Sorts the position list based on increasing columnn number
    def Sort(sub_li):
        sub_li.sort(key=lambda x: x[1])
        return sub_li

    # Calculates heuristic i.e total number of attacks for a board
    def heuristic(self, board):

        r_attack = 0
        f_attack = 0
        attack = 0
        count_i = 0
        for m in range(0, Hill_Climbing.col):
            for n in range(0, Hill_Climbing.col):
                if board[m][n] == 1:

                    if Hill_Climbing.flag == 1:
                        Hill_Climbing.temp_list.insert(n, [m, n])  # temp_list stores position of queens

                    for p in range(n + 1, Hill_Climbing.col):  # Loop counts row attacks
                        if board[m][p] == 1:
                            count_i = count_i + 1

                    for p in range(0, n):  # Loop counts reverse attack
                        if m + p + 1 < Hill_Climbing.col and n - p - 1 >= 0:
                            if board[m + p + 1][n - p - 1] == 1:
                                r_attack = r_attack + 1
                    for p in range(0, Hill_Climbing.col - n):  # Loop counts forward attack
                        if m + p + 1 < Hill_Climbing.col and n + p + 1 < Hill_Climbing.col:
                            if board[m + p + 1][n + p + 1] == 1:
                                f_attack = f_attack + 1

            attack = count_i + r_attack + f_attack

        Hill_Climbing.pos_list = Hill_Climbing.Sort(Hill_Climbing.temp_list)

        Hill_Climbing.flag = 0

        return attack

    # Creates a board with heuristic values in a every position
    # that shows how many attacks are possible
    # if the queen is moved to that position.
    def hb(self):

        Hill_Climbing.heuristic_board = copy.deepcopy(Hill_Climbing.board)

        for m in range(0, Hill_Climbing.col):

            x = Hill_Climbing.pos_list[m][0]
            y = Hill_Climbing.pos_list[m][1]

            Hill_Climbing.new_state = copy.deepcopy(Hill_Climbing.board)

            # Creates all possible configurations by moving the queen to a new row for every column
            for n in range(0, Hill_Climbing.col):
                if Hill_Climbing.new_state[n][m] == 0 and Hill_Climbing.new_state[n][m] == Hill_Climbing.board[n][m]:
                    Hill_Climbing.new_state[n][m], Hill_Climbing.new_state[x][y] = Hill_Climbing.new_state[x][y], \
                                                                                   Hill_Climbing.new_state[n][m]
                    Hill_Climbing.heuristic_board[n][m] = self.heuristic(Hill_Climbing.new_state)

                    x = n
                    y = m

                if Hill_Climbing.board[n][m] == 1:
                    Hill_Climbing.heuristic_board[n][m] = Hill_Climbing.global_max + 1

        Hill_Climbing.flag = 1

    # Creates a board with lesser heuristic than that of current board
    def selection(self, heuristic_board):

        x = 0
        y = 0

        min_list = []
        temp = Hill_Climbing.global_max

        for i in range(0, Hill_Climbing.col):

            min_value = min(heuristic_board[i])

            if min_value < temp:
                temp = min_value
                x = i
                y = heuristic_board[i].index(min_value)

            elif min_value == temp:
                x = i
                y = heuristic_board[i].index(min_value)
                min_list.append([min_value, x, y])          #Stores heuristic that are equal to global maximum

        # Creates a board with lesser attacks
        if temp < Hill_Climbing.global_max:

            Hill_Climbing.side_count = 0                    #Finds the Queen that is supposed to be swapped
            for i in range(0, Hill_Climbing.col):
                if Hill_Climbing.pos_list[i][1] == y:
                    Hill_Climbing.board_x = Hill_Climbing.pos_list[i][0]

            # Creates a board with lesser heuristic than that of current board
            Hill_Climbing.board[x][y], Hill_Climbing.board[Hill_Climbing.board_x][y] = \
                Hill_Climbing.board[Hill_Climbing.board_x][y], Hill_Climbing.board[x][y]

            Hill_Climbing.status = 1

        # Creates a board with equal attacks i.e sideway move is made
        elif temp == Hill_Climbing.global_max and Hill_Climbing.side_count <= 100 and len(min_list) != 0:

            Hill_Climbing.side_count = Hill_Climbing.side_count + 1
            #Selects a random heuristic that is equal from min_list 
            m = randrange(0, len(min_list))
            x = min_list[m][1]
            y = min_list[m][2]

            for i in range(0, Hill_Climbing.col):
                if Hill_Climbing.pos_list[i][1] == y:
                    Hill_Climbing.board_x = Hill_Climbing.pos_list[i][0]

            Hill_Climbing.board[x][y], Hill_Climbing.board[Hill_Climbing.board_x][y] = \
                Hill_Climbing.board[Hill_Climbing.board_x][y], Hill_Climbing.board[x][y]

            Hill_Climbing.status = 1


        else:

            Hill_Climbing.side_count = 0
            Hill_Climbing.f_count = Hill_Climbing.f_count + Hill_Climbing.w_count - 1
            Hill_Climbing.failure = Hill_Climbing.failure + 1
            if Hill_Climbing.counter <= 3:
                print("Fail")
            Hill_Climbing.status = 0

        Hill_Climbing.pos_list = []
        Hill_Climbing.temp_list = []


HC: Hill_Climbing = Hill_Climbing()
HC.HC_initial()
