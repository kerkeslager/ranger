import unittest

from showdown import *

class ShowdownKeyTests(unittest.TestCase):
    def test_board_and_combo(self):
        self.assertEqual(
            showdown_key(
                board={'As','Ks','8c','8d','3s'},
                combo={'Kc','Kd'},
            ),
            showdown_key(
                hand={'Kc','Kd','Ks','8c','8d'},
            )
        )

        self.assertEqual(
            showdown_key(
                board={'As','Ks','8c','8d','3s'},
                combo={'Qs','9s'},
            ),
            showdown_key(
                hand={'As','Ks','Qs','9s','3s'},
            )
        )

    def test_straight_flush(self):
        hand = ['8c', 'Tc', '9c', 'Jc', 'Qc']

        self.assertEqual(
            showdown_key(hand=hand)[0],
            STRAIGHT_FLUSH,
        )

    def test_straight_flush_beats_lesser(self):
        hi = frozenset(['8c', 'Tc', '9c', 'Jc', 'Qc'])
        lo = frozenset(['8c', 'Tc', '9c', 'Jc', '7c'])

        self.assertGreater(
            showdown_key(hand=hi),
            showdown_key(hand=lo),
        )

    def test_straight_flush_beats_four_kind(self):
        hi = frozenset(['8c', 'Tc', '9c', 'Jc', 'Qc'])
        lo = frozenset(['2h', 'Kh', 'Kc', 'Kd', 'Ks'])

        self.assertGreater(
            showdown_key(hand=hi),
            showdown_key(hand=lo),
        )

    def test_four_kind(self):
        hand = ['Kc', 'Kh', 'Ks', 'Kd', 'Qc']

        self.assertEqual(
            showdown_key(hand=hand)[0],
            FOUR_KIND,
        )

    def test_four_kind_beats_lesser(self):
        hi = frozenset(['2h', 'Kh', 'Kc', 'Kd', 'Ks'])
        lo = frozenset(['Ah', 'Qh', 'Qc', 'Qd', 'Qs'])

        self.assertGreater(
            showdown_key(hand=hi),
            showdown_key(hand=lo),
        )

    def test_four_kind_beats_full_house(self):
        hi = frozenset(['Th', 'Td', 'Jh', 'Tc', 'Ts'])
        lo = frozenset(['Th', 'Td', 'Jh', 'Jc', 'Js'])

        self.assertGreater(
            showdown_key(hand=hi),
            showdown_key(hand=lo),
        )

    def test_full_house(self):
        hand = ['Qs', 'Kh', 'Ks', 'Kd', 'Qc']

        self.assertEqual(
            showdown_key(hand=hand)[0],
            FULL_HOUSE,
        )

    def test_full_house_beats_lesser(self):
        hi = frozenset(['2h', '2c', 'Kc', 'Kd', 'Ks'])
        lo = frozenset(['Ah', 'Ac', 'Qc', 'Qd', 'Qs'])

        self.assertGreater(
            showdown_key(hand=hi),
            showdown_key(hand=lo),
        )

    def test_full_house_beats_flush(self):
        hi = frozenset(['Th', 'Td', 'Jh', 'Tc', 'Js'])
        lo = frozenset(['Qh', 'Th', '7h', '6h', '2h'])

        self.assertGreater(
            showdown_key(hand=hi),
            showdown_key(hand=lo),
        )

    def test_flush(self):
        hand = ['Qh', 'Kh', 'Jh', '7h', 'Th']

        self.assertEqual(
            showdown_key(hand=hand)[0],
            FLUSH,
        )

    def test_flush_beats_lesser(self):
        hi = frozenset(['Ah', '2h', 'Kh', 'Th', '7h'])
        lo = frozenset(['Ah', '2h', 'Qh', 'Th', '7h'])

        self.assertGreater(
            showdown_key(hand=hi),
            showdown_key(hand=lo),
        )

    def test_flush_beats_straight(self):
        hi = frozenset(['Qh', 'Th', '7h', '6h', '2h'])
        lo = frozenset(['Kh', 'Qd', 'Jh', 'Tc', '9s'])

        self.assertGreater(
            showdown_key(hand=hi),
            showdown_key(hand=lo),
        )

    def test_straight(self):
        hand = ['Qh', 'Kd', 'Jh', '9c', 'Ts']

        self.assertEqual(
            showdown_key(hand=hand)[0],
            STRAIGHT,
        )

        hand = ['Ah', '3d', '2h', '5c', '4s']

        self.assertEqual(
            showdown_key(hand=hand)[0],
            STRAIGHT,
        )

    def test_straight_beats_lesser(self):
        hi = frozenset(['Ah', 'Kd', 'Qh', 'Tc', 'Js'])
        lo = frozenset(['Jh', 'Kd', 'Qh', 'Tc', '9s'])

        self.assertGreater(
            showdown_key(hand=hi),
            showdown_key(hand=lo),
        )

        hi = frozenset(['6h', '2d', '3h', '4c', '5s'])
        lo = frozenset(['Ah', '2d', '3h', '4c', '5s'])

        self.assertGreater(
            showdown_key(hand=hi),
            showdown_key(hand=lo),
        )

    def test_straight_beats_three_kind(self):
        hi = frozenset(['Kh', 'Qd', 'Jh', 'Tc', '9s'])
        lo = frozenset(['Ah', 'Kd', 'Kh', 'Kc', '7s'])

        self.assertGreater(
            showdown_key(hand=hi),
            showdown_key(hand=lo),
        )

    def test_three_kind(self):
        hand = ['Ah', 'Kd', 'Kh', 'Kc', '7s']

        self.assertEqual(
            showdown_key(hand=hand)[0],
            THREE_KIND,
        )

    def test_three_kind_beats_lesser(self):
        hi = frozenset(['Ah', 'Kd', 'Kh', 'Kc', '7s'])
        lo = frozenset(['Ah', 'Qd', 'Qh', 'Qc', '7s'])

        self.assertGreater(
            showdown_key(hand=hi),
            showdown_key(hand=lo),
        )

        hi = frozenset(['Ah', 'Qd', 'Qh', 'Qc', '7s'])
        lo = frozenset(['Kh', 'Qd', 'Qh', 'Qc', '7s'])

        self.assertGreater(
            showdown_key(hand=hi),
            showdown_key(hand=lo),
        )

    def test_three_kind_beats_two_pair(self):
        hi = frozenset(['Kh', '7d', '7h', '7c', '2s'])
        lo = frozenset(['Ah', 'Kd', 'Kh', '7c', '7s'])

        self.assertGreater(
            showdown_key(hand=hi),
            showdown_key(hand=lo),
        )

    def test_two_pair(self):
        hand = ['Ah', 'Kd', 'Kh', '7c', '7s']

        self.assertEqual(
            showdown_key(hand=hand)[0],
            TWO_PAIR,
        )

    def test_two_pair_beats_lesser(self):
        hi = frozenset(['Ah', 'Kd', 'Kh', '7c', '7s'])
        lo = frozenset(['Ah', 'Qd', 'Qh', '7c', '7s'])

        self.assertGreater(
            showdown_key(hand=hi),
            showdown_key(hand=lo),
        )

        hi = frozenset(['Ah', 'Qd', 'Qh', '7c', '7s'])
        lo = frozenset(['Kh', 'Qd', 'Qh', '7c', '7s'])

        self.assertGreater(
            showdown_key(hand=hi),
            showdown_key(hand=lo),
        )

    def test_two_pair_beats_pair(self):
        hi = frozenset(['Kh', 'Kd', '7h', '7c', '2s'])
        lo = frozenset(['Ah', 'Kd', '7h', '7c', '2s'])

        self.assertGreater(
            showdown_key(hand=hi),
            showdown_key(hand=lo),
        )

    def test_pair(self):
        hand = ['Ah', 'Kd', 'Kh', '7c', '2s']

        self.assertEqual(
            showdown_key(hand=hand)[0],
            PAIR,
        )

    def test_pair_beats_lesser(self):
        hi = frozenset(['Ah', 'Kd', 'Kh', '7c', '2s'])
        lo = frozenset(['Ah', 'Qd', 'Qh', '7c', '2s'])

        self.assertGreater(
            showdown_key(hand=hi),
            showdown_key(hand=lo),
        )

        hi = frozenset(['Ah', 'Qd', 'Qh', '7c', '2s'])
        lo = frozenset(['Kh', 'Qd', 'Qh', '7c', '2s'])

        self.assertGreater(
            showdown_key(hand=hi),
            showdown_key(hand=lo),
        )

    def test_pair_beats_high_card(self):
        hi = frozenset(['Ah', 'Kd', '7h', '7c', '2s'])
        lo = frozenset(['Ah', 'Kd', 'Th', '7c', '2s'])

        self.assertGreater(
            showdown_key(hand=hi),
            showdown_key(hand=lo),
        )

    def test_high_card(self):
        hand = frozenset(['Ah', 'Kd', 'Th', '7c', '2s'])

        self.assertEqual(
            showdown_key(hand=hand)[0],
            HIGH_CARD,
        )

    def test_high_card_beats_lesser(self):
        hi = frozenset(['Ah', 'Kd', 'Th', '7c', '2s'])
        lo = frozenset(['Ah', 'Qd', 'Th', '7c', '2s'])

        self.assertGreater(
            showdown_key(hand=hi),
            showdown_key(hand=lo),
        )



