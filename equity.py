import fractions
import functools
import itertools
import operator
import random

from common import *
import showdown

def sample(iterator, n):
    '''
    Takes every nth item from iterator. n should be a prime number to avoid aligning
    with cycles in the data.
    '''
    nth = [0] * n
    nth[0] = 1
    return itertools.compress(iterator, itertools.cycle(nth))

def equity(board, ranges):
    assert len(board) in {0,3,4,5}

    if len(board) == 0:
        # It appears that using list() instead of sorted() causes
        # the order to be non-deterministic, which causes the test on this
        # to fail.
        cards = sorted(CARDS)
        boards = (
            frozenset(random.sample(cards, 5))
            for i in range(3000)
        )
    else:
        boards = (
            frozenset(itertools.chain(board, remaining))
            for remaining in itertools.combinations(CARDS - board, 5 - len(board))
        )

    equities = [0 for r in ranges]

    weighted_ranges = [
        [(combo, weight) for combo, weight in r.items() if weight > 0]
        for r in ranges
    ]

    for b in boards:
        range_keys = [
            [
                (showdown.showdown_key(board=b, combo=combo), combo, weight)
                for combo, weight in r
                if len(b | combo) == 7
            ]
            for r in weighted_ranges
        ]

        for sd in itertools.product(*range_keys):
            keys, combos, weights = zip(*sd)

            if len(functools.reduce(operator.or_, combos)) < 2 * len(combos):
                continue

            weight = functools.reduce(operator.mul, weights)

            winning_key = max(keys)
            winner_count = sum(k == winning_key for k in keys)

            for index, key in enumerate(keys):
                if key == winning_key:
                    equities[index] += fractions.Fraction(1, winner_count) * weight

    total_equity = sum(equities)
    return [e / total_equity for e in equities]

