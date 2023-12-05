import functools

symbol_characters = "!@#$%^&*()_-+=/"

test_input = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

class Point:
    """Represents an x,y point"""

    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self)->str:
        return f'Point({self.x}, {self.y})'

class PartNumber:
    """Represents a part number in a schematic"""

    instance_id: int
    value: int
    pos: Point

    def __init__(self, instance_id: int, value: int, pos: Point):
        self.instance_id = instance_id
        self.value = value
        self.pos = pos

    def __len__(self)->int:
        return len(f'{self.value}')

    def __repr__(self)->str:
        return f'PartNumber({self.instance_id}, {self.value}, {self.pos})'

    def contains_point(self, point: Point)->bool:
        return point.y == self.pos.y and point.x >= self.pos.x and point.x < (self.pos.x + len(self))

class Symbol:
    """Represents a symbol in a schematic"""

    value: str
    pos: Point

    def __init__(self, value: int, pos: Point):
        self.value = value
        self.pos = pos

    def __repr__(self)->str:
        return f'Symbol({self.value}, {self.pos})'

class SchematicScan:
    size: Point
    part_numbers: list[PartNumber]
    symbols: list[Symbol]

    def __init__(self, size: Point, part_numbers: list[PartNumber], symbols: list[Symbol]):
        self.size = size
        self.part_numbers = part_numbers
        self.symbols = symbols
    
    def __repr__(self) -> str:
        return f'SchematicScan({self.size}, {self.part_numbers}, {self.symbols})'

class Gear:
    symbol: Symbol
    part_numbers: list[PartNumber]

    def __init__(self, symbol: Symbol, part_numbers: list[PartNumber]):
        self.symbol = symbol
        self.part_numbers = part_numbers

    def ratio(self)->int:
        if len(self.part_numbers) != 2:
            raise Exception(f"{self} is not a valid gear")
        return self.part_numbers[0].value * self.part_numbers[1].value

    def __repr__(self)->str:
        return f'Gear({self.symbol}, {self.part_numbers})'

def main():
    #schematic_text = test_input
    schematic_text = open("./inputs/q3.txt").read()
    part1(schematic_text) # 556057
    part2(schematic_text) # 82824352

def part1(schematic_text: str):
    schematic_scan = scan_schematic(schematic_text)
    part_numbers = pull_part_numbers_adjacent_to_symbols(schematic_scan)
    total = sum(part_number.value for part_number in part_numbers)
    print(total)

def part2(schematic_text: str):
    schematic_scan = scan_schematic(schematic_text)
    gears = pull_gears(schematic_scan)
    for gear in gears:
        print(f'{gear} {gear.ratio()}')
    total = sum(gear.ratio() for gear in gears)
    print(total)

def pull_gears(schematic_scan)->list[Gear]:
    gears: list[Gear] = []
    for symbol in schematic_scan.symbols:
        if symbol.value != '*':
            continue
        adjacent_part_numbers = get_adjacent_part_numbers(schematic_scan, symbol)
        if len(adjacent_part_numbers) == 2:
            gears.append(Gear(symbol, adjacent_part_numbers))
    return gears

def pull_part_numbers_adjacent_to_symbols(schematic_scan: SchematicScan)->list[PartNumber]:
    part_numbers: dict[int, PartNumber] = {}
    for symbol in schematic_scan.symbols:
        for part_number in get_adjacent_part_numbers(schematic_scan, symbol):
            part_numbers[part_number.instance_id] = part_number
    return list(part_numbers.values())

def get_adjacent_part_numbers(schematic_scan: SchematicScan, symbol: Symbol)->list[PartNumber]:
    part_numbers: dict[int, PartNumber] = {}
    for point in get_adjacent_points(schematic_scan, symbol.pos):
        for part_number in schematic_scan.part_numbers:
            if part_number.contains_point(point):
                if not (part_number.instance_id in part_numbers.keys()):
                    print(f'{symbol} {point} {part_number} {part_number.contains_point(point)}')
                    part_numbers[part_number.instance_id] = part_number
    return list(part_numbers.values())

def scan_schematic(schematic_text: str) -> SchematicScan:
    next_instance_id = 1
    schematic = schematic_text.splitlines()
    size: Point = Point(0, len(schematic))
    part_numbers: list[PartNumber] = []
    symbols: list[Symbol] = []
    for y, line in enumerate(schematic):
        size.x = max(size.x, len(line))
        building_part_number_text = ''
        for x, ch in enumerate(line):
            if ch.isdigit():
                building_part_number_text += ch
            else:
                if len(building_part_number_text) > 0:
                    part_numbers.append(PartNumber(next_instance_id, int(building_part_number_text), Point(x - len(building_part_number_text), y)))
                    next_instance_id += 1
                    building_part_number_text = ''
                if ch in symbol_characters:
                    symbols.append(Symbol(ch, Point(x, y)))
                elif ch != '.':
                    raise Exception(f'MISSING SYMBOL: {ch}')
        if len(building_part_number_text) > 0:
            part_numbers.append(PartNumber(next_instance_id, int(building_part_number_text), Point(x - len(building_part_number_text), y)))
            next_instance_id += 1
    return SchematicScan(size, part_numbers, symbols)

def get_adjacent_points(schematic_scan: SchematicScan, point: Point)->list[Point]:
    adjacent_points: list[Point] = []
    for y2 in range(-1, 2, 1):
        for x2 in range(-1, 2, 1):
            if x2 != 0 or y2 != 0:
                adjacent_point = Point(point.x + x2, point.y + y2)
                if is_point_inbounds(schematic_scan, adjacent_point):
                    adjacent_points.append(adjacent_point)
    return adjacent_points

def is_point_inbounds(schematic_scan: SchematicScan, point: Point)->bool:
    return point.x >= 0 and point.y >= 0 and point.x < schematic_scan.size.x and point.y < schematic_scan.size.y

main()
