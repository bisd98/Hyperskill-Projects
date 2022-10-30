# write your code here
msg_0 = "Enter an equation"
msg_1 = "Do you even know what numbers are? Stay focused!"
msg_2 = "Yes ... an interesting math operation. You've slept through all classes, haven't you?"
msg_3 = "Yeah... division by zero. Smart move..."
msg_4 = "Do you want to store the result? (y / n):"
msg_5 = "Do you want to continue calculations? (y / n):"
msg_6 = " ... lazy"
msg_7 = " ... very lazy"
msg_8 = " ... very, very lazy"
msg_9 = "You are"
msg_10 = "Are you sure? It is only one digit! (y / n)"
msg_11 = "Don't be silly! It's just one number! Add to the memory? (y / n)"
msg_12 = "Last chance! Do you really want to embarrass yourself? (y / n)"
msg_ = [msg_0, msg_1, msg_2, msg_3, msg_4, msg_5, msg_6, msg_7, msg_8, msg_9, msg_10, msg_11, msg_12]


def check(v1, v2, v3):
    msg = ""
    if is_one_digit(v1) and is_one_digit(v2):
        msg = msg + msg_6
    if (v1 == 1 or v2 == 1) and v3 == '*':
        msg = msg + msg_7
    if (v1 == 0 or v2 == 0) and v3 in ['*', '+', '-']:
        msg = msg + msg_8
    if msg != "":
        msg = msg_9 + msg
        print(msg)


def is_one_digit(v):
    if (v - int(v) == 0) and (-10 < v < 10):
        return True
    else:
        return False


memory = 0
while True:
    calc = input(msg_0 + '\n')
    x, o, y = calc.split()
    if x == "M":
        x = memory
    if y == "M":
        y = memory
    try:
        answer = 0
        result = 0
        float(x) and float(y)
        if o not in ['+', '-', '/', '*']:
            print(msg_2)
        else:
            check(float(x), float(y), o)
            if o == "+":
                print(float(x) + float(y))
                result = float(x) + float(y)
            elif o == "-":
                print(float(x) - float(y))
                result = float(x) - float(y)
            elif o == "*":
                print(float(x) * float(y))
                result = float(x) * float(y)
            elif o == "/":
                try:
                    print(float(x) / float(y))
                    result = float(x) / float(y)
                except ZeroDivisionError:
                    print(msg_3)
                    continue
        while answer not in ['y', 'n']:
            print(msg_4)
            answer = input()
            if answer == "y":
                if is_one_digit(result):
                    msg_index = 10
                    answer = 0
                    while answer == 'y' or answer != 'n':
                        print(msg_[msg_index])
                        answer = input()
                        if answer == 'y':
                            if msg_index < 12:
                                msg_index += 1
                            else:
                                memory = result
                                break
                    if answer == 'n':
                        break
            memory = result
        answer = 0
        while answer not in ['y', 'n']:
            print(msg_5)
            answer = input()
            if answer == "n":
                exit()
    except ValueError:
        print(msg_1)
