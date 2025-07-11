#hexapawn.py
import copy
import numpy as np

class Hexapawn:
    def __init__(self):
        self.board = [['B','B','B'],
                      ['-','-','-'],
                      ['W','W','W']]
        #space 1 ahead is empty ->1
        #space 1 to the right or left has opponent ->1
        
        self.player = 'W'
    
    #Function to transform board to vector representation
    def to_vector(self):
        vector_list = []
        if self.player == "W":
            vector_list.append(0)
        else:
            vector_list.append(1)
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "W":
                    vector_list.append(1)
                if self.board[i][j] == "B":
                    vector_list.append(-1)
                if self.board[i][j] == "-":
                    vector_list.append(0)
        return vector_list

    def change_turn(self):
        if self.player == 'B':
            self.player = 'W'
        else:
            self.player = 'B'
    
    def print_board(self):
        for row in self.board:
            print(row)

#The player whose turn it is to move in state s
def to_move(s):
    return s.player

#The set of legal moves in state s
#Input: state of the game.
#Output: list [action, row to be moved, column to be moved]
def possible_actions(s):
    actions = []
    if s.player == 'W':
        dir = -1
        enemy = 'B'
    else:
        dir = 1
        enemy = 'W'
    for row in range(3):
        for col in range(3):
            if s.board[row][col]==s.player:
                if (0 <= (row+dir)) and ((row+dir) < 3) and (s.board[row+dir][col] == '-'):
                    action = ['Advance', row, col]
                    actions.append(action)
                if s.player=='W' and (0<=(col+1)) and ((col+1)<3) and s.board[row+dir][col+1]==enemy:
                    action = ["Capture-Right", row, col]
                    actions.append(action)
                if s.player=='W' and (0<=(col-1)) and ((col-1)<3) and s.board[row+dir][col-1]==enemy:
                    action = ["Capture-Left", row, col]
                    actions.append(action)
                if s.player=='B' and (0<=(col+1)) and ((col+1)<3) and s.board[row+dir][col+1]==enemy:
                    action = ["Capture-Left", row, col]
                    actions.append(action)
                if s.player=='B' and (0<=(col-1)) and ((col-1)<3) and s.board[row+dir][col-1]==enemy:
                    action = ["Capture-Right", row, col]
                    actions.append(action)
    return actions


#Transition Model: defines state resulting from taking action a in state s
def result(s,action):
    #should probably make a deep copy
    new_state = copy.deepcopy(s)

    r = action[1]
    c = action[2]
    if action[0] == 'Advance' and s.player=='W':
        new_state.board[r-1][c] = 'W'
        new_state.board[r][c] = '-'
    if action[0] == 'Advance' and s.player=='B':
        new_state.board[r+1][c] = 'B'
        new_state.board[r][c] = '-'
    if action[0] == 'Capture-Right' and s.player=='W':
        new_state.board[r-1][c+1] = 'W'
        new_state.board[r][c] = '-'
    if action[0] == 'Capture-Right' and s.player=='B':
        new_state.board[r+1][c-1] = 'B'
        new_state.board[r][c] = '-'
    if action[0] == 'Capture-Left' and s.player=='W':
        new_state.board[r-1][c-1] = 'W'
        new_state.board[r][c] = '-'
    if action[0] == 'Capture-Left' and s.player=='B':
        new_state.board[r+1][c+1] = 'B'
        new_state.board[r][c] = '-'
    new_state.change_turn()
    return new_state

#Terminal test: returns true when game is over and false otherwise
#Terminal States: states where the game has ended
def is_terminal(s):
    white_pawns = sum(row.count('W') for row in s.board)
    black_pawns = sum(row.count('B') for row in s.board)
    #check if all pawns are captured
    if white_pawns == 0 or black_pawns == 0:
        return True

    #check if no moves left
    if not possible_actions(s):
        return True
    #check if pawns reached other end of board
    for c in range(3):
        if s.board[0][c] == 'W' or s.board[2][c] == 'B':
            return True
    return False

#defines final numeric value to player when game ends in terminal state s
def utility(s):
    white_pawns = sum(row.count('W') for row in s.board)
    black_pawns = sum(row.count('B') for row in s.board)
    if s.player == 'W':
        if (not(black_pawns)) or (s.board[0][0] == 'W') or (s.board[0][1] == 'W') or (s.board[0][2] == 'W'):
            return 1
        if (not white_pawns) or (s.board[2][0] == 'B') or (s.board[2][1] == 'B') or (s.board[2][2] == 'B') or (not possible_actions(s)):
            return 0
    if s.player == 'B':
        if (not(black_pawns)) or (s.board[0][0] == 'W') or (s.board[0][1] == 'W') or (s.board[0][2] == 'W') or (not possible_actions(s)):
            return 0
        if (not white_pawns) or (s.board[2][0] == 'B') or (s.board[2][1] == 'B') or (s.board[2][2] == 'B'):
            return 1
        
def minimax(state):
    vm_pair = max_value(state)
    print(vm_pair, 'vm pair')
    return vm_pair[1]

def max_value(state):
    if is_terminal(state):
        return [utility(state),None]
    value = -2
    for action in possible_actions(state):
        v_move = min_value(result(state,action))
        if v_move[0] > value:
            v_move = [v_move[0],action]
    return v_move

def min_value(state):
    if is_terminal(state):
        return [utility(state),None]
    value = 2
    for action in possible_actions(state):
        v_move = max_value(result(state,action))
        if v_move[0] > value:
            v_move = [v_move[0],action]
    return v_move

#need to revise policy table creation
def policy_table_wrapper(init_state):
    policytable = []
    return policy_table(init_state, policytable)

def create_policy(state, action) -> list:
    new_state = copy.deepcopy(state)
    board = new_state.board

    position_i = action[1]
    position_j = action[2]

    for i in range(len(board)):
        for j in range(len(board)):
            board[i][j] = 0

    board[position_i][position_j] = 1
    new_state.board = board
    policy = []
    for i in new_state.board:
        policy.extend(i)
    print(policy,'policy')
    return policy

#policy = (0 0 0 1 1 1 0 0 0)
#specifies that any of (advance 2 0), (advance 2 1), or (advance 2 2) 
#will get MAX their optimal expected value.
#For each state, the policy should include the value of the
#game as well as every action that achieves that value.
def policy_table(state, table):
    if is_terminal(state):
        return table

    move = minimax(state)
    new_state = result(state, move)
    print(new_state.board,new_state.player)
    table.append([state.to_vector(), create_policy(state, move)])
    print('table: ', table)
    return policy_table(new_state, table)


#testing
game = Hexapawn()
print(game.board)
print(game.to_vector())
#print(minimax(game))
the_policy_table = policy_table_wrapper(game)
print('The Policy Table: ', the_policy_table)