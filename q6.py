"""q6"""

from __future__ import annotations
from dataclasses import dataclass
import re
import math

TEST_INPUT = """Time:      7  15   30
Distance:  9  40  200"""

@dataclass
class Race:
    """race"""
    time: int
    distance: int

def quadratic_formula(a: int, b: int, c: int)->tuple[float, float]:
    """for formula ax^2 + bx + c = 0, solve for x"""
    x1 = (-b + math.sqrt((b ** 2) - (4 * a * c))) / (2 * a)
    x2 = (-b - math.sqrt((b ** 2) - (4 * a * c))) / (2 * a)
    return (x1, x2)

def get_winning_waits(race: Race)->list[int]:
    winning_routes: list[int] = []
    for wait in range(1, race.time):
        if wait * (race.time - wait) > race.distance:
            #print(f'  {wait} * ({race.time - wait}) > {race.distance} => {wait * (race.time - wait)} > {race.distance}')
            winning_routes.append(wait)
    return winning_routes

def calculate_winning_wait_range(race: Race)->range:
    """calculates winning wait range with quadratic formula in constant time"""
    (max_wait_time, min_wait_time) = quadratic_formula(1, -race.time, race.distance + 1)
    winning_wait_range = range(math.ceil(min_wait_time), math.floor(max_wait_time) + 1)
    #print(f'calc {race} {(min_wait_time, max_wait_time)} {winning_wait_range} {len(winning_wait_range)}')
    return winning_wait_range

def answer(races: list[Race])->int:
    mul = 1
    for race in races:
        get_winning_waits(race)
        winning_wait_range = calculate_winning_wait_range(race)
        mul *= len(winning_wait_range)
    return mul

def parse_races_q1(text: str)->list[Race]:
    times_text, distances_text = text.splitlines()
    times = [int(x) for x in re.split(r' +', times_text.replace("Time: ", "").strip())]
    distances = [int(x) for x in re.split(r' +', distances_text.replace("Distance: ", "").strip())]
    return [Race(time, distances[i]) for i, time in enumerate(times)]

def parse_races_q2(text: str)->list[Race]:
    times_text, distances_text = text.splitlines()
    time = int(times_text.replace("Time: ", "").replace(" ", ""))
    distance = int(distances_text.replace("Distance: ", "").replace(" ", ""))
    return [Race(time, distance)]

def main():
    print(answer(parse_races_q1(TEST_INPUT)))
    with open("./inputs/q6.txt", encoding="utf-8") as test_file:
        print(answer(parse_races_q1(test_file.read())))
    print(answer(parse_races_q2(TEST_INPUT)))
    with open("./inputs/q6.txt", encoding="utf-8") as test_file:
        print(answer(parse_races_q2(test_file.read())))

main()
