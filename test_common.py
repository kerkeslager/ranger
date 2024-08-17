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
