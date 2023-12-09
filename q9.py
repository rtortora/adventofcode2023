def parse_line(line: str)->list[int]:
    return [int(x) for x in line.split(" ")]

def get_sequence_of_differences(values: list[int])->list[int]:
    return [values[i] - values[i - 1] for i in range(1, len(values))]

def is_all_zeros(values: list[int])->bool:
    return next((x for x in values if x != 0), None) is None

def extrapolate_next_value(values: list[int])->int:
    stack: list[list[int]] = [values]
    while not is_all_zeros(values):
        values = get_sequence_of_differences(values)
        stack.append(values)
    stack[-1].append(0)
    for i in range(len(stack) - 2, -1, -1):
        stack[i].append(stack[i][-1] + stack[i + 1][-1])
    return stack[0][-1]

def main():
    print(extrapolate_next_value([0, 3, 6, 9, 12, 15]))
    print(extrapolate_next_value([1, 3, 6, 10, 15, 21]))
    print(extrapolate_next_value([10, 13, 16, 21, 30, 45]))

    with open("./inputs/q9.txt", encoding="utf-8") as file:
        lines = file.read().splitlines()
        sum = 0
        for line in lines:
            next_value = extrapolate_next_value(parse_line(line))
            sum += next_value
            print(f'{next_value} {sum}')
        print(f'FINAL: {sum}')

main()
