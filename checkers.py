import math
import sys
import time

import numpy as np


def read_input(input_file):
    """ Reading input from input file. Also converts the start state from the
     input format to the output format """
    start_state = []
    with open(input_file) as file:
        level = 0
        for line in file:
            temp = []
            i = 0
            while i < 8:
                temp.append(line[i])
                i += 1
            start_state.append(temp)
            level += 1
    start_state_np = np.array(start_state)
    # print(start_state_np)
    return start_state_np


def utility_finder(state):
    """Finds the utility of the given board state"""
    red_counter = 0
    list_r = np.where(state == 'r')
    red_counter += len(list_r[0])
    list_r_king = np.where(state == 'R')
    to_add_r = 2 * len(list_r_king[0])
    red_counter += to_add_r

    black_counter = 0
    list_b = np.where(state == 'b')
    black_counter += len(list_b[0])
    list_b_king = np.where(state == 'B')
    to_add_b = 2 * len(list_b_king[0])
    black_counter += to_add_b

    utility = red_counter - black_counter

    return utility


def get_successors(state, player):
    """
    Finds all the successors to the given state.
    :param state: Current board state
    :param player: Current player (red or black)
    :return: list of new board states
    """
    successors = []
    captures = []
    r_location_list = []
    r_king_location_list = []
    b_location_list = []
    b_king_location_list = []

    if player == "red":
        raw_r_locations = np.where(state == 'r')
        raw_r_king_locations = np.where(state == 'R')
        i = 0
        while i < len(raw_r_locations[0]):
            to_append = (raw_r_locations[0][i], raw_r_locations[1][i])
            r_location_list.append(to_append)
            i += 1
        j = 0
        while j < len(raw_r_king_locations[0]):
            r_king_raw_loc = (raw_r_king_locations[0][j], raw_r_king_locations[1][j])
            r_king_location_list.append(r_king_raw_loc)
            j += 1
        # print(r_location_list)
        # print(r_king_location_list)

        for loc in r_location_list:
            row = loc[0]
            col = loc[1]

            # (CAPTURE) move over b or B on up left (no other piece in up left space over b or B, no 2nd to left col, no 2nd to top row) (for r and R)
            # (CAPTURE) move over b or B on up right (no other piece in up right space over b or B, no 2nd to right col, no 2nd to top row) (for r and R)
            # if after capture by r or R, there is a b or B to the left or right up of r or R, move over the b or B
            # (no piece in the space over b or B, no 2nd to left col for left diag,
            #  no 2nd to right col for right diag, no 2nd to top row for both left and right diag)
            if ((col >= 2) and (row >= 2) and ((state[row - 1][col - 1] == 'b') or (state[row - 1][col - 1] == 'B')) and (state[row - 2][col - 2] == '.')) or \
                    ((col <= 5) and (row >= 2) and ((state[row - 1][col + 1] == 'b') or (state[row - 1][col + 1] == 'B')) and (state[row - 2][col + 2] == '.')):
                capture_result = capture_b(state, row, col, 'r')
                # print("Capture start")
                # for cr in capture_result:
                #     print(cr)
                # print("Capture over")
                # successors.extend(capture_result)
                captures.extend(capture_result)
                # successors.append(capture_b(state, row, col, 'r'))

            if len(captures) == 0:
                # move one space up left (No top row, no left col, no other piece on left up) (for r, R and B)
                if (col != 0) and (state[row-1][col-1] == '.'):
                    successors.append(move_up_left(state, row, col, 'r'))

                # move one space up right (No top row, no right col, no piece on right) (for r, R and B)
                if (col != 7) and (state[row-1][col+1] == '.'):
                    successors.append(move_up_right(state, row, col, 'r'))

        for rk_loc in r_king_location_list:
            rk_row = rk_loc[0]
            rk_col = rk_loc[1]

            # (CAPTURE) move over b or B on up left (no other piece in up left space over b or B, no 2nd to left col, no 2nd to top row) (for r and R)
            # (CAPTURE) move over b or B on up right (no other piece in up right space over b or B, no 2nd to right col, no 2nd to top row) (for r and R)
            # (CAPTURE) move over b or B on down left (no other piece in down left space over b or B, no 2nd to bottom row, no 2nd to left col) (for R)
            # (CAPTURE) move over b or B on down right (no other piece in down right space over b or B, no 2nd to bottom row, no 2nd to right col) (for R)
            # if after capture by r or R, there is a b or B to the left or right up of r or R, move over the b or B
            # (no piece in the space over b or B, no 2nd to left col for left diag,
            #  no 2nd to right col for right diag, no 2nd to top row for both left and right diag)
            if ((rk_col >= 2) and (rk_row >= 2) and ((state[rk_row - 1][rk_col - 1] == 'b') or (state[rk_row - 1][rk_col - 1] == 'B')) and (state[rk_row - 2][rk_col - 2] == '.')) or\
                    ((rk_col <= 5) and (rk_row >= 2) and ((state[rk_row - 1][rk_col + 1] == 'b') or (state[rk_row - 1][rk_col + 1] == 'B')) and (state[rk_row - 2][rk_col + 2] == '.')) or\
                    ((rk_col >= 2) and (rk_row <= 5) and ((state[rk_row + 1][rk_col - 1] == 'b') or (state[rk_row + 1][rk_col - 1] == 'B')) and (state[rk_row + 2][rk_col - 2] == '.')) or\
                    ((rk_col <= 5) and (rk_row <= 5) and ((state[rk_row + 1][rk_col + 1] == 'b') or (state[rk_row + 1][rk_col + 1] == 'B')) and (state[rk_row + 2][rk_col + 2] == '.')):
                capture_result = king_capture(state, rk_row, rk_col, 'R')
                # print("Capture start")
                # for cr in capture_result:
                #     print(cr)
                # print("Capture over")
                # successors.extend(capture_result)
                captures.extend(capture_result)
                # successors.append(capture_b(state, row, col, 'r'))

            if len(captures) == 0:
                # move one space up left (No top row, no left col, no other piece on left up) (for r, R and B)
                if (rk_row != 0) and (rk_col != 0) and (
                        state[rk_row - 1][rk_col - 1] == '.'):
                    successors.append(move_up_left(state, rk_row, rk_col, 'R'))

                # move one space up right (No top row, no right col, no piece on right) (for r, R and B)
                if (rk_row != 0) and (rk_col != 7) and (
                        state[rk_row - 1][rk_col + 1] == '.'):
                    successors.append(move_up_right(state, rk_row, rk_col, 'R'))

                # move one space down left (No bottom row, no left col, no other piece on left down) (for b, R and B)
                if (rk_col != 0) and (rk_row != 7) and (state[rk_row+1][rk_col-1] == '.'):
                    successors.append(move_down_left(state, rk_row, rk_col, 'R'))

                # move one space down right (No bottom row, no right col, no other piece on right down) (for b, R and B)
                if (rk_col != 7) and (rk_row != 7) and (state[rk_row+1][rk_col+1] == '.'):
                    successors.append(move_down_right(state, rk_row, rk_col, 'R'))

    elif player == "black":
        raw_b_locations = np.where(state == 'b')
        raw_b_king_locations = np.where(state == 'B')
        ptr = 0
        while ptr < len(raw_b_locations[0]):
            to_append = (raw_b_locations[0][ptr], raw_b_locations[1][ptr])
            b_location_list.append(to_append)
            ptr += 1
        ptr2 = 0
        while ptr2 < len(raw_b_king_locations[0]):
            b_king_raw_loc = (raw_b_king_locations[0][ptr2], raw_b_king_locations[1][ptr2])
            b_king_location_list.append(b_king_raw_loc)
            ptr2 += 1

        for b_loc in b_location_list:
            b_row = b_loc[0]
            b_col = b_loc[1]

            # (CAPTURE) move over r or R on down left (no other piece in down left space over r or R, no 2nd to bottom row, no 2nd to left col) (for b and B)
            # (CAPTURE) move over r or R on down right (no other piece in down right space over r or R, no 2nd to bottom row, no 2nd to right col) (for b and B)
            if ((b_col >= 2) and (b_row <= 5) and ((state[b_row + 1][b_col - 1] == 'r') or (state[b_row + 1][b_col - 1] == 'R')) and (state[b_row + 2][b_col - 2] == '.')) or \
                    ((b_col <= 5) and (b_row <= 5) and ((state[b_row + 1][b_col + 1] == 'r') or (state[b_row + 1][b_col + 1] == 'R')) and (state[b_row + 2][b_col + 2] == '.')):
                capture_result = capture_r(state, b_row, b_col, 'b')
                # print("Capture start")
                # for cr in capture_result:
                #     print(cr)
                # print("Capture over")
                # successors.extend(capture_result)
                captures.extend(capture_result)

            if len(captures) == 0:
                # move one space down left (No bottom row, no left col, no other piece on left down) (for b, R and B)
                if (b_col != 0) and (state[b_row + 1][b_col - 1] == '.'):
                    successors.append(move_down_left(state, b_row, b_col, 'b'))

                # move one space down right (No bottom row, no right col, no other piece on right down) (for b, R and B)
                if (b_col != 7) and (state[b_row + 1][b_col + 1] == '.'):
                    successors.append(move_down_right(state, b_row, b_col, 'b'))

        for bk_loc in b_king_location_list:
            bk_row = bk_loc[0]
            bk_col = bk_loc[1]

            # (CAPTURE) move over r or R on up left (no other piece in up left space over r or R, no 2nd to left col, no 2nd to top row) (for B)
            # (CAPTURE) move over r or R on up right (no other piece in up right space over r or R, no 2nd to right col, no 2nd to top row) (for B)
            # (CAPTURE) move over r or R on down left (no other piece in down left space over r or R, no 2nd to bottom row, no 2nd to left col) (for b and B)
            # (CAPTURE) move over r or R on down right (no other piece in down right space over r or R, no 2nd to bottom row, no 2nd to right col) (for b and B)
            if ((bk_col >= 2) and (bk_row >= 2) and ((state[bk_row - 1][bk_col - 1] == 'r') or (state[bk_row - 1][bk_col - 1] == 'R')) and (state[bk_row - 2][bk_col - 2] == '.')) or \
                    ((bk_col <= 5) and (bk_row >= 2) and ((state[bk_row - 1][bk_col + 1] == 'r') or (state[bk_row - 1][bk_col + 1] == 'R')) and (state[bk_row - 2][bk_col + 2] == '.')) or \
                    ((bk_col >= 2) and (bk_row <= 5) and ((state[bk_row + 1][bk_col - 1] == 'r') or (state[bk_row + 1][bk_col - 1] == 'B')) and (state[bk_row + 2][bk_col - 2] == '.')) or \
                    ((bk_col <= 5) and (bk_row <= 5) and ((state[bk_row + 1][bk_col + 1] == 'r') or (state[bk_row + 1][bk_col + 1] == 'R')) and (state[bk_row + 2][bk_col + 2] == '.')):
                capture_result = king_capture(state, bk_row, bk_col, 'B')
                # print("Capture start")
                # for cr in capture_result:
                #     print(cr)
                # print("Capture over")
                # successors.extend(capture_result)
                captures.extend(capture_result)
                # successors.append(capture_b(state, row, col, 'r'))

            if len(captures) == 0:
                # move one space up left (No top row, no left col, no other piece on left up) (for r, R and B)
                if (bk_row != 0) and (bk_col != 0) and (
                        state[bk_row - 1][bk_col - 1] == '.'):
                    successors.append(move_up_left(state, bk_row, bk_col, 'B'))

                # move one space up right (No top row, no right col, no piece on right) (for r, R and B)
                if (bk_row != 0) and (bk_col != 7) and (
                        state[bk_row - 1][bk_col + 1] == '.'):
                    successors.append(move_up_right(state, bk_row, bk_col, 'B'))

                # move one space down left (No bottom row, no left col, no other piece on left down) (for b, R and B)
                if (bk_row != 7) and (bk_col != 0) and (
                        state[bk_row + 1][bk_col - 1] == '.'):
                    successors.append(
                        move_down_left(state, bk_row, bk_col, 'B'))

                # move one space down right (No bottom row, no right col, no other piece on right down) (for b, R and B)
                if (bk_row != 7) and (bk_col != 7) and (
                        state[bk_row + 1][bk_col + 1] == '.'):
                    successors.append(
                        move_down_right(state, bk_row, bk_col, 'B'))
    if len(captures) == 0:
        return successors
    else:
        return captures


def move_down_left(state, row, col, piece):
    new_state = np.copy(state)
    if piece == 'b':
        if row + 1 == 7:
            new_state[row + 1][col - 1] = 'B'
        else:
            new_state[row + 1][col - 1] = piece
    else:
        new_state[row + 1][col - 1] = piece
    new_state[row][col] = '.'
    # if piece == 'B':
    #     print(new_state)
    return new_state


def move_down_right(state, row, col, piece):
    new_state = np.copy(state)
    if piece == 'b':
        if row + 1 == 7:
            new_state[row + 1][col + 1] = 'B'
        else:
            new_state[row + 1][col + 1] = piece
    else:
        new_state[row + 1][col + 1] = piece
    new_state[row][col] = '.'
    # if piece == 'B':
    #     print(new_state)
    return new_state


def capture_r(state, row, col, piece) -> list:
    successors = []
    if row + 2 > 7:
        return [state]
    if col - 2 < 0:
        if (state[row + 1][col + 1] != 'r') and (state[row + 1][col + 1] != 'R'):
            return [state]
        elif state[row+2][col+2] != '.':
            return [state]
    if col + 2 > 7:
        if (state[row + 1][col - 1] != 'r') and (state[row + 1][col - 1] != 'R'):
            return [state]
        elif state[row+2][col-2] != '.':
            return [state]
    if (6 > col > 1) and ((state[row + 1][col - 1] != 'r') and (
            state[row + 1][col - 1] != 'R')) and (
            (state[row + 1][col + 1] != 'r') and (
            state[row + 1][col + 1] != 'R')):
        return [state]
    if (6 > col > 1) and (state[row + 2][col - 2] != '.') and (state[row + 2][col + 2] != '.'):
        return [state]
    else:
        if (col >= 2) and (row <= 5) and ((state[row + 1][col - 1] == 'r') or (
                state[row + 1][col - 1] == 'R')) and (
                state[row + 2][col - 2] == '.'):
            new_state_1 = np.copy(state)
            new_piece = 'b'
            if piece == 'b':
                if row + 2 == 7:
                    new_state_1[row + 2][col - 2] = 'B'
                    new_piece = 'B'
                else:
                    new_state_1[row + 2][col - 2] = piece
            else:
                new_state_1[row + 2][col - 2] = piece
            new_state_1[row][col] = '.'
            new_state_1[row + 1][col - 1] = '.'
            # successors.append(new_state_1)
            multi_capture_1 = capture_r(new_state_1, row + 2, col - 2,
                                        new_piece)
            successors.extend(multi_capture_1)
        if (col <= 5) and (row <= 5) and ((state[row + 1][col + 1] == 'r') or (
                state[row + 1][col + 1] == 'R')) and (
                state[row + 2][col + 2] == '.'):
            new_state_2 = np.copy(state)
            new_piece = 'b'
            if piece == 'b':
                if row + 2 == 7:
                    new_state_2[row + 2][col + 2] = 'B'
                    new_piece = 'B'
                else:
                    new_state_2[row + 2][col + 2] = piece
            else:
                new_state_2[row + 2][col + 2] = piece
            new_state_2[row][col] = '.'
            new_state_2[row + 1][col + 1] = '.'
            # successors.append(new_state_2)
            multi_capture_2 = capture_r(new_state_2, row + 2, col + 2,
                                        new_piece)
            successors.extend(multi_capture_2)
        return successors


def capture_b(state, row, col, piece) -> list:
    successors = []
    if row - 2 < 0:
        return [state]
    if col - 2 < 0:
        if (state[row - 1][col + 1] != 'b') and (state[row - 1][col + 1] != 'B'):
            return [state]
        elif state[row-2][col+2] != '.':
            return [state]
    if col + 2 > 7:
        if (state[row - 1][col - 1] != 'b') and (state[row - 1][col - 1] != 'B'):
            return [state]
        elif state[row-2][col-2] != '.':
            return [state]
    if (6 > col > 1) and ((state[row - 1][col - 1] != 'b') and (
            state[row - 1][col - 1] != 'B')) and (
            (state[row - 1][col + 1] != 'b') and (
            state[row - 1][col + 1] != 'B')):
        return [state]
    if (6 > col > 1) and (state[row - 2][col - 2] != '.') and (state[row - 2][col + 2] != '.'):
        return [state]
    else:
        if (col >= 2) and (row >= 2) and ((state[row - 1][col - 1] == 'b') or (
                state[row - 1][col - 1] == 'B')) and (
                state[row - 2][col - 2] == '.'):
            new_state_1 = np.copy(state)
            new_piece = 'r'
            if piece == 'r':
                if row - 2 == 0:
                    new_state_1[row - 2][col - 2] = 'R'
                    new_piece = 'R'
                else:
                    new_state_1[row - 2][col - 2] = piece
            else:
                new_state_1[row - 2][col - 2] = piece
            new_state_1[row][col] = '.'
            new_state_1[row - 1][col - 1] = '.'
            # successors.append(new_state_1)
            multi_capture_1 = capture_b(new_state_1, row - 2, col - 2,
                                        new_piece)
            successors.extend(multi_capture_1)
        if (col <= 5) and (row >= 2) and ((state[row - 1][col + 1] == 'b') or (
                state[row - 1][col + 1] == 'B')) and (
                state[row - 2][col + 2] == '.'):
            new_state_2 = np.copy(state)
            new_piece = 'r'
            if piece == 'r':
                if row - 2 == 0:
                    new_state_2[row - 2][col + 2] = 'R'
                    new_piece = 'R'
                else:
                    new_state_2[row - 2][col + 2] = piece
            else:
                new_state_2[row - 2][col + 2] = piece
            new_state_2[row][col] = '.'
            new_state_2[row - 1][col + 1] = '.'
            # successors.append(new_state_2)
            multi_capture_2 = capture_b(new_state_2, row - 2, col + 2,
                                        new_piece)
            successors.extend(multi_capture_2)
        return successors


def king_capture(state, row, col, piece):
    successors = []
    if piece == 'B':
        to_capture = 'r'
        king_to_capture = 'R'
    else:
        to_capture = 'b'
        king_to_capture = 'B'
    if row - 2 < 0:
        if col >= 6:
            if (state[row+1][col-1] != to_capture) and (state[row+1][col-1] != king_to_capture):
                return [state]
            elif state[row+2][col-2] != '.':
                return [state]
        elif col <= 1:
            if (state[row+1][col+1] != to_capture) and (state[row+1][col+1] != king_to_capture):
                return [state]
            elif state[row+2][col+2] != '.':
                return [state]
        else:
            if (state[row+1][col-1] != to_capture) and\
                    (state[row+1][col-1] != king_to_capture) and\
                    (state[row+1][col+1] != to_capture) and\
                    (state[row+1][col+1] != king_to_capture):
                return [state]
            elif ((state[row+1][col-1] == to_capture) or (state[row+1][col-1] == king_to_capture)) and (state[row+2][col-2] != '.'):
                return [state]
            elif ((state[row+1][col+1] == to_capture) or (state[row+1][col+1] == king_to_capture)) and (state[row+2][col+2] != '.'):
                return [state]
    if row + 2 > 7:
        if col <= 1:
            if (state[row-1][col+1] != to_capture) and (state[row-1][col+1] != king_to_capture):
                return [state]
            elif state[row-2][col+2] != '.':
                return [state]
        elif col >= 6:
            if (state[row-1][col-1] != to_capture) and (state[row-1][col-1] != king_to_capture):
                return [state]
            elif state[row-2][col-2] != '.':
                return [state]
        else:
            if (state[row-1][col+1] != to_capture) and \
                    (state[row-1][col+1] != king_to_capture) and \
                    (state[row-1][col-1] != to_capture) and \
                    (state[row-1][col-1] != king_to_capture):
                return [state]
            elif ((state[row-1][col+1] == to_capture) or (state[row-1][col+1] == king_to_capture)) and state[row-2][col+2] != '.':
                return [state]
            elif ((state[row-1][col-1] == to_capture) or (state[row-1][col-1] == king_to_capture)) and state[row-2][col-2] != '.':
                return [state]
    if (6 > row > 1) and col - 2 < 0:
        if (state[row+1][col+1] != to_capture) and\
                (state[row+1][col+1] != king_to_capture) and\
                (state[row-1][col+1] != to_capture) and\
                (state[row-1][col+1] != king_to_capture):
            return [state]
        elif ((state[row+1][col+1] == to_capture) or (state[row+1][col+1] == king_to_capture)) and (state[row + 2][col + 2] != '.'):
            return [state]
        elif ((state[row-1][col+1] == to_capture) or (state[row-1][col+1] == king_to_capture)) and (state[row-2][col+2] != '.'):
            return [state]

    if (6 > row > 1) and col + 2 > 7:
        if (state[row+1][col-1] != to_capture) and \
                (state[row+1][col-1] != king_to_capture) and \
                (state[row-1][col-1] != to_capture) and \
                (state[row-1][col-1] != king_to_capture):
            return [state]
        elif ((state[row+1][col-1] == to_capture) or (state[row+1][col-1] == king_to_capture)) and (state[row + 2][col - 2] != '.'):
            return [state]
        elif ((state[row-1][col-1] == to_capture) or (state[row-1][col-1] == king_to_capture)) and (state[row-2][col-2] != '.'):
            return [state]

    if (6 > row > 1) and (6 > col > 1) and (state[row - 1][col - 1] != to_capture) and\
            (state[row - 1][col - 1] != king_to_capture) and\
            (state[row - 1][col + 1] != to_capture) and (state[row - 1][col + 1] != king_to_capture) and\
            (state[row + 1][col - 1] != to_capture) and (state[row + 1][col - 1] != king_to_capture) and\
            (state[row + 1][col + 1] != to_capture) and (state[row + 1][col + 1] != king_to_capture):
        return [state]

    if (6 > row > 1) and (6 > col > 1) and (state[row - 2][col - 2] != '.') and (state[row - 2][col + 2] != '.')\
            and (state[row+2][col-2] != '.') and (state[row+2][col+2] != '.'):
        return [state]

    else:
        if (col >= 2) and (row >= 2) and ((state[row - 1][col - 1] == to_capture) or (
                state[row - 1][col - 1] == king_to_capture)) and (
                state[row - 2][col - 2] == '.'):
            new_state_1 = np.copy(state)
            new_state_1[row - 2][col - 2] = piece
            new_state_1[row][col] = '.'
            new_state_1[row - 1][col - 1] = '.'
            # successors.append(new_state_1)
            multi_capture_1 = king_capture(new_state_1, row - 2, col - 2, piece)
            successors.extend(multi_capture_1)
        if (col >= 2) and (row <= 5) and \
                ((state[row+1][col-1] == to_capture) or (state[row+1][col-1] == king_to_capture)) and \
                (state[row+2][col-2] == '.'):
            new_state_2 = np.copy(state)
            new_state_2[row + 2][col - 2] = piece
            new_state_2[row][col] = '.'
            new_state_2[row + 1][col - 1] = '.'
            # successors.append(new_state_1)
            multi_capture_2 = king_capture(new_state_2, row + 2, col - 2, piece)
            successors.extend(multi_capture_2)
        if (col <= 5) and (row >= 2) and ((state[row - 1][col + 1] == to_capture) or (
                state[row - 1][col + 1] == king_to_capture)) and (
                state[row - 2][col + 2] == '.'):
            new_state_3 = np.copy(state)
            new_state_3[row-2][col+2] = piece
            new_state_3[row][col] = '.'
            new_state_3[row-1][col+1] = '.'
            multi_capture_3 = king_capture(new_state_3, row-2, col+2, piece)
            successors.extend(multi_capture_3)
        if (col <= 5) and (row <= 5) and\
                ((state[row + 1][col+1] == to_capture) or (state[row+1][col+1] == king_to_capture)) and\
                (state[row+2][col+2] == '.'):
            new_state_4 = np.copy(state)
            new_state_4[row+2][col+2] = piece
            new_state_4[row][col] = '.'
            new_state_4[row+1][col+1] = '.'
            multi_capture_4 = king_capture(new_state_4, row+2, col+2, piece)
            successors.extend(multi_capture_4)
        return successors


def move_up_right(state, row, col, piece):
    new_state = np.copy(state)
    if piece == 'r':
        if row-1 == 0:
            new_state[row-1][col+1] = 'R'
        else:
            new_state[row-1][col+1] = piece
    else:
        new_state[row-1][col+1] = piece
    new_state[row][col] = '.'
    # print(new_state)
    return new_state


def move_up_left(state, row, col, piece):
    """
    Move current piece one space up to the left.
    :param state: current state
    :param row: current row
    :param col: current column
    :param piece: 'r', 'b', 'R', 'B'
    :return: new state
    """
    new_state = np.copy(state)
    if piece == 'r':
        if row-1 == 0:
            new_state[row-1][col-1] = 'R'
        else:
            new_state[row - 1][col - 1] = piece
    else:
        new_state[row - 1][col - 1] = piece
    new_state[row][col] = '.'
    # print(new_state)
    return new_state


def minimax(state, player, depth):
    best_state = None
    next_state = None
    value = None
    next_val = None
    if depth != 0:
        successors = get_successors(state, player)
    else:
        successors = []
    if len(successors) == 0:
        # print(best_state, utility_finder(state))
        return best_state, utility_finder(state)
    if player == "red":
        value = -math.inf
    if player == "black":
        value = math.inf
    for suc in successors:
        if player == "red":
            next_state, next_val = minimax(suc, "black", depth - 1)
        elif player == "black":
            next_state, next_val = minimax(suc, "red", depth - 1)
        if player == "red" and value < next_val:
            value, best_state = next_val, suc
        elif player == "black" and value > next_val:
            value, best_state = next_val, suc
    # print(best_state, value)
    return best_state, value


def alphabeta(state, player, depth, alpha, beta) -> tuple:
    best_state = None
    next_state = None
    value = None
    next_val = None
    if depth != 0:
        successors = get_successors(state, player)
    else:
        successors = []
    if len(successors) == 0:
        return best_state, utility_finder(state)
    if player == "red":
        value = -math.inf
    elif player == "black":
        value = math.inf
    for suc in successors:
        if player == "red":
            next_state, next_val = alphabeta(suc, "black", depth - 1, alpha, beta)
        elif player == "black":
            next_state, next_val = alphabeta(suc, "red", depth - 1, alpha, beta)
        if player == "red":
            if value < next_val:
                value, best_state = next_val, suc
            if value >= beta:
                # print("pruned")
                return best_state, value
            alpha = max(alpha, value)
        if player == "black":
            if value > next_val:
                value, best_state = next_val, suc
            if value <= alpha:
                # print("pruned")
                return best_state, value
            beta = min(beta, value)
    return best_state, value


def generate_output_file(state, output_file):
    file = open(output_file, "w")
    i = 0
    j = 0
    while i < 8:
        while j < 8:
            file.write(state[i][j])
            j += 1
        file.write('\n')
        j = 0
        i += 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # start_time = time.time()
    # begin_state = read_input("input1.txt")
    # # print(utility_finder(begin_state))
    # # # print("Red Successors")
    # # # get_successors(begin_state, "red")
    # # # print("Black Successors")
    # # # get_successors(begin_state, "black")
    # # # result = minimax(begin_state, "red", 7)
    # result = alphabeta(begin_state, "red", 15, -math.inf, math.inf)
    # # print(type(result[0]))
    # # result_state = result[0]
    # end_time = time.time()
    # elapsed = end_time - start_time
    # print(result[0])
    # print('Time taken:', elapsed)

    # TODO: Uncomment before submission!!!!!
    begin_file = sys.argv[1]
    end_file = sys.argv[2]
    begin_state = read_input(begin_file)
    res = alphabeta(begin_state, "red", 12, -math.inf, math.inf)
    # res = minimax(begin_state, "red", 6)
    generate_output_file(res[0], end_file)
