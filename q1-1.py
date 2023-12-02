test_data = """1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet"""

def main():
  #sum_calibration_values(test_data)
  sum_calibration_values(open("./q1-1-input.txt").read())

def sum_calibration_values(input):
  sum = 0
  for line in input.splitlines():
    first_digit = find_first_digit(line)
    last_digit = find_last_digit(line)
    number = int(first_digit + last_digit)
    sum += number
    print(f'{line}: {number}')
  print(f'FINAL: {sum}')

def find_first_digit(str):
  for _, ch in enumerate(str):
    if is_digit(ch):
      return ch
  return None

def find_last_digit(str):
  return find_first_digit(str[::-1])

def is_digit(ch):
  return ord(ch) >= ord('0') and ord(ch) <= ord('9')

main()
