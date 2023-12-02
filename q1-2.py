test_data = """two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""

digit_spellings = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
digit_spellings_by_direction = {
  1: digit_spellings,
  -1: list(map(lambda word: word[::-1], digit_spellings)),
}

def main():
  #sum_calibration_values(test_data)
  sum_calibration_values(open("./q1-1-input.txt").read())

def sum_calibration_values(input):
  sum = 0
  for line in input.splitlines():
    first_digit = find_first_or_last_digit(line, 1)
    if first_digit is None:
      print(f'No first digit in: {line}')
    last_digit = find_first_or_last_digit(line, -1)
    if last_digit is None:
      print(f'No last digit, first digit was {first_digit} in: {line}')
    number = first_digit * 10 + last_digit
    sum += number
    print(f'{line}: {number}')
  print(f'FINAL: {sum}')

def find_first_or_last_digit(str, direction):
  if direction == -1:
    str = str[::-1]
  for index, ch in enumerate(str):
    if is_digit(ch):
      return int(ch)
    for number, word in enumerate(digit_spellings_by_direction[direction]):
      if str[index:].startswith(word):
        return number
  return None

def is_digit(ch):
  return ord(ch) >= ord('0') and ord(ch) <= ord('9')

main()
