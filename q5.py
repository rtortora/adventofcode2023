from dataclasses import dataclass
import re

@dataclass
class Map:
  destination_range_start: int
  source_range_start: int
  range_length: int

  def contains(self, value: int)->bool:
    return value >= self.source_range_start and value < (self.source_range_start + self.range_length)

  def lookup(self, value: int)->int:
    return value - self.source_range_start + self.destination_range_start

@dataclass
class MapList:
  maps: list[Map]
  def lookup(self, value: int)->int:
    for map in self.maps:
      for conversion in map:
        if conversion.contains(value):
          value = conversion.lookup(value)
          break
    return value

@dataclass
class Almanac:
  seeds: list[int]
  map_list: MapList

@dataclass
class SeedRange:
  start: int
  length: int

@dataclass
class AlmanacWithSeedRanges:
  seeds: list[SeedRange]
  map_list: MapList

def parse_almanac(input: str)->Almanac:
  seeds_line_text, *lines = input.splitlines()
  map_list = MapList([])
  seeds_texts = seeds_line_text.replace("seeds: ", "").split(" ")
  seeds = [int(x) for x in seeds_texts]
  for line in lines:
    if len(line) == 0:
      continue
    elif ":" in line:
      map_list.maps.append([]);
    else:
      numbers = [int(x) for x in line.split(" ")]
      map_list.maps[len(map_list.maps) - 1].append(Map(numbers[0], numbers[1], numbers[2]))
  return Almanac(seeds, map_list)

def parse_almanac_with_seed_ranges(input: str)->AlmanacWithSeedRanges:
  almanac = parse_almanac(input)
  seed_ranges = [SeedRange(almanac.seeds[i], almanac.seeds[i + 1]) for i in range(0, len(almanac.seeds), 2)]
  return AlmanacWithSeedRanges(seed_ranges, almanac.map_list)

def q1(input: str):
  almanac = parse_almanac(input)
  min_seed = None
  min_seed_location = None
  for seed in almanac.seeds:
    location = almanac.map_list.lookup(seed)
    if min_seed == None or location < min_seed_location:
      min_seed = seed
      min_seed_location = location
  print(f'seed {min_seed}, location {min_seed_location}')

def q2(input: str):
  almanac = parse_almanac_with_seed_ranges(input)
  min_seed = None
  min_seed_location = None
  for seed_range in almanac.seeds:
    for seed in range(seed_range.start, seed_range.start + seed_range.length):
      location = almanac.map_list.lookup(seed)
      if min_seed == None or location < min_seed_location:
        min_seed = seed
        min_seed_location = location
  print(f'seed {min_seed}, location {min_seed_location}')

def main():
  #q1(open("./inputs/q5-test.txt").read())
  #q1(open("./inputs/q5.txt").read()) # 462648396
  #q2(open("./inputs/q5-test.txt").read()) # 46
  q2(open("./inputs/q5.txt").read())


main()
