import fractions
import unittest

from common import *

class RankValueTests(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(rank_value('A'), 14)
        self.assertEqual(rank_value('2'), 2)

class AreSuitedTests(unittest.TestCase):
    def test_basic(self):
        self.assertTrue(are_suited(['Ah','Kh','3h']))
        self.assertFalse(are_suited(['Ah','Ks','3d']))

class StartingHandToCombosTests(unittest.TestCase):
    def test_pairs(self):
        self.assertEqual(
            starting_hand_to_combos('KK'),
            frozenset([
                frozenset(['Kc','Kd']),
                frozenset(['Kc','Kh']),
                frozenset(['Kc','Ks']),
                frozenset(['Kd','Kh']),
                frozenset(['Kd','Ks']),
                frozenset(['Kh','Ks']),
            ]),
        )

    def test_suited(self):
        self.assertEqual(
            starting_hand_to_combos('A5s'),
            frozenset([
                frozenset(['Ac','5c']),
                frozenset(['Ad','5d']),
                frozenset(['Ah','5h']),
                frozenset(['As','5s']),
            ]),
        )

    def test_offsuit(self):
        self.assertEqual(
            starting_hand_to_combos('AKo'),
            frozenset([
                frozenset(['Ac','Kd']),
                frozenset(['Ac','Kh']),
                frozenset(['Ac','Ks']),
                frozenset(['Ad','Kc']),
                frozenset(['Ad','Kh']),
                frozenset(['Ad','Ks']),
                frozenset(['Ah','Kc']),
                frozenset(['Ah','Kd']),
                frozenset(['Ah','Ks']),
                frozenset(['As','Kc']),
                frozenset(['As','Kd']),
                frozenset(['As','Kh']),
            ]),
        )

class ComboToStartingHand(unittest.TestCase):
    def test_pair(self):
        self.assertEqual(
            combo_to_starting_hand(['Ah', 'Ad']),
            'AA',
        )

    def test_suited(self):
        self.assertEqual(
            combo_to_starting_hand(['Ah', '5h']),
            'A5s',
        )

    def test_offsuit(self):
        self.assertEqual(
            combo_to_starting_hand(['Ah', 'Kd']),
            'AKo',
        )

class FractionToRatioTests(unittest.TestCase):
    def test_self_greater_than_other(self):
        self.assertEqual(
            fraction_to_ratio(fractions.Fraction(2, 3)),
            '2:1',
        )

    def test_self_less_than_other(self):
        self.assertEqual(
            fraction_to_ratio(fractions.Fraction(1,3)),
            '1:2',
        )

    def test_decimals(self):
        self.assertEqual(
            fraction_to_ratio(fractions.Fraction(3, 5)),
            '1.5:1',
        )
        self.assertEqual(
            fraction_to_ratio(fractions.Fraction(2, 5)),
            '1:1.5',
        )

    def test_rounding(self):
        self.assertEqual(
            fraction_to_ratio(fractions.Fraction(4, 7)),
            '1.3:1',
        )
        self.assertEqual(
            fraction_to_ratio(fractions.Fraction(3, 7)),
            '1:1.3',
        )
        self.assertEqual(
            fraction_to_ratio(fractions.Fraction(5, 8)),
            '1.7:1',
        )
        self.assertEqual(
            fraction_to_ratio(fractions.Fraction(3, 8)),
            '1:1.7',
        )
