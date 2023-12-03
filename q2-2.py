import re
import functools

testinput="""Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

"""Represents a single drawing, has counts by color"""
class Drawing:
    red = 0
    green = 0
    blue = 0

    def __init__(self, red: int, green: int, blue: int):
        self.red = red
        self.green = green
        self.blue = blue

    def set(self, key: str, value: int):
        if key == "red":
            self.red = value
        elif key == "green":
            self.green = value
        elif key == "blue":
            self.blue = value
        else:
            raise Error(f'Unexpected key {key}')
    
    def power(self):
        return self.red * self.green * self.blue

    def __repr__(self):
        return f'Drawing({self.red}, {self.green}, {self.blue})'

"""Represents a game, a collection of drawings"""
class Game:
    game_number = 0
    drawings = []

    def __init__(self, game_number: int, drawings):
        self.game_number = game_number
        self.drawings = drawings

    def __repr__(self):
        return f'Game({self.game_number}, {self.drawings})'

    def get_min_drawing(self):
        min = Drawing(0, 0, 0)
        for drawing in self.drawings:
            min.red = max(min.red, drawing.red)
            min.green = max(min.green, drawing.green)
            min.blue = max(min.blue, drawing.blue)
        return min

def parse_games(text: str):
    return list(map(lambda game_text: parse_game(game_text), text.splitlines()))

def parse_game(line: str):
    game_text, *drawing_texts = re.split(r'[:;] ?', line)
    _, game_num_text = game_text.split(' ')
    game = Game(int(game_num_text), [])
    for drawing_text in drawing_texts:
        parts_text = re.split(r', *', drawing_text)
        drawing = Drawing(0, 0, 0)
        for part_text in parts_text:
            number_text, color_text = part_text.split(' ')
            drawing.set(color_text, int(number_text))
        game.drawings.append(drawing)
    return game

# def get_max_draws(game): 
#     max_drawing = Drawing(0, 0, 0)
#     for drawing in game.drawings:
#         max_drawing.red = max(max_drawing.red, drawing.red)
#         max_drawing.green = max(max_drawing.green, drawing.green)
#         max_drawing.blue = max(max_drawing.blue, drawing.blue)
#     return max_drawing

# def does_pass_test(game):
#     max_draws = get_max_draws(game)
#     return max_draws.red <= 12 and max_draws.green <= 13 and max_draws.blue <= 14

# def sum_game_ids_that_pass_test(games) -> int:
#     sum = 0
#     for game in games:
#         if does_pass_test(game):
#             sum += game.game_number
#     return sum

def main():
    #games = parse_games(testinput)
    games = parse_games(open("./q2-1-input.txt").read())
    sum = 0
    for game in games:
        min_drawing = game.get_min_drawing()
        #print(f'game {game.game_number} {min_drawing} {min_drawing.power()}')
        sum += min_drawing.power()
    print(f'ANSWER: {sum}')

main()

