"""q8"""

from __future__ import annotations
from dataclasses import dataclass
from collections import defaultdict
from collections.abc import Iterator
import math

@dataclass
class Branch:
    """tree branch"""
    nodes: tuple[str, str]

type Tree = dict[str, Branch]

def parse_branch(line: str) -> tuple[str, Branch]:
    """parse branch"""
    key, branch_text = line.split(" = ")
    node1, node2 = branch_text[1:-1].split(", ")
    return (key, Branch((node1, node2)))

def parse_tree(lines: list[str]) -> Tree:
    """parse tree"""
    return dict([parse_branch(line) for line in lines])

def parse_input(text: str) -> tuple[str, Tree]:
    """parse input"""
    path, _, *tree_lines = text.splitlines()
    return (path, parse_tree(tree_lines))

TEST_INPUT="""LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""

PATHING = {"L": 0, "R": 1}

class NextZIterator:
    """Infinite iterator that finds the next node that ends with a Z, counting steps along the way"""
    tree: Tree
    node: str
    path: str
    path_iter: Iterator[str]
    steps: int
    def __init__(self, tree: Tree, node: str, path: str):
        self.tree = tree
        self.node = node
        self.path = path
        self.path_iter = iter(path)
        self.steps = 0
    def __iter__(self):
        return self
    def __next__(self)->tuple[str, int]:
        while True:
            next_step = next(self.path_iter, None)
            if next_step is None:
                self.path_iter = iter(self.path)
                next_step = next(self.path_iter)
            pathing = PATHING[next_step]
            self.node = self.tree[self.node].nodes[pathing]
            self.steps += 1
            if self.node.endswith("Z"):
                return (self.node, self.steps)

def get_cadence(tree: Tree, node: str, path: str)->int:
    """Assumes that if the first 3 Z nodes are equidistant, they all will be, and gets that cadence"""
    next_z_iter = NextZIterator(tree, node, path)
    expected_cadence = next(next_z_iter)[1]
    last_value = expected_cadence
    for _ in range(0, 10):
        next_z_steps = next(next_z_iter)[1]
        if next_z_steps - last_value != expected_cadence:
            raise RuntimeError("Nooo")
        last_value = next_z_steps
    return expected_cadence

def get_factor(value: int)->list[int]:
    """factor a number"""
    factors: list[int] = []
    while True:
        if value % 2 == 0:
            factors.append(2)
            value = math.trunc(value / 2)
            continue
        for n in range(3, int(value / 2) + 1, 2):
            if value % n == 0:
                factors.append(n)
                value = int(value / n)
                continue
        if value != 1:
            factors.append(value)
        return factors

def get_lcm(factors_list: list[list[int]])->list[int]:
    """get LCM for a set of factors"""
    factors_dicts: list[defaultdict[int, int]] = []
    for factors in factors_list:
        counts: defaultdict[int, int] = defaultdict(lambda: 0)
        for factor in factors:
            counts[factor] += 1
        factors_dicts.append(counts)

    common_factors: list[int] = []
    for factor in factors_dicts[0]:
        found_missing = False
        for other_factor_dict in factors_dicts[1:]:
            if not factor in other_factor_dict.keys():
                found_missing = True
                break
        if not found_missing:
            common_factors.append(factor)
            for factors_dict in factors_dicts:
                factors_dict[factor] -= 1

    for factors_dict in factors_dicts:
        for factor in factors_dict.keys():
            for _ in range(0, factors_dict[factor]):
                common_factors.append(factor)

    return common_factors

def best_steps_for_all_zs(tree: Tree, path: str)->int:
    """get the answer"""
    cadences = [get_cadence(tree, node, path) for node in tree.keys() if node.endswith("A")]
    factors = [get_factor(cadence) for cadence in cadences]
    mul = 1
    for factor in get_lcm(factors):
        mul *= factor
    return mul

def main():
    """main"""
    with open("./inputs/q8.txt", encoding="utf-8") as file:
        path, tree = parse_input(file.read())
        print(best_steps_for_all_zs(tree, path))

main()
