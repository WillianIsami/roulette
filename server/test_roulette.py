from unittest import TestCase
from roulette import Bet, BetFactory, InvalidBet, number_to_xy
from random import sample, choice


def gen_bet_numbers(size):
    return sample(range(0, 37), k=size)


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

    def test_convert_user_input_multiple_numbers(self):
        dataset = dict(
            (','.join(map(str, numbers)), set(numbers))
            for numbers in
            [gen_bet_numbers(choice(range(2, 5))) for _ in range(10)]
        )
        for input, expected in dataset.items():
            with self.subTest(f"Convert {input} to {expected}"):
                try: 
                    bet = self.factory.create_from_str(0, input)
                    self.assertIsInstance(bet, Bet)
                    self.assertEqual(bet.numbers, expected)
                except InvalidBet:
                    with self.assertRaises(InvalidBet):
                        self.factory.create_from_str(0, input)

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
