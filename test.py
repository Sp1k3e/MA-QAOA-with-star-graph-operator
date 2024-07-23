def generate_combinations(options, length, current_combination, index, result):
    if index == length:
        result.append(current_combination.copy())
        return

    for choice in options:
        current_combination[index] = choice
        generate_combinations(options, length, current_combination, index + 1, result)

options = ['A', 'B', 'C']

length = 3  # 比如列表有3个元素

result = []

current_combination = [None] * length

generate_combinations(options, length, current_combination, 0, result)

for combination in result:
    print(combination)


