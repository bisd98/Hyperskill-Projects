def check_if_01(base):
    for i in base:
        if i not in '01':
            return False
    return True


print("Please give AI some data to learn...")
final_string = ''
while len(final_string) < 100:
    input_string = input(f"Current data length is {len(final_string)}"
                         f", {100 - len(final_string)} symbols left"
                         "\nPrint a random string containing 0 or 1:")
    final_string += ''.join(i for i in input_string if i in '01')
print(f"\nFinal data string:\n{final_string}\n\n"
      'You have $1000. Every time the system successfully predicts your next press, you lose $1.\n'
      'Otherwise, you earn $1. Print "enough" to leave the game. Let\'s go!\n')
triads = ['000', '001', '010', '011', '100', '101', '110', '111']
result = dict.fromkeys(triads)
parts = [final_string[index:index + 4] for index in range(0, len(final_string) - 3)]
for x in triads:
    res_0 = parts.count(x + '0')
    res_1 = parts.count(x + '1')
    result[x] = [res_0, res_1]
user_input = ''
balance = 1000
while user_input != 'enough':
    user_input = input('Print a random string containing 0 or 1:\n')
    if not check_if_01(user_input):
        continue
    pre_length = len(user_input)
    prediction = user_input[0:3]
    correct = 0
    for i in range(3, pre_length):
        x = result[user_input[i - 3:i]]
        prediction += '0' if x[0] > x[1] else '1'
        if prediction[i] == user_input[i]:
            correct += 1
    balance -= correct - ((pre_length - 3) - correct)
    print(f'prediction:\n{prediction}\n'
          f'\nComputer guessed right {correct} out of {pre_length - 3} '
          f'symbols ({((correct / (pre_length - 3)) * 100):.2f} %)\n'
          f'Your balance is now ${balance}\n')
print('Game over!')
