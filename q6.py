"""q6"""

from __future__ import annotations
from dataclasses import dataclass
import re
import math

test_input = """Time:      7  15   30
Distance:  9  40  200"""

@dataclass
class Race:
    time: int
    distance: int


# time = total time available
# distance = distance to bear
# wait = how long to wait
# speed = how long you are now moving = wait
# travel_time = how long it takes to ravel = time - wait

# wait * (time - wait) = distance
# ln(wait * (time - wait)) = ln(distance)
# ln(wait) + ln(time - wait) = ln(distance)
#

type Route = int

def get_winning_routes(race: Race)->list[Route]:
    winning_routes: list[Route] = []
    for wait in range(1, race.time):
        if wait * (race.time - wait) > race.distance:
            print(f'  {wait} * ({race.time} - {wait}) > {race.distance} => {wait * (race.time - wait)} > {race.distance}')
            winning_routes.append(wait)
    return winning_routes

def q1(text: str)->int:
    mul = 1
    for race in parse_races(text):
        winning_routes = get_winning_routes(race)
        print(f'{race} {winning_routes}')
        mul *= len(winning_routes)
    return mul

def parse_races(text: str)->list[Race]:
    times_text, distances_text = text.splitlines()
    times = [int(x) for x in re.split(r' +', times_text.replace("Time: ", "").strip())]
    distances = [int(x) for x in re.split(r' +', distances_text.replace("Distance: ", "").strip())]
    return [Race(time, distances[i]) for i, time in enumerate(times)]

def main():
    #print(q1(test_input))
    with open("./inputs/q6.txt", encoding="utf-8") as test_file:
        print(q1(test_file.read()))

main()
