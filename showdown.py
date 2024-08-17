from common import *

HIGH_CARD = 0
PAIR = 1
TWO_PAIR = 2
THREE_KIND = 3
STRAIGHT = 4
FLUSH = 5
FULL_HOUSE = 6
FOUR_KIND = 7
STRAIGHT_FLUSH = 8

_GROUP_COUNTS = {
    (4,1): FOUR_KIND,
    (3,2): FULL_HOUSE,
    (3,1,1): THREE_KIND,
    (2,2,1): TWO_PAIR,
    (2,1,1,1): PAIR,
}

_STRAIGHTS = { tuple(range(i, i - 5, -1)) : i for i in range(14, 5, -1) }
_STRAIGHTS[(14,5,4,3,2)] = 5 # Wheel straight

def showdown_key(*, board=None, combo=None, hand=None):
    if board and combo:
        assert len(board) == 5
        assert len(combo) == 2
        cards = frozenset(itertools.chain(board, combo))
        assert len(cards) == 7
        return max(
            showdown_key(hand=hand)
            for hand in itertools.combinations(cards, 5)
        )

    assert board is None
    assert combo is None
    assert hand is not None
    assert len(set(hand)) == 5

    rank_values = tuple(sorted(
        map(lambda c: rank_value(rank(c)), hand),
        reverse=True,
    ))

    is_flush = len({ suit(c) for c in hand }) == 1

    if rank_values in _STRAIGHTS:
        if is_flush:
            return (STRAIGHT_FLUSH, _STRAIGHTS[rank_values])

        return (STRAIGHT, _STRAIGHTS[rank_values])

    if is_flush:
        return (FLUSH,) + rank_values

    counts = [1]
    groups = [rank_values[0]]

    for rv in rank_values[1:]:
        if rv == groups[-1]:
            counts[-1] += 1
        else:
            groups.append(rv)
            counts.append(1)

    counts, groups = zip(*sorted(zip(counts,groups), reverse=True))

    if counts in _GROUP_COUNTS:
        return (_GROUP_COUNTS[counts],) + groups

    return (HIGH_CARD,) + rank_values
