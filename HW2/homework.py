# Global
from copy import deepcopy
import os, time

black_king_row = {(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)}
white_king_row = {(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7)}
movement = {'b': [(-1, 1), (1, 1)], 'w': [(-1, -1), (1, -1)],
            'B': [(-1, -1), (-1, 1), (1, -1), (1, 1)], 'W': [(-1, -1), (-1, 1), (1, -1), (1, 1)]}
single_jump_path = []


class Move:
    def __init__(self, cur_pos, new_pos, parent, color):
        self.cur_pos = cur_pos
        self.new_pos = new_pos
        self.parent = parent
        self.color = color


class jumpMove:
    def __init__(self, cur_pos, new_pos, jump_path, skipped, color_change):
        self.cur_pos = cur_pos
        self.new_pos = new_pos
        self.jump_path = jump_path
        self.skipped = skipped
        self.color_change = color_change


class Board:
    def __init__(self, panel):
        self.panel = panel
        self.black_pos = []
        self.black_king_pos = []
        self.white_pos = []
        self.white_king_pos = []
        for row in range(0, 8):
            for col in range(0, 8):
                if panel[row][col] == 'b':
                    self.black_pos.append((col, row))
                if panel[row][col] == 'B':
                    self.black_king_pos.append((col, row))
                if panel[row][col] == 'w':
                    self.white_pos.append((col, row))
                if panel[row][col] == 'W':
                    self.white_king_pos.append((col, row))
        self.white_count = len(self.white_pos) + len(self.white_king_pos)
        self.white_king_count = len(self.white_king_pos)
        self.black_count = len(self.black_pos) + len(self.black_king_pos)
        self.black_king_count = len(self.black_king_pos)


def outPointTrans(x, y):
    axis = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    t = 8 - y
    res = axis[x] + str(t)
    return res


def boundTest(pos):
    if 0 <= pos[0] <= 7 and 0 <= pos[1] <= 7:
        return True
    else:
        return False


def singleMode(ori_board, max_player_color):
    all_move = getAllPossibleMove(ori_board, max_player_color)
    path = []
    if len(all_move):
        move = all_move[0]
        path = move.jump_path
    return path


def possibleJump(color, cur_pos, parent_move, board):
    possible_jump = []
    if color in ('b', 'B'):
        enemy_color = ('w', 'W')
    else:
        enemy_color = ('b', 'B')
    for move in movement[color]:
        temp_pos = (cur_pos[0] + move[0], cur_pos[1] + move[1])
        if boundTest(temp_pos) and board.panel[temp_pos[1]][temp_pos[0]] in enemy_color:
            new_pos = (temp_pos[0] + move[0], temp_pos[1] + move[1])
            if boundTest(new_pos) and (board.panel[new_pos[1]][new_pos[0]] == '.'):
                possible_jump.append(Move(cur_pos, new_pos, parent_move, color))
    return possible_jump


def isEndJump(possible_jump, visited_skip):
    for jump in possible_jump:
        if (0.5 * (jump.cur_pos[0] + jump.new_pos[0]), 0.5 * (jump.cur_pos[1] + jump.new_pos[1])) not in visited_skip:
            return False
    return True


# find all possible jump path from start_pos to new_pos
def completeJump(board, color, start_pos, new_pos):
    stack = []
    valid_moves = []
    stack.append(Move(start_pos, new_pos, None, color))
    visited_skip = []
    jump_path = []
    skipped = []
    change_to_king_flag = 0

    while (len(stack)):
        top_move = stack.pop()
        if top_move.color == 'b' and top_move.new_pos in white_king_row:
            top_move.color = 'B'
            change_to_king_flag = 1
        if top_move.color == 'w' and top_move.new_pos in black_king_row:
            top_move.color = 'W'
            change_to_king_flag = 1
        possible_jump = possibleJump(top_move.color, top_move.new_pos, top_move, board)
        skip = (0.5 * (top_move.cur_pos[0] + top_move.new_pos[0]), 0.5 * (top_move.cur_pos[1] + top_move.new_pos[1]))
        visited_skip.append(skip)
        flag = 0

        if len(possible_jump) == 0 or isEndJump(possible_jump, visited_skip) or change_to_king_flag:
            temp = top_move
            while (temp.parent):
                temp_skip = (
                    0.5 * (temp.new_pos[0] + temp.parent.new_pos[0]), 0.5 * (temp.new_pos[1] + temp.parent.new_pos[1]))
                jump_path.append(temp.new_pos)
                skipped.append(temp_skip)
                if len(stack) and temp.cur_pos == stack[-1].cur_pos:
                    visited_skip = [x for x in visited_skip if x not in skipped]
                temp = temp.parent
            jump_path.append(temp.new_pos)
            jump_path.append(temp.cur_pos)
            skipped.append((0.5 * (start_pos[0] + temp.new_pos[0]), 0.5 * (start_pos[1] + temp.new_pos[1])))
            jump_path.reverse()
            skipped.reverse()
            if len(skipped) == 1 and skipped[0][0] % 1 != 0:
                skipped = []
            if top_move.color != color:
                color_change = True
            else:
                color_change = False
            valid_moves.append(jumpMove(start_pos, top_move.new_pos, jump_path, skipped, color_change))
            jump_path = []
            skipped = []
            flag = 1
            possible_jump = []
        if flag == 0:
            for jump in possible_jump:
                if (0.5 * (jump.cur_pos[0] + jump.new_pos[0]), 0.5 * (jump.cur_pos[1] + jump.new_pos[1])) not in visited_skip:
                    stack.append(jump)

    return valid_moves


def getAllPossibleMove(board, max_player_color):
    if max_player_color in ('b', 'B'):
        max_player_position = board.black_pos
        max_player_king_position = board.black_king_pos
    else:
        max_player_position = board.white_pos
        max_player_king_position = board.white_king_pos

    max_player_all = max_player_position
    max_player_all.extend(max_player_king_position)
    possible_moves = []
    if max_player_color in ('b', 'B'):
        enemy_color = ('w', 'W')
    else:
        enemy_color = ('b', 'B')
    #     jump
    for choose in max_player_all:
        if choose in max_player_king_position:
            temp_color = max_player_color.upper()
        else:
            temp_color = max_player_color
        for move in movement[temp_color]:
            temp_pos = (choose[0] + move[0], choose[1] + move[1])
            if boundTest(temp_pos) and board.panel[temp_pos[1]][temp_pos[0]] in enemy_color:
                new_pos = (temp_pos[0] + move[0], temp_pos[1] + move[1])
                if boundTest(new_pos) and board.panel[new_pos[1]][new_pos[0]] == '.':
                    possible_jumps = completeJump(board, temp_color, choose, new_pos)
                    for jump in possible_jumps:
                        possible_moves.append(jump)
    if len(possible_moves) == 0:
        for choose in max_player_all:
            if choose in max_player_king_position:
                temp_color = max_player_color.upper()
            else:
                temp_color = max_player_color
            for move in movement[temp_color]:
                new_pos = (choose[0] + move[0], choose[1] + move[1])
                if boundTest(new_pos) and board.panel[new_pos[1]][new_pos[0]] == '.':
                    if (temp_color == 'b' and new_pos in white_king_row) or (
                            temp_color == 'w' and new_pos in black_king_row):
                        possible_moves.append(jumpMove(choose, new_pos, [choose, new_pos], [], True))
                    else:
                        possible_moves.append(jumpMove(choose, new_pos, [choose, new_pos], [], False))
    return possible_moves


def gameMode(ori_board, max_player_color, time_limit, start_time):
    if max_player_color in ('b', 'B'):
        min_opponent_color = 'w'
    else:
        min_opponent_color = 'b'
    all_move = getAllPossibleMove(ori_board, max_player_color)
    if not os.path.exists('playdata.txt'):
        if time_limit > 100:
            max_depth = 5
        else:
            max_depth = 2
        with open("playdata.txt", 'w') as file2:
            file2.write(str(max_depth) + '\n')
            file2.close()
    else:
        file2 = open('playdata.txt')
        fileData2 = file2.readlines()
        max_depth = int(fileData2.pop(0).rstrip())

    time_bound = start_time + time_limit - 5
    path = []
    final_board = []
    if len(all_move) == 0:
        return path, ori_board
    resValue = float("-Inf")
    min_first_value = float("-Inf")
    for move in all_move:
        new_board = deepcopy(afterMoveBoard(move, ori_board))
        value, first_depth_value = minValue(new_board, 0, float("-Inf"), float("Inf"), min_opponent_color, max_player_color, max_depth, time_bound)
        if value > resValue or (value == resValue and first_depth_value > min_first_value):
            path = move.jump_path
            resValue = value
            final_board = new_board
            min_first_value = first_depth_value
    return path, final_board


def minValue(board, depth, alpha, beta, min_opponent_color, max_player_color, max_depth, time_bound):
    all_move = getAllPossibleMove(board, min_opponent_color)
    if time.time() >= time_bound:
        max_depth = 2
    first_depth_value = float("-Inf")
    if depth >= max_depth or gameOver(board, len(all_move)):
        return heuristic(board, max_player_color), first_depth_value
    minvalue = float("Inf")

    for move in all_move:
        new_board = deepcopy(afterMoveBoard(move, board))
        temp_value, first_depth_value = maxValue(new_board, depth + 1, alpha, beta, max_player_color, min_opponent_color, max_depth, time_bound)
        minvalue = min(minvalue, temp_value)

        if minvalue <= alpha:
            return minvalue, first_depth_value
        beta = min(minvalue, beta)
    return minvalue, first_depth_value


def maxValue(board, depth, alpha, beta, max_player_color, min_opponent_color, max_depth, time_bound):
    all_move = getAllPossibleMove(board, max_player_color)
    if time.time() >= time_bound:
        max_depth = 2
    first_depth_value = float("-Inf")
    if depth >= max_depth or gameOver(board, len(all_move)):
        return heuristic(board, max_player_color), first_depth_value
    value = float("-Inf")
    for move in all_move:
        new_board = deepcopy(afterMoveBoard(move, board))
        temp_value, first_depth_value = minValue(new_board, depth + 1, alpha, beta, min_opponent_color, max_player_color, max_depth, time_bound)
        value = max(value, temp_value)
        if max_depth >= 1 and depth == 1:
            first_depth_value = heuristic(board, max_player_color)
        if value >= beta:
            return value, first_depth_value
        alpha = max(value, alpha)
    return value, first_depth_value


def afterMoveBoard(move, board):
    panel = deepcopy(board.panel)
    if move.color_change:
        panel[move.new_pos[1]][move.new_pos[0]] = panel[move.cur_pos[1]][move.cur_pos[0]].upper()
    else:
        panel[move.new_pos[1]][move.new_pos[0]] = panel[move.cur_pos[1]][move.cur_pos[0]]
    panel[move.cur_pos[1]][move.cur_pos[0]] = '.'
    if len(move.skipped) != 0:
        for skip in move.skipped:
            panel[int(skip[1])][int(skip[0])] = '.'
    new_board = Board(panel)
    return new_board


def gameOver(board, length):
    if board.black_count == 0 or board.white_count == 0 or length == 0:
        return True
    else:
        return False


def heuristic(board, max_player_color):
    if max_player_color in ('b', 'B'):
        if board.black_count == 0:
            return -100
        elif board.white_count == 0:
            return 100
        else:
            return board.black_count - board.white_count + (board.black_king_count - board.white_king_count)
    else:
        if board.black_count == 0:
            return 100
        elif board.white_count == 0:
            return -100
        else:
            return board.white_count - board.black_count + (board.white_king_count - board.black_king_count)


if __name__ == "__main__":
    panel = []
    inputFile = open("input.txt")
    fileData = inputFile.readlines()
    method = fileData.pop(0).rstrip()
    max_player_color = fileData.pop(0).strip()
    time_limit = float(fileData.pop(0).strip())
    start_time = time.time()
    for i in range(0, 8):
        panel.append(list(fileData.pop(0).strip()))
    ori_board = Board(panel)
    if max_player_color == "BLACK":
        max_player_color = 'b'
    else:
        max_player_color = 'w'
    path = []
    if method == "SINGLE":
        path = singleMode(ori_board, max_player_color)
    else:
        path, final_board = gameMode(ori_board, max_player_color, time_limit, start_time)
        # **************TEST*************************************************
        end_time = time.time()
        with open("input.txt", 'w') as file3:
            file3.write("GAME\n")
            # if max_player_color in ('b','B'):
            #     file3.write("WHITE\n")
            # else:
            #     file3.write("BLACK\n")
            file3.write("BLACK\n")
            rest_time = time_limit - (time.time() - start_time)
            file3.write(str(rest_time) + "\n")
            for x in range(0, 8):
                for y in range(0, 8):
                    file3.write(final_board.panel[x][y])
                file3.write("\n")
    #        ***********************************************************************
    with open("output.txt", 'w') as file:
        if len(path) != 0:
            if abs(path[1][0] - path[0][0]) > 1 or abs(path[1][1] - path[0][1] > 1):
                for i in range(len(path) - 1):
                    file.write('J ')
                    res = outPointTrans(path[i][0], path[i][1]) + " " + outPointTrans(path[i + 1][0], path[i + 1][1]) + "\n"
                    file.write(res)
            else:
                file.write('E ')
                for i in range(len(path) - 1):
                    res = outPointTrans(path[i][0], path[i][1]) + " " + outPointTrans(path[i + 1][0], path[i + 1][1]) + "\n"
                    file.write(res)
            file.close()
