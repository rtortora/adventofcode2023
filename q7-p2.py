from __future__ import annotations
from dataclasses import dataclass
from collections import defaultdict
from collections.abc import Iterator

CARD_POWER = "AKQT" + "".join([str(x) for x in range(9, 1, -1)]) + "J"

type Card = str
type Hand = list[Card]
type HandAndBid = tuple[Hand, int]


def get_hand_type_power(hand: Hand) -> int:
    """get hand type represents as an abstract integer, higher the stronger"""
    counts: defaultdict[Card, int] = defaultdict(lambda: 0)
    for card in hand:
        counts[card] += 1
    wilds = counts["J"]
    del counts["J"]

    if wilds >= 4:
        return 50
    elif len([card for card in counts.keys() if wilds + counts[card] == 5]) > 0:
        return 50
    elif len([card for card in counts.keys() if wilds + counts[card] == 4]) > 0:
        return 40
    elif len([card for card in counts.keys() if wilds + counts[card] == 3]) > 0:
        three_kind_card = [card for card in counts.keys() if wilds + counts[card] == 3][0]
        wilds_used = 3 - counts[three_kind_card]
        wilds_left = wilds - wilds_used
        if len([card for card in counts.keys() if card != three_kind_card and wilds_left + counts[card] == 2]) > 0:
            return 32 # full house
        else:
            return 30 # three of a kind
    elif len([card for card in counts.keys() if wilds + counts[card] == 2]) > 0:
        pair_card = [card for card in counts.keys() if wilds + counts[card] == 2][0]
        wilds_used = 2 - counts[pair_card]
        wilds_left = wilds - wilds_used
        if len([card for card in counts.keys() if card != pair_card and wilds_left + counts[card] == 2]) > 0:
            return 22 # two pair
        else:
            return 20 # one pair
    else:
        return 10 # high card

def get_hand_power(hand: Hand) -> int:
    """get hand total power as an abstract integer, higher the stronger"""
    score_parts: list[str] = [
        str(get_hand_type_power(hand)).zfill(2),
        *[str(len(CARD_POWER) - CARD_POWER.index(card)).zfill(2) for card in hand],
    ]
    score = int("".join(score_parts))
    return score


def accum_game(hands_and_bids: Iterator[HandAndBid], verbose: bool) -> int:
    """accum"""
    sorted_hands_and_bids = sorted(
        hands_and_bids,
        reverse=True,
        key=lambda hand_and_bid: get_hand_power(hand_and_bid[0]),
    )
    sum = 0
    for inverse_0_rank, (hand, bid) in enumerate(sorted_hands_and_bids):
        rank = len(sorted_hands_and_bids) - inverse_0_rank
        if verbose:
            print(
                f'{"".join(hand)} {get_hand_type_power(hand)} {get_hand_power(hand)} -- {rank} * {bid} -- {(rank) * bid}'
            )
        sum += (rank) * bid
    return sum


def parse_text(text: str) -> Iterator[HandAndBid]:
    """parse text"""
    for line in text.splitlines():
        hand, bid_text = line.split(" ")
        yield ([*hand], int(bid_text))


sample_input="""32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""

def main():
    """main"""
    test_output = accum_game(parse_text(sample_input), False)
    if test_output != 5905:
        accum_game(parse_text(sample_input), True)
        raise RuntimeError(f"Failed q1 test input: {test_output}")

    with open("./inputs/q7.txt", encoding="utf-8") as file:
        print(accum_game(parse_text(file.read()), True))


# 250370104 too low
# 251296863 too low
# 251735672

main()
