from dataclasses import dataclass
import re

test_input = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""

@dataclass
class Card:
  id: int
  answers: set[int]
  numbers: set[int]

  def winning_numbers(self)->set[int]:
    return self.answers & self.numbers

  def score(self)->int:
    winning_numbers = self.winning_numbers()
    if len(winning_numbers) == 0:
      return 0
    return 2 ** (len(self.winning_numbers()) - 1)

def parse_card(card_text: str)->Card:
  id, answers_text, _, numbers_text, _ = re.match(r"Card +(\d+):(( *\d+)*) \| (( *\d+)*)", card_text).groups()
  answers = set(int(v) for v in re.split(r' +', answers_text.strip()))
  numbers = set(int(v) for v in re.split(r' +', numbers_text.strip()))
  return Card(id, answers, numbers)

def parse_cards(card_texts: str)->list[Card]:
  return list(parse_card(line) for line in card_texts.splitlines())

def q1(input: str):
  cards = parse_cards(input)
  for card in cards:
    print(f'{card} winning={card.winning_numbers()} score={card.score()}')
  total = sum(card.score() for card in cards)
  print(f'{total}')

def main():
  q1(test_input)
  q1(open("./inputs/q4.txt").read())

main()
