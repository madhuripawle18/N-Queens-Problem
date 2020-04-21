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
    pos_list: List=[]
    temp_list: List = []
    heuristic_board: List = []
    new_state: List = []
    success:int=0
    failure:int=0
    status:int=0
    counter:int=1
    input_count=int(input("Enter the number of iterations\n"))
    board_x:int=0
    r_count:int=0
    t_count:int=0
    w_count:int= 1
    init_count: int=1
    total_r_count: int = 0

    # Initial function which acts as the main function.
    def HC_initial(self):

        #This loop goes on till the desired number of iterations is reached.
        while Hill_Climbing.counter<=Hill_Climbing.input_count:
            print ("Iteration: ",Hill_Climbing.counter)

            #This loop goes on till a success state has been reached.
            while Hill_Climbing.success==0:

                if Hill_Climbing.init_count == 1:
                    self.initial_state()
                    Hill_Climbing.status=1

                #This loop checks if Hill climbing is still in progress
                while Hill_Climbing.status == 1:
                    Hill_Climbing.global_max = self.heuristic(Hill_Climbing.board)

                    #If Goal state has been reached
                    if Hill_Climbing.global_max == 0:
                        Hill_Climbing.status = 0
                        Hill_Climbing.success = 1

                    else:
                        self.hb()
                        self.selection(Hill_Climbing.heuristic_board)

            Hill_Climbing.t_count = Hill_Climbing.t_count + Hill_Climbing.w_count + Hill_Climbing.r_count
            Hill_Climbing.total_r_count = Hill_Climbing.total_r_count + Hill_Climbing.r_count
            Hill_Climbing.success = 0
            Hill_Climbing.w_count = 0
            Hill_Climbing.r_count = 0
            Hill_Climbing.counter = Hill_Climbing.counter + 1

        print("Average Number of random restarts used without sideways move", Hill_Climbing.total_r_count/Hill_Climbing.input_count)
        print("Average number of steps required without sideways ", Hill_Climbing.t_count/Hill_Climbing.input_count)

    #Function to create a random initial state
    def initial_state(self):
        Hill_Climbing.board=[]
        for i in range(0, Hill_Climbing.col):
            row: List = [0] * Hill_Climbing.col
            j = randrange(0, Hill_Climbing.col)
            row[j] = 1
            Hill_Climbing.board.insert(i, row)
        Hill_Climbing.board = list(map(list, np.transpose(Hill_Climbing.board)))

    #Function to keep position list (pos_list) in ascending order
    def Sort(sub_li):
        sub_li.sort(key=lambda x: x[1])
        return sub_li

    #Function which calculates the heuristic value of any board given to it
    def heuristic(self, board):

        r_attack = 0
        f_attack = 0
        attack = 0
        count_i = 0
        for m in range(0, Hill_Climbing.col):
            for n in range(0, Hill_Climbing.col):
                if board[m][n] == 1:
                    if Hill_Climbing.flag == 1:
                        Hill_Climbing.temp_list.insert(n, [m, n])

                    for p in range(n + 1, Hill_Climbing.col):    #For loop for horizontal attacks
                        if board[m][p] == 1:
                            count_i = count_i + 1

                    for p in range(0,n):                         #For loop for left diagonal going in downward direction
                        if m+p+1<Hill_Climbing.col and n-p-1>=0:
                            if board[m+p+1][n-p-1]==1:
                                r_attack=r_attack+1

                    for p in range(0,Hill_Climbing.col-n ):      #For loop for right diagonal going in downward direction
                        if m + p + 1 < Hill_Climbing.col and n + p + 1 <Hill_Climbing.col:
                            if board[m+p+1][n+p+1]==1:
                                f_attack = f_attack+1

            attack = count_i + r_attack + f_attack               #Total number of attacks

        Hill_Climbing.pos_list = Hill_Climbing.Sort(Hill_Climbing.temp_list)  #List of the locations where 1s (Queens are present)

        Hill_Climbing.flag = 0

        return attack

    #Function which creates a heuristic board using heauristic values of all the possible new state configurations
    def hb(self):

        Hill_Climbing.heuristic_board = copy.deepcopy(Hill_Climbing.board)

        for m in range(0, Hill_Climbing.col):

            x = Hill_Climbing.pos_list[m][0]
            y = Hill_Climbing.pos_list[m][1]

            Hill_Climbing.new_state = copy.deepcopy(Hill_Climbing.board)

            for n in range(0, Hill_Climbing.col):
                if Hill_Climbing.new_state[n][m] == 0 and Hill_Climbing.new_state[n][m] == Hill_Climbing.board[n][m]:

                    # Generation of all possible new states
                    Hill_Climbing.new_state[n][m], Hill_Climbing.new_state[x][y] = Hill_Climbing.new_state[x][y], Hill_Climbing.new_state[n][m]
                    Hill_Climbing.heuristic_board[n][m] = self.heuristic(Hill_Climbing.new_state)

                    x = n
                    y = m

                if Hill_Climbing.board[n][m] == 1:
                    Hill_Climbing.heuristic_board[n][m] = Hill_Climbing.global_max

        Hill_Climbing.flag=1

    #Function which decides which heuristic is to be used for swapping the queen
    def selection(self, heuristic_board):

        temp = Hill_Climbing.global_max
        for i in range(0, Hill_Climbing.col):

            min_value = min(heuristic_board[i])

            if min_value < temp:                        #Selection of minimum heuristic
                temp = min_value
                x = i
                y = heuristic_board[i].index(min_value)

        if temp < Hill_Climbing.global_max:

            for i in range(0, Hill_Climbing.col):
                if Hill_Climbing.pos_list[i][1] == y:
                    Hill_Climbing.board_x = Hill_Climbing.pos_list[i][0]

            # Better board with lesser attacks than global maxima is being generated
            Hill_Climbing.board[x][y], Hill_Climbing.board[Hill_Climbing.board_x][y] = \
                Hill_Climbing.board[Hill_Climbing.board_x][y], Hill_Climbing.board[x][y]
            Hill_Climbing.w_count = Hill_Climbing.w_count + 1

        else:

            Hill_Climbing.r_count = Hill_Climbing.r_count+1
            Hill_Climbing.status = 0
            Hill_Climbing.init_count = 1

        Hill_Climbing.pos_list = []
        Hill_Climbing.temp_list = []


HC: Hill_Climbing = Hill_Climbing()
HC.HC_initial()