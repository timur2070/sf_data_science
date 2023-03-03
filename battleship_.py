from random import randint


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Dot({self.x}, {self.y})"


class BoardException(Exception):
    pass


class BoardOutException(BoardException):
    def __str__(self):
        return "You trying to shoot against the Board border!"


class BoardBusyException(BoardException):
    def __str__(self):
        return  "You already shoot in this cell!"


class BoardWrongException(BoardException):
    pass


class Ship:
    def __init__(self, bow, length, orientation):
        self.bow = bow
        self.length = length
        self.orientation = orientation

        self.lives = length

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.length):
            cur_x = self.bow.x
            cur_y = self.bow.y
            if self.orientation == 0:
                cur_y += i
            elif self.orientation == 1:
                cur_x += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots


class Board:
    def __init__(self, hidden=False, size=6):
        self.size = size
        self.hidden = hidden
        self.count = 0
        self.field = [ ["0"] * self.size for _ in range(self.size) ]

        self.ships = []
        self.busy = []


    def __str__(self):
        res = "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i in range(self.size):
            res += f"\n{i + 1} | " + " | ".join(self.field[i]) + " |"

        if self.hidden:
            res = res.replace("■", "0")
        return res

    def add_ship(self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:
                raise BoardBusyException()
        for d in ship.dots:
            self.busy.append(d)
            self.field[d.x][d.y] = "■"
        self.ships.append(ship)
        self.contour(ship)

    def contour(self, ship, verb=False):
        near = [
                (-1, -1), (-1, 0), (-1, 1),
                (0, -1), (0, 0), (0, 1),
                (1, -1), (1, 0), (1, 1)
               ]
        for dx, dy in near:
            for d in ship.dots:
                if Dot(d.x + dx, d.y + dy) not in self.busy and not self.out(Dot(d.x + dx, d.y + dy)):
                    if verb:
                        self.field[d.x + dx][d.y + dy] = "."
                    self.busy.append(Dot(d.x + dx, d.y + dy))

    def out(self, d):
        return not ((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def shot(self, d):
        if self.out(d):
            raise BoardOutException()

        if d in self.busy:
            raise BoardBusyException()

        self.busy.append(d)

        for ship in self.ships:
            if d in ship.dots:
                ship.lives -= 1
                if ship.lives == 0:
                    self.field[d.x][d.y] = "X"
                    print("The ship was destoyed")
                    self.contour(ship, verb=True)
                    return False
                else:
                    self.field[d.x][d.y] = "X"
                    print("The ship is damaged")
                    return True

            print("You missed!")
            self.field[d.x][d.y] = "."
            return False



    def begin(self):
        self.busy = []


class Player:
    def __init__(self, my_board, enemy_board):
        self.my_board = my_board
        self.enemy_board = enemy_board

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy_board.shot(target)
                return repeat
            except BoardException as e:
                print(e)

class AI(Player):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f"Computer move is: {d.x + 1} {d.y + 1}")
        return d


class User(Player):
    def ask(self):
        while True:
            d = input("Please enter the coordinates: ").split()
            if len(d) != 2:
                print("Please enter ONLY two coordinates!")
                continue
            x, y = d

            if not (x.isdigit()) or not (y.isdigit()):
                print("Please enter only digits")
                continue
            x, y = int(x), int(y)
            return Dot(x - 1, y - 1)

class Game:
    def __init__(self, size=6):
        self.size = size
        human_board = self.random_board()
        computer_board = self.random_board()
        computer_board.hid = True

        self.human = User(human_board, computer_board)
        self.ai = AI(computer_board, human_board)

    def random_board(self):
        board = None
        while board is None:
            board = self.random_place()
        return board


    def random_place(self):
        lens = [4, 2, 2, 1, 1, 1, 1]
        board = Board(size=self.size)
        attempts = 0

        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0, 1))
                try:
                    board.add_ship(ship)
                    break
                except BoardBusyException:
                    pass
        board.begin()
        return board

    def greet(self):
        print("Welcome to the Game")

    def loop(self):
        num = 0
        while True:
            print("-" * 20)
            print("The Player Board:")
            print(self.human.my_board)
            print("-" * 20)
            print("The Computer Board:")
            print(self.ai.my_board)
            if num % 2 == 0:
                print("-" * 20)
                print("The players move: ")
                repeat = self.human.move()
            else:
                print("-" * 20)
                print("The computer move: ")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.human.my_board.count == 7:
                print("-" * 20)
                print("The computer WON")
                break

            if self.ai.my_board.count == 7:
                print("-" * 20)
                print("The Player WON")
                break

            num += 1

    def start(self):
        self.greet()
        self.loop()

# b1 = Board()
# s1 = Ship(Dot(randint(0, 5), randint(0, 5)), 4, randint(0, 1))
# s2 = Ship(Dot(randint(0, 5), randint(0, 5)), 2, randint(0, 1))
# s3 = Ship(Dot(randint(0, 5), randint(0, 5)), 1, randint(0, 1))
# b1.add_ship(s1)
# b1.add_ship(s2)
# b1.add_ship(s3)
# print(b1)

g1 = Game()
g1.start()


