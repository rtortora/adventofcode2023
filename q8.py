from __future__ import annotations
from dataclasses import dataclass
from collections import defaultdict
from collections.abc import Iterator

@dataclass
class Chain:
    nodes: tuple[str, str]

type ChainMap = dict[str, Chain]

def parse_chain(line: str) -> tuple[str, Chain]:
    key, chain_text = line.split(" = ")
    node1, node2 = chain_text[1:-1].split(", ")
    return (key, Chain((node1, node2)))

def parse_chain_map(lines: list[str]) -> ChainMap:
    return dict([parse_chain(line) for line in lines])

def parse_input(text: str) -> tuple[str, ChainMap]:
    path, _, *chain_map_lines = text.splitlines()
    return (path, parse_chain_map(chain_map_lines))

test_input_1="""RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""

test_input_2="""LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""

PATHING = {"L": 0, "R": 1}

def follow(path: str, chain_map: ChainMap, debug: bool)->int:
    steps = 0
    cursor = "AAA"
    while cursor != "ZZZ":
        for pathing in path:
            prev = cursor
            cursor = chain_map[cursor].nodes[PATHING[pathing]]
            if debug:
                print(f'{prev} {pathing} -> {cursor}')
            steps += 1
            if cursor == "ZZZ":
                return steps
    return steps

def main():
    if follow(*parse_input(test_input_1), False) != 2:
        raise RuntimeError("test 1 fail")
    if follow(*parse_input(test_input_2), False) != 6:
        raise RuntimeError("test 2 fail")
    with open("./inputs/q8.txt", encoding="utf-8") as file:
        print(follow(*parse_input(file.read()), True))
main()
