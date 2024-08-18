import unittest

from equity import *

class EquityTests(unittest.TestCase):
    def test_preflop_equity(self):
        random.seed(42)
        hero_range = {
            frozenset(['Jc','Jd']): True,
            frozenset(['Jc','Jh']): True,
            frozenset(['Jc','Js']): True,
            frozenset(['Jd','Jh']): True,
            frozenset(['Jd','Js']): True,
            frozenset(['Jh','Js']): True,
        }
        villain_range = {
            frozenset(['Ac','Kc']): True,
            frozenset(['Ad','Kd']): True,
            frozenset(['Ah','Kh']): True,
            frozenset(['As','Ks']): True,
        }

        result = equity(set(), [hero_range, villain_range])
        result = [fraction_to_percent(e) for e in result]

        self.assertEqual(
            result,
            ['54%', '46%'],
        )

    def test_flop_equity(self):
        board = { 'Qh', '8h', '7d' }

        hero_range = {
            frozenset(['Ah','Kh']): True,
            frozenset(['Ah','5h']): True,
        }
        villain_range = {
            frozenset(['Qc','Qd']): True,
            frozenset(['Qc','Qs']): True,
            frozenset(['Qd','Qs']): True,
        }

        result = equity(board, [hero_range, villain_range])
        result = [fraction_to_percent(e) for e in result]

        self.assertEqual(
            result,
            ['26%', '74%'],
        )

    def test_turn_equity(self):
        board = { 'Qh', '8h', '7d', '2h' }

        hero_range = {
            frozenset(['Ah','Kh']): True,
            frozenset(['Ah','5h']): True,
        }
        villain_range = {
            frozenset(['Qc','Qd']): True,
            frozenset(['Qc','Qs']): True,
            frozenset(['Qd','Qs']): True,
        }

        result = equity(board, [hero_range, villain_range])
        result = [fraction_to_percent(e) for e in result]

        self.assertEqual(
            result,
            ['77%', '23%'],
        )

    def test_river_equity(self):
        board = { 'Qh', '8h', '7d', '2h', '8c' }

        hero_range = {
            frozenset(['Ah','Kh']): True,
            frozenset(['Ah','5h']): True,
        }
        villain_range = {
            frozenset(['Qc','Qd']): True,
            frozenset(['Qc','Qs']): True,
            frozenset(['Qd','Qs']): True,
        }

        result = equity(board, [hero_range, villain_range])
        result = [fraction_to_percent(e) for e in result]

        self.assertEqual(
            result,
            ['0%', '100%'],
        )
