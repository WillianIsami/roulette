from typing import Sequence
from functools import reduce
from operator import add
from dataclasses import dataclass

DEFAULT_NUMBERS = (
    0,
    32,
    15,
    19,
    4,
    21,
    2,
    25,
    17,
    34,
    6,
    27,
    13,
    36,
    11,
    30,
    8,
    23,
    10,
    5,
    24,
    16,
    33,
    1,
    20,
    14,
    31,
    9,
    22,
    18,
    29,
    7,
    28,
    12,
    35,
    3,
    26,
)

DEFAULT_RED_NUMBERS = tuple(DEFAULT_NUMBERS[1::2])
DEFAULT_BLACK_NUMBERS = tuple(DEFAULT_NUMBERS[2::2])


def number_to_xy(number):
    col = (number - 1) // 3
    lin = (number - 1) % 3
    return col, lin

def distance_2d(a, b):
    p = tuple_sub(a, b)
    return (p[0] ** 2 + p[1] ** 2) ** 0.5


def tuple_sub(a, b):
    return tuple(
        a_item - b_item
        for a_item, b_item
        in zip(a, b)
    )

def street_verify(arr):
    arr.sort()
    len_verify = len(arr) == 3
    multiply_three_verify = max(arr) % 3 == 0
    number_col_verify = (arr[-2] == arr[-1]-1) and (arr[-3] == arr[-1]-2)
    result = len_verify and multiply_three_verify and number_col_verify
    if not (result):
        raise InvalidBet
    return arr

def check_corner_condition(modOne, modTwo):
    conditions = {
        0: 2,
        1: 2,
        2: True
    }
    if conditions.get(modOne) is True:
        return True
    return conditions.get(modOne) == modTwo

def check_difference(max_value, min_value, diff_num):
    return max_value - min_value == diff_num


class InvalidBet(Exception):
    pass


@dataclass
class BetFactory:

    def create_from_str(self, value: float, raw_str):
        numbers = set(map(int, raw_str.split(',')))
        positions = list(map(number_to_xy, numbers))
        total_distance = distance_2d(max(positions), min(positions))
        if total_distance > 1:
            raise InvalidBet
        return Bet(value=0, numbers=numbers)


@dataclass
class Bet:
    value: float
    numbers: Sequence[int]

    @classmethod
    def create_black(cls, value: float):
        return cls(value=value, numbers=set(DEFAULT_BLACK_NUMBERS))

    @classmethod
    def create_red(cls, value: float):
        return cls(value=value, numbers=set(DEFAULT_RED_NUMBERS))

    @classmethod
    def create_from_filter(cls, value: float, fn):
        return cls(
            value=value,
            numbers=set(filter(fn, DEFAULT_NUMBERS[1:]))
        )

    @classmethod
    def create_odd(cls, value: float):
        return cls.create_from_filter(value, lambda it: it % 2 == 1)

    @classmethod
    def create_even(cls, value: float):
        return cls.create_from_filter(value, lambda it: it % 2 == 0)
    
    @classmethod 
    def create_line(cls, value: float, result_mod):
        return cls.create_from_filter(value, lambda it: it % 3 == result_mod)

    @classmethod
    def create_from_range(cls, value: float, range):
        return cls(value, set(range))

    @classmethod
    def create_low(cls, value):
        return cls.create_from_range(value, range(1, 19))
    
    @classmethod
    def create_high(cls, value):
        return cls.create_from_range(value, range(19, 37))

    @classmethod
    def create_first_dozen(cls, value):
        return cls.create_from_range(value, range(1,13))
    
    @classmethod
    def create_second_dozen(cls, value):
        return cls.create_from_range(value, range(13,25))
    
    @classmethod
    def create_third_dozen(cls, value):
        return cls.create_from_range(value, range(25,37))

    @classmethod
    def create_street(cls, value, street):
        return cls(
            value,
            street_verify(street)
        )
    
    @classmethod
    def create_two_street(cls, value, lst):
        lst.sort()
        max_value, min_value =  max(lst), \
                                min(lst)
        modules_max_min_values = max_value % 3 == 0 and \
                                 min_value % 3 == 1
        lst_equal_two_street = lst == [i for i in range(min_value, max_value+1)]
        if lst_equal_two_street and modules_max_min_values and len(lst) == 6:
            return cls(
                value,
                lst
            )
        raise InvalidBet

    @classmethod
    def create_corner(cls, value, lst):
        max_value, min_value = max(lst), min(lst)
        lst = sorted(list(set(lst)))
        copy_lst = list(map(lambda it: it%3, lst))
        if len(copy_lst) != 4:
            raise InvalidBet
        copy_lst.sort()
        num_one_two_same_line, num_three_four_same_line =  (copy_lst[0] == copy_lst[1],
                                                            copy_lst[2] == copy_lst[3])
        same_line = num_one_two_same_line and \
                    num_three_four_same_line
        max_minus_min = check_difference(max_value, min_value, 4)
        verify_line = check_corner_condition(copy_lst[0], copy_lst[2])
        if same_line and max_minus_min and verify_line:
            return cls(
                value, 
                lst
            )
        raise InvalidBet


class Roleta:
    
    def spin_wheel(self):
        ...

    def get_current_number(self):
        ...

    def access_history(self):
        ...

    
class Player:

    def update_balance(self):
        ...

    def list_of_bets(self):
        ...
