from __future__ import annotations
from dataclasses import dataclass
from collections import defaultdict
from collections.abc import Iterator

CARD_POWER = "AKQJT" + "".join([str(x) for x in range(9, 1, -1)])

type Card = str
type Hand = list[Card]
type HandAndBid = tuple[Hand, int]

def get_hand_type_power(hand: Hand)->int:
    """get hand type represents as an abstract integer, higher the stronger"""
    count_by_value: defaultdict[Card, int] = defaultdict(lambda: 0)
    for card in hand:
        count_by_value[card] += 1
    sorted_values: list[int] = list(count_by_value.values())
    sorted_values.sort(reverse=True)
    if sorted_values[0] >= 4:
        return sorted_values[0] * 10
    elif len(sorted_values) == 2 and sorted_values[0] == 3 and sorted_values[1] == 2:
        return 32
    elif sorted_values[0] == 3:
        return 30
    elif len(sorted_values) >= 2 and sorted_values[0] == 2 and sorted_values[1] == 2:
        return 22
    return sorted_values[0] * 10

def get_hand_power(hand: Hand)->int:
    """get hand total power as an abstract integer, higher the stronger"""
    score_parts: list[str] = [
        str(get_hand_type_power(hand)).zfill(2),
        *[str(len(CARD_POWER) - CARD_POWER.index(card)).zfill(2) for card in hand]
    ]
    score = int("".join(score_parts))
    return score

def accum_game(hands_and_bids: Iterator[HandAndBid], verbose: bool)->int:
    """accum"""
    sorted_hands_and_bids = sorted(hands_and_bids, reverse=True, key=lambda hand_and_bid: get_hand_power(hand_and_bid[0]))
    sum = 0
    for inverse_0_rank, (hand, bid) in enumerate(sorted_hands_and_bids):
        rank = (len(sorted_hands_and_bids) - inverse_0_rank)
        if verbose:
            print(f'{hand} {bid} -- {get_hand_type_power(hand)} {get_hand_power(hand)} -- {rank} * {bid} -- {(rank) * bid}')
        sum += (rank) * bid
    return sum

def parse_text(text: str)->Iterator[HandAndBid]:
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
    test_output =accum_game(parse_text(sample_input), False)
    if test_output != 6440:
        raise RuntimeError(f"Failed q1 test input: {test_output}")

    with open("./inputs/q7.txt", encoding="utf-8") as file:
        print(accum_game(parse_text(file.read()), True))

main()
