# from unittest import TestCase
from django.test import TestCase
from roulette_api.roulette import Bet, BetFactory, InvalidBet, number_to_xy
from random import sample, choice
from itertools import chain


def gen_bet_numbers(size):
    return sample(range(0, 37), k=size)

def all_two_horizontal():
    for l in range(3):
        yield from zip(range(1 + l, 32 + l, 3), range(4 + l, 35 + l, 3))

def all_two_vertical():
    for c in range(0, 35, 3):
        yield c + 1, c + 2
        yield c + 2, c + 3

def all_two():
    return chain(all_two_horizontal(), all_two_vertical())

def gen_all_four_corners():
    for i in range(0, 32, 3):
        yield (i + 1, i + 4, i + 2, i + 5)
    for i in range(1, 33, 3):
        yield (i + 1, i + 4, i + 2, i + 5)


class MatrizTest(TestCase):

    def test_to_xy(self):
        dataset = {
            1: (0, 0),
            2: (0, 1),
            3: (0, 2),
            15: (4, 2),
            16: (5, 0),
            20: (6, 1),
            34: (11, 0),
            35: (11, 1),
            36: (11, 2),
        }
        for input, expected in dataset.items():
            with self.subTest(f"Position of {input} == {expected}"):
                result = number_to_xy(input)
                self.assertEqual(result, expected)


class BetTest(TestCase):

    def setUp(self) -> None:
        self.factory = BetFactory()

    def test_convert_user_input_just_a_number(self):
        dataset = dict(
            (str(number), {number})
            for number in range(0, 37)
        )
        for input, expected in dataset.items():
            with self.subTest(f"Convert {input} to {expected}"):
                bet = self.factory.create_from_str(0, input)
                self.assertIsInstance(bet, Bet)
                self.assertEqual(bet.numbers, expected)

    def test_convert_user_input_double_numbers(self):
        dataset = dict(
            (','.join(map(str, numbers)), set(numbers))
            for numbers in all_two()
        )
        for input, expected in dataset.items():
            with self.subTest(f"Convert {input} to {expected}"):
                bet = self.factory.create_from_str(0, input)
                self.assertIsInstance(bet, Bet)
                self.assertEqual(bet.numbers, expected)

    def test_error_when_not_neighbor(self):
        dataset = (
            '5,11',
            '16,22',
            '2,6',
            '0,36',
            '1,7',
            '18,19',
        )
        for input in dataset:
            with self.subTest(f"Check error for {input}"):
                with self.assertRaises(InvalidBet):
                    self.factory.create_from_str(0, input)

    def test_error_street(self):
        dataset = (
            [2,3,4],
            [1,2,4],
            [1,1,1],
            [1,3,3],
            [9,10,11],
            [1,1,2,3],
            [16,15,14],
            [18,19,20],
            [23,24,21]
        )
        for input in dataset:
            with self.subTest(f"Check error for {input} street bet"):
                with self.assertRaises(InvalidBet):
                    bet = Bet.create_street(100., input)
                    self.assertIsInstance(bet, Bet)
                    self.assertEqual(bet.numbers, input)

    def test_error_two_street(self):
        dataset = (
            [2,3,4,5,6,7],
            [1,2,4,7,8,9],
            [1,1,1,6,6,6],
            [1,3,3,4,5,6],
            [13,14,15,16,16,18],
            [19,20,21,22,24,24],
            [4,5,6,10,11,12],
            [10,11,12,13,14,15,16,17,18],
            [25,26,27,28,29,33]
        )
        for input in dataset:
            with self.subTest(f"Check error for {input} two street bet"):
                with self.assertRaises(InvalidBet):
                    bet = Bet.create_two_street(100., input)
                    self.assertIsInstance(bet, Bet)
                    self.assertEqual(bet.numbers, input)

    def test_error_when_not_corner_bet(self):
        dataset = (
            [1,2,7,8],
            [10,11,4,5],
            [13,18,20,23],
            [14,29,30,13],
            [2,3,8,9],
            [9,10,12,13],
            [2,6,2,6]
        )
        for input in dataset:
            with self.subTest(f"Check error for {input} corner bet"):
                with self.assertRaises(InvalidBet):
                    Bet.create_corner(100., input)

class RoletaTest(TestCase):

    def test_run_test(self):
        self.assertTrue(True)

    def test_black(self):
        bet = Bet.create_black(value=100.)
        self.assertIsInstance(bet, Bet)
        self.assertEqual(bet.value, 100.)
        black = {
            2, 4, 6, 8, 10, 11, 13, 15,
            17, 20, 22, 24, 26, 28, 29, 31, 33, 35
        }
        self.assertSetEqual(bet.numbers, black)

    def test_red(self):
        bet = Bet.create_red(value=100.)
        self.assertIsInstance(bet, Bet)
        self.assertEqual(bet.value, 100.)
        red = {
            1, 3, 5, 7, 9, 12,
            14, 16, 18, 19,
            21, 23, 25, 27,
            30, 32, 34, 36
        }
        self.assertSetEqual(bet.numbers, red)

    def test_odd(self):
        bet = Bet.create_odd(value=100.)
        self.assertIsInstance(bet, Bet)
        self.assertEqual(bet.value, 100.)
        self.assertEqual(len(bet.numbers), 18)
        self.assertEqual(
            len(list(filter(lambda it: it % 2 == 0, bet.numbers))), 0)

    def test_even(self):
        bet = Bet.create_even(value=100.)
        self.assertIsInstance(bet, Bet)
        self.assertEqual(bet.value, 100.)
        self.assertEqual(len(bet.numbers), 18)
        self.assertEqual(
            len(list(filter(lambda it: it % 2 == 1, bet.numbers))), 0)

    def test_line(self):
        result_mod = choice([0,1,2])
        start_with = 3 if result_mod == 0 else result_mod
        bet = Bet.create_line(value=100., result_mod=result_mod)
        self.assertIsInstance(bet, Bet)
        self.assertEqual(bet.value, 100.)
        self.assertEqual(len(bet.numbers), 12)
        self.assertEqual(
            sorted(list(filter(lambda it: it % 3 == result_mod, bet.numbers))), [i for i in range(start_with,37,3)])

    def test_low(self):
        bet = Bet.create_low(value=100.)
        self.assertIsInstance(bet, Bet)
        self.assertEqual(bet.numbers, set(range(1, 19)))

    def test_high(self):
        bet = Bet.create_high(value=100.)
        self.assertIsInstance(bet, Bet)
        self.assertEqual(bet.numbers, set(range(19, 37)))

    def test_first_dozen(self):
        bet = Bet.create_first_dozen(value=100.)
        self.assertIsInstance(bet, Bet)
        self.assertEqual(bet.numbers, set(range(1, 13)))
    
    def test_second_dozen(self):
        bet = Bet.create_second_dozen(value=100.)
        self.assertIsInstance(bet, Bet)
        self.assertEqual(bet.numbers, set(range(13, 25)))

    def test_third_dozen(self):
        bet = Bet.create_third_dozen(value=100.)
        self.assertIsInstance(bet, Bet)
        self.assertEqual(bet.numbers, set(range(25, 37)))

    def test_street(self):
        for input in range(1,13):
            with self.subTest(f"Check error for {list(map(lambda it: input*3+it,[-2,-1,0]))} street bet"):
                bet = Bet.create_street(100., list(map(lambda it: input*3+it, [-2,-1,0])))
                self.assertIsInstance(bet, Bet)
                self.assertEqual(bet.numbers, list(map(lambda it: input*3+it, [-2,-1,0])))

    def test_two_street(self):
        for input in range(1,7):
            with self.subTest(f"Check error for {list(map(lambda it: input*3+it, [-2,-1,0,1,2,3]))} two street bet"):
                bet = Bet.create_two_street(100., list(map(lambda it: input*3+it, [-2,-1,0,1,2,3])))
                self.assertIsInstance(bet, Bet)
                self.assertEqual(bet.numbers, list(map(lambda it: input*3+it, [-2,-1,0,1,2,3])))

    def test_corner_bet(self):
        for input in gen_all_four_corners():
            with self.subTest(f"Check error for {input} corner bet"):
                bet = Bet.create_corner(100., input)
                self.assertIsInstance(bet, Bet)
                self.assertEqual(bet.numbers, sorted(input))
