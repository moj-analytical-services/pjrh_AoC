import numpy as np
import re

# Read in and process

input = [s for s in open("inputs/11-input.txt").read().split("\n") if s != ""]

input_bool = [re.sub('L', '1', s) for s in input]
input_bool = [re.sub('\.', '0', s) for s in input_bool]
input_bool = [list(s) for s in input_bool]
input_bool = np.array(input_bool).astype(int)


def pad_with(vector, pad_width, iaxis, kwargs):
    pad_value = kwargs.get('padder', 10)
    vector[:pad_width[0]] = pad_value
    vector[-pad_width[1]:] = pad_value


input_bool_pad = np.pad(input_bool, 1, pad_with, padder=0)

# Part 1

def sum_adjacent(a):
    a_up = np.roll(a, -1, axis=0)
    a_down = np.roll(a, 1, axis=0)
    a_left = np.roll(a, 1, axis=1)
    a_right = np.roll(a, -1, axis=1)
    b = a_up + a_down + a_left + a_right + np.roll(a_up, -1, axis=1) + np.roll(a_down, -1, axis=1) + np.roll(a_up, 1, axis=1) + np.roll(a_down, 1, axis=1)
    return b


p1looper = np.zeros(input_bool_pad.shape)
floor = np.zeros(input_bool_pad.shape)
floor[input_bool_pad == 0] = 1

empty_seats_step = input_bool_pad
occup_seats_step = np.zeros(input_bool_pad.shape)

go = 1
while (go):
    p1looper_prev = p1looper + 1 - 1 # why do I have to add and subtract 1 to get this to work?

    empty_seats_step[np.logical_and(p1looper == 0, floor == 0)] = 1
    occup_seats_step[np.logical_and(p1looper == 1, floor == 0)] = 1

    step = sum_adjacent(p1looper)

    p1looper[np.logical_and(empty_seats_step == 1, step == 0)] = 1
    p1looper[np.logical_and(occup_seats_step == 1, step >= 4)] = 0

    comparison = np.array_equal(p1looper, p1looper_prev)
    go = not comparison


print(sum(sum(p1looper)))

# Part 2 - warning takes a long time to run (10mins?)


def see_occseat_in_dir(seats, x_list, y_list):
    x_len = len(x_list)
    y_len = len(y_list)
    len_needed = min(x_len, y_len)
    
    x_list = x_list[:int(len_needed)]
    y_list = y_list[:int(len_needed)]
    
    view = seats[y_list, x_list]
    view_non_zeros_bool = view !=0
    if any(view_non_zeros_bool) == False:
        return(0)
    else:
        if view[view_non_zeros_bool][0] == 1:
            return(1)
        else:
            return(0)

def see_occseats_count(seat_status_arr):
    see = np.zeros(seat_status_arr.shape)
    for index in np.ndindex(seat_status_arr.shape):
        if index[0] == 0: continue
        if index[1] == 0: continue
        if index[0] == seat_status_arr.shape[0]: continue
        if index[1] == seat_status_arr.shape[1]: continue
        
        up_list_y = [x for x in reversed(range(0, index[0]))]
        up_list_x = [index[1] for x in reversed(range(0, index[0]))]
        down_list_y = [x for x in range(1 + index[0], seat_status_arr.shape[0])]
        down_list_x = [index[1] for x in range(1 + index[0], seat_status_arr.shape[0])]
        left_list_x = [x for x in reversed(range(0, index[1]))]
        left_list_y = [index[0] for x in reversed(range(0, index[1]))]
        right_list_x = [x for x in range(1 + index[1], seat_status_arr.shape[1])]
        right_list_y = [index[0] for x in range(1 + index[1], seat_status_arr.shape[1])]
    
    
        see[index] = see[index] + see_occseat_in_dir(seat_status_arr, up_list_x, up_list_y)
        see[index] = see[index] + see_occseat_in_dir(seat_status_arr, down_list_x, down_list_y)
        see[index] = see[index] + see_occseat_in_dir(seat_status_arr, left_list_x, left_list_y)
        see[index] = see[index] + see_occseat_in_dir(seat_status_arr, right_list_x, right_list_y)
        see[index] = see[index] + see_occseat_in_dir(seat_status_arr, left_list_x, up_list_y)
        see[index] = see[index] + see_occseat_in_dir(seat_status_arr, right_list_x, up_list_y)
        see[index] = see[index] + see_occseat_in_dir(seat_status_arr, left_list_x, down_list_y)
        see[index] = see[index] + see_occseat_in_dir(seat_status_arr, right_list_x, down_list_y)
        
    return(see)

# init
p1looper = np.zeros(input_bool_pad.shape)
floor = np.zeros(input_bool_pad.shape)
floor[input_bool_pad == 0] = 1



go = 1
while (go):
    p1looper_prev = p1looper + 1 - 1 # why do I have to add and subtract 1 to get this to work?

    empty_seats_step = np.zeros(input_bool_pad.shape)
    occup_seats_step = np.zeros(input_bool_pad.shape)
    empty_seats_step[np.logical_and(p1looper == 0, floor == 0)] = 1
    occup_seats_step[np.logical_and(p1looper == 1, floor == 0)] = 1
    seat_status = occup_seats_step - empty_seats_step # 1 for occupied, -1 for empty
    see_occ_seat_count = see_occseats_count(seat_status)
    p1looper[np.logical_and(empty_seats_step == 1, see_occ_seat_count == 0)] = 1
    p1looper[np.logical_and(occup_seats_step == 1, see_occ_seat_count >= 5)] = 0

    comparison = np.array_equal(p1looper, p1looper_prev)
    go = not comparison


print(sum(sum(p1looper)))
