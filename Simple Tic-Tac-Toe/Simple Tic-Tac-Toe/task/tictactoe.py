result = ""
sym = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
queue = ["X", "O"]
x_wins = ["X", "X", "X"]
o_wins = ["O", "O", "O"]
n = 0


def print_matrix():
    print(f"""---------
| {sym[0]} {sym[1]} {sym[2]} |
| {sym[3]} {sym[4]} {sym[5]} |
| {sym[6]} {sym[7]} {sym[8]} |
---------""")


while result == "":
    rows = [sym[0:3], sym[3:6], sym[6:9]]
    columns = [sym[0:7:3], sym[1:8:3], sym[2:9:3]]
    diagonals = [sym[0:9:4], sym[2:7:2]]
    matrix = [rows, columns, diagonals]
    print_matrix()
    for sequences in matrix:
        for sequence in sequences:
            if sequence == x_wins:
                result = "X wins"
            if sequence == o_wins:
                result = "O wins"
    if result != "":
        continue
    empty = [x for x in sym if x == " "]
    if len(empty) == 0:
        result = "Draw"
        continue
    try:
        coord = [int(x) for x in input().split()]
        if coord[0] in [1, 2, 3] and coord[1] in [1, 2, 3]:
            if coord[0] == 1:
                index = coord[1] - 1
                if sym[index] != " ":
                    print("This cell is occupied! Choose another one!")
                else:
                    sym[index] = queue[n]
            elif coord[0] == 2:
                index = sum(coord)
                if sym[index] != " ":
                    print("This cell is occupied! Choose another one!")
                else:
                    sym[index] = queue[n]
            elif coord[0] == 3:
                index = 2 * coord[0] + coord[1] - 1
                if sym[index] != " ":
                    print("This cell is occupied! Choose another one!")
                else:
                    sym[index] = queue[n]
        else:
            print("Coordinates should be from 1 to 3!")
    except ValueError:
        print("You should enter numbers!")
    n = abs(n - 1)
print(result)
