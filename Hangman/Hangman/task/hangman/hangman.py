import random
won = 0
lost = 0
attempts = 8
print("H A N G M A N\n")
answers = ["python", "java", "swift", "javascript"]
while True:
    choice = input('Type "play" to play the game, "results" to show the scoreboard, and "exit" to quit:')
    if choice == "play":
        right = random.choice(answers)
        word = list(len(right) * '-')
        tried = list()
        while attempts > 0:
            print("".join(word))
            answer = input('Input a letter:')
            if len(answer) != 1:
                print("Please, input a single letter.")
                continue
            elif not answer.islower():
                print("Please, enter a lowercase letter from the English alphabet.")
                continue
            if answer in tried:
                print("You've already guessed this letter.")
                continue
            elif answer not in right:
                print("That letter doesn't appear in the word.")
            else:
                attempts += 1
                for i in range(len(right)):
                    if answer == right[i]:
                        word[i] = answer
            tried.append(answer)
            if "".join(word) == right:
                won += 1
                print(f"You guessed the word {right}!\nYou survived!")
                break
            attempts -= 1
            if attempts == 0:
                lost += 1
                print("You lost!")
    elif choice == "results":
        print(f"""You won: {won} times.
    You lost: {lost} times.""")
    else:
        exit()
