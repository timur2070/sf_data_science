layout = [
    [' ', '0', '1', '2'],
    ['0', '-', '-', '-'],
    ['1', '-', '-', '-'],
    ['2', '-', '-', '-']
]

mark_letter ='X'

def mark_rotator():
    global mark_letter
    if mark_letter == 'X':
        mark_letter = 'O'
    else:
        mark_letter = 'X'

def print_layout():
    for i in layout:
        str1 = ' '
        print(str1.join(i))

#returns the position selection in a list format
def play():
    print_layout()
    print(f'Enter the position you want to place {mark_letter} sign in the format 0 0: ')
    position = list(input().split())
    if not "".join(position).isnumeric():
        print("Please enter the numbers only.")
        play()
    position = list(map(int, position))
    if len(position) != 2:
        print("Check the number of arguments you enter.")
        play()

    if isValidSelection(position):
        mark_cell(position)
        #print_layout()
        if isWin():
            print(f'The {mark_letter} is WON!')
            return 0
        else:
            mark_rotator()
            play()
    else:
        play()


def isValidSelection(position):
    row, col = position[0] + 1, position[1] + 1

    if row > 3 or row < 1 or col > 3 or col < 1:
        print('Your selection is out of boundaries. Please re-enter the position.')
        return False
    elif layout[row][col] != '-':
        print('The selected cell is already been marked. Make another cell selection.')
        return False
    else:
        return True

def mark_cell(position):
    row, col = position[0] + 1, position[1] + 1
    layout[row][col] = mark_letter


def isWin():
    global layout
    global mark_letter
    #horizontal check
    for row in layout:
        if "".join(row[1::]) == mark_letter * 3:
            return True

    #vertical check
    rotated_layout_tuple = list(zip(*layout))
    rotated_layout = []
    for row in rotated_layout_tuple:
        rotated_layout.append(list(row))

    for row in rotated_layout:
        if "".join(row[1::]) == mark_letter * 3:
            return True

    #cross check
    cross_check1 = []
    for i in range(1, 4):
        cross_check1.append(layout[i][i])
    if "".join(cross_check1) == mark_letter * 3:
        return True

    cross_check2 = []

    i = 1
    j = 3
    for i in range(1, 4):
        cross_check2.append(layout[i][j])
        j -= 1

    if "".join(cross_check2) == mark_letter * 3:
        return True

    return False

play()