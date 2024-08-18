import itertools

RANKS = 'AKQJT98765432'
SUITS = 'cdhs'

CARDS = frozenset(
    rank + suit
    for rank in RANKS
    for suit in SUITS
)

_RANK_VALUES = {
    rank : 14 - RANKS.index(rank)
    for rank in RANKS
}
def rank_value(rank):
    return _RANK_VALUES[rank]

STARTING_HANDS = frozenset(
    RANKS[i] + RANKS[j] + 's' if i < j else
    RANKS[j] + RANKS[i] + 'o' if i > j else
    RANKS[i] + RANKS[j]
    for i in range(len(RANKS))
    for j in range(len(RANKS))
)

COMBOS = frozenset(frozenset(c) for c in itertools.combinations(CARDS, 2))

def rank(card):
    r, s = card
    return r

def suit(card):
    r, s = card
    return s

def are_suited(cards):
    return len(set(s for r,s in cards)) == 1

def starting_hand_to_combos(sh):
    if len(sh) == 2:
        r0,r1 = sh
        return frozenset(
            frozenset([r0+s0, r1+s1])
            for s0,s1 in itertools.combinations(SUITS, 2)
        )

    high, low, suitedness = sh

    if suitedness == 's':
        return frozenset(
            frozenset([high + suit, low + suit])
            for suit in SUITS
        )

    return frozenset(
        frozenset([high + hs, low + ls])
        for hs,ls in itertools.permutations(SUITS, 2)
    )

def combo_to_starting_hand(combo):
    high, low = combo

    hr = rank(high)
    lr = rank(low)

    if hr == lr:
        return hr + lr

    if rank_value(hr) < rank_value(lr):
        hr, lr = lr, hr

    if suit(high) == suit(low):
        return hr + lr + 's'

    return hr + lr + 'o'

def fraction_to_ratio(x):
    y = 1 - x
    x = x.numerator
    y = y.numerator

    if x > y:
        return '{}:1'.format(
            '{:.1f}'.format(x / y).rstrip('0').rstrip('.')
        )

    if x < y:
        return '1:{}'.format(
            '{:.1f}'.format(y / x).rstrip('0').rstrip('.')
        )

    return '1:1'

def fraction_to_percent(x):
    n, d = x.as_integer_ratio()
    return '{:.0%}'.format(n / d)

def print_range(r):
    result = '{ '
    for combo in r:
        result += ''.join(card for card in combo) + ': ' + str(r[combo]) + ', '
    print(result)
