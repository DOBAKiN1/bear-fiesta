import curses
from colorama import init
import random

init()


class Tile:
    X = -1
    Y = -1
    displaySymbol = "!"
    isPassable = True


class Grass(Tile):
    def __init__(self, grassX, grassY):
        self.X = grassX
        self.Y = grassY
        self.displaySymbol = ","
        self.foodAmount = 0  # When player step on it becomes dirt
        # self.tileUnder = tileUnder


class Dirt(Tile):
    def __init__(self, dirtX, dirtY):
        self.X = dirtX
        self.Y = dirtY
        self.displaySymbol = "."


class Barrier(Tile):
    def __init__(self, barrierX, barrierY):
        self.X = barrierX
        self.Y = barrierY
        self.displaySymbol = "#"
        self.isPassable = False


class Player(Tile):
    def __init__(self, playerX, playerY):
        self.X = playerX
        self.Y = playerY
        self.displaySymbol = "B"


class SmallWater(Tile):
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.displaySymbol = "V"


class BigWater(Tile):
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.displaySymbol = "W"
        self.isPassable = False


class Tree(Tile):
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.displaySymbol = "T"
        self.foodAmount = 10


class Mushroom(Tile):
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.displaySymbol = "M"
        self.foodAmount = 10


class Fish(Tile):
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.displaySymbol = "~"
        self.foodAmount = 5


class Wolf(Tile):
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.displaySymbol = "K"
        self.foodAmount = 10
        self.currentTile = Dirt(X, Y)


class Deer(Tile):
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.displaySymbol = "D"
        self.foodAmount = 20
        self.currentTile = Dirt(X, Y)


class Cave(Tile):
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.displaySymbol = "C"
        self.isPassable = True


class End(Tile):
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.displaySymbol = "&"
        self.isPassable = True


class Error(Tile):  # ticket ^To be implemented^
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y
        self.displaySymbol = "E"
        self.isPassable = False


class GameField:
    wolfList = []
    mushroomList = []
    field = []
    caveField = []
    grassList = []
    treeList = []
    bigWaterList = []
    smallWaterList = []
    fishList = []
    dirtList = []
    caveDirtList = []
    deerList = []

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.caveWidth = 10
        self.caveHeight = 10
        self.timeStop = 0
        self.playerClass = Player(width // 2, height // 2)
        self.playerClassInCave = Player(10 // 2, 10 // 2)
        self.currentTile = Dirt(width // 2, height // 2)
        self.grassOnMapCap = 200
        self.fishOnMapCap = 3
        self.treesOnMapCap = 10
        self.wolvesOnMapCap = 5
        self.deerOnMapCap = 3
        self.food = 0
        self.caveMode = False
        self.caveModeExit = False
        self.moveStat = 0
        self.fishStat = 0
        self.treeStat = 0
        self.wolfStat = 0
        self.worldGeneration()

    def worldGeneration(self):
        for j in range(self.height):
            row = []
            for i in range(self.width):
                if i == 0 or i == self.width - 1 or j == 0 or j == self.height - 1:
                    row.append(Barrier(i, j))
                else:
                    if i == self.playerClass.X and j == self.playerClass.Y:
                        row.append(self.currentTile)
                    else:
                        newDirt = Dirt(i, j)
                        row.append(newDirt)
                        self.dirtList.append(newDirt)

            self.field.append(row)

        self.field[self.playerClass.Y][self.playerClass.X] = self.playerClass

        self.waterGeneration()
        self.treeGeneration()
        self.caveGeneration()
        self.caveFieldGeneration()
        self.caveEndGeneration()
        self.caveMushroomGeneration()

    def waterGeneration(self):
        random_corner = random.randint(1, 4)
        smallWaterRange = 20
        bigWaterRange = 14

        if random_corner == 1:
            for j in range(1, bigWaterRange):
                for i in range(1, bigWaterRange - j):
                    self.dirtList.remove(self.field[j][i])
                    newBigWater = BigWater(i, j)
                    self.field[j][i] = newBigWater
                    self.bigWaterList.append(newBigWater)
        elif random_corner == 2:
            for j in range(1, bigWaterRange):
                for i in range(self.width - bigWaterRange + j, self.width - 1):
                    self.dirtList.remove(self.field[j][i])
                    newBigWater = BigWater(i, j)
                    self.field[j][i] = newBigWater
                    self.bigWaterList.append(newBigWater)
        elif random_corner == 3:
            for j in range(self.height - bigWaterRange, self.height - 1):
                for i in range(1, bigWaterRange - (self.height - j - 1)):
                    self.dirtList.remove(self.field[j][i])
                    newBigWater = BigWater(i, j)
                    self.field[j][i] = newBigWater
                    self.bigWaterList.append(newBigWater)
        elif random_corner == 4:
            for j in range(self.height - bigWaterRange, self.height - 1):
                for i in range(self.width - bigWaterRange + (self.height - j - 1), self.width - 1):
                    self.dirtList.remove(self.field[j][i])
                    newBigWater = BigWater(i, j)
                    self.field[j][i] = newBigWater
                    self.bigWaterList.append(newBigWater)

        if random_corner == 1:  # left up
            for j in range(1, smallWaterRange):
                for i in range(1, smallWaterRange - j):
                    if isinstance(self.field[j][i], Dirt):
                        self.dirtList.remove(self.field[j][i])
                        newSmallWater = SmallWater(i, j)
                        self.field[j][i] = newSmallWater
                        self.smallWaterList.append(newSmallWater)
        elif random_corner == 2:  # right up
            for j in range(1, smallWaterRange):
                for i in range(self.width - smallWaterRange + j, self.width - 1):
                    if isinstance(self.field[j][i], Dirt):
                        self.dirtList.remove(self.field[j][i])
                        newSmallWater = SmallWater(i, j)
                        self.field[j][i] = newSmallWater
                        self.smallWaterList.append(newSmallWater)
        elif random_corner == 3:  # down left
            for j in range(self.height - smallWaterRange, self.height - 1):
                for i in range(1, smallWaterRange - (self.height - j - 1)):
                    if isinstance(self.field[j][i], Dirt):
                        self.dirtList.remove(self.field[j][i])
                        newSmallWater = SmallWater(i, j)
                        self.field[j][i] = newSmallWater
                        self.smallWaterList.append(newSmallWater)
        elif random_corner == 4:  # down right
            for j in range(self.height - smallWaterRange, self.height - 1):
                for i in range(self.width - smallWaterRange + (self.height - j - 1), self.width - 1):
                    if isinstance(self.field[j][i], Dirt):
                        self.dirtList.remove(self.field[j][i])
                        newSmallWater = SmallWater(i, j)
                        self.field[j][i] = newSmallWater
                        self.smallWaterList.append(newSmallWater)

    def caveGeneration(self):
        randomX = random.randint(2, self.width - 2)
        randomY = random.randint(2, self.height - 2)
        if isinstance(self.field[randomY][randomX], Dirt):
            newCave = Cave(randomX, randomY)
            self.dirtList.remove(self.field[randomY][randomX])
            self.field[randomY][randomX] = newCave
        else:
            while not isinstance(self.field[randomY][randomX], Dirt):
                randomX = random.randint(2, self.width - 2)
                randomY = random.randint(2, self.height - 2)
            newCave = Cave(randomX, randomY)
            self.dirtList.remove(self.field[randomY][randomX])
            self.field[randomY][randomX] = newCave

    def caveEndGeneration(self):
        randomX = 2
        randomY = 2
        if isinstance(self.caveField[randomY][randomX], Dirt):
            newEnd = End(randomX, randomY)
            self.caveDirtList.remove(self.caveField[randomY][randomX])
            self.caveField[randomY][randomX] = newEnd
        else:
            while not isinstance(self.caveField[randomY][randomX], Dirt):
                randomX = random.randint(2, self.width - 2)
                randomY = random.randint(2, self.height - 2)
            newEnd = End(randomX, randomY)
            self.caveDirtList.remove(self.caveField[randomY][randomX])
            self.caveField[randomY][randomX] = newEnd

    def caveFieldGeneration(self):
        for j in range(self.caveHeight):
            row = []
            for i in range(self.caveWidth):
                if i == 0 or i == self.caveWidth - 1 or j == 0 or j == self.caveHeight - 1:
                    row.append(Barrier(i, j))
                else:
                    if i == self.playerClassInCave.X and j == self.playerClassInCave.Y:
                        newDirt = Dirt(i, j)
                        row.append(newDirt)
                        self.caveDirtList.append(newDirt)
                    else:
                        newDirt = Dirt(i, j)
                        row.append(newDirt)
                        self.caveDirtList.append(newDirt)

            self.caveField.append(row)

        self.caveField[self.playerClassInCave.Y][self.playerClassInCave.X] = self.playerClassInCave

    def caveMushroomGeneration(self):
        count = random.randint(5, 10)
        for _ in range(count):
            randomX = random.randint(2, self.caveWidth - 2)
            randomY = random.randint(2, self.caveHeight - 2)
            if isinstance(self.caveField[randomY][randomX], Dirt):
                newMushroom = Mushroom(randomX, randomY)
                self.caveDirtList.remove(self.caveField[randomY][randomX])
                self.caveField[randomY][randomX] = newMushroom
                self.mushroomList.append(newMushroom)
            else:
                while not isinstance(self.caveField[randomY][randomX], Dirt):
                    randomX = random.randint(2, self.caveWidth - 2)
                    randomY = random.randint(2, self.caveHeight - 2)
                newMushroom = Mushroom(randomX, randomY)
                self.caveDirtList.remove(self.caveField[randomY][randomX])
                self.caveField[randomY][randomX] = newMushroom
                self.mushroomList.append(newMushroom)

    def treeGeneration(self):
        count = random.randint(2, 5)
        for _ in range(count):
            randomX = random.randint(2, self.width - 2)
            randomY = random.randint(2, self.height - 2)
            if isinstance(self.field[randomY][randomX], Dirt):
                newTree = Tree(randomX, randomY)
                self.dirtList.remove(self.field[randomY][randomX])
                self.field[randomY][randomX] = newTree
                self.treeList.append(newTree)
            else:
                while not isinstance(self.field[randomY][randomX], Dirt):
                    randomX = random.randint(2, self.width - 2)
                    randomY = random.randint(2, self.height - 2)
                newTree = Tree(randomX, randomY)
                self.dirtList.remove(self.field[randomY][randomX])
                self.field[randomY][randomX] = newTree
                self.treeList.append(newTree)

    def display(self, stdscr):
        if self.caveMode is False:
            stdscr.addstr(0, 0, "Кількість їжі: " + str(self.food))
            for row in self.field:
                if len(row) != self.width:
                    somethingWrong = 1
                tileCounter = 0
                for tile in row:

                    if tile.displaySymbol == 'B':
                        stdscr.addstr(tile.Y + 1, tile.X, tile.displaySymbol, curses.color_pair(1))
                    elif tile.displaySymbol == '~':
                        stdscr.addstr(tile.Y + 1, tile.X, tile.displaySymbol, curses.color_pair(2))
                    elif tile.displaySymbol == ',':
                        stdscr.addstr(tile.Y + 1, tile.X, tile.displaySymbol, curses.color_pair(3))
                    elif tile.displaySymbol == '.' or tile.displaySymbol == "#" or tile.displaySymbol == "C":
                        stdscr.addstr(tile.Y + 1, tile.X, tile.displaySymbol, curses.color_pair(4))
                    elif tile.displaySymbol == 'W':
                        stdscr.addstr(tile.Y + 1, tile.X, tile.displaySymbol, curses.color_pair(5))
                    elif tile.displaySymbol == 'V':
                        stdscr.addstr(tile.Y + 1, tile.X, tile.displaySymbol, curses.color_pair(6))
                    elif tile.displaySymbol == 'T':
                        stdscr.addstr(tile.Y + 1, tile.X, tile.displaySymbol, curses.color_pair(7))
                    elif tile.displaySymbol == 'K':
                        stdscr.addstr(tile.Y + 1, tile.X, tile.displaySymbol, curses.color_pair(8))
                    elif tile.displaySymbol == 'D' or tile.displaySymbol == 'M':
                        stdscr.addstr(tile.Y + 1, tile.X, tile.displaySymbol, curses.color_pair(9))
                    else:
                        stdscr.addstr(tile.Y + 1, tile.X, "E", curses.color_pair(1))
                    tileCounter += 1
        else:
            stdscr.addstr(0, 0, "Кількість їжі: " + str(self.food))
            for row in self.caveField:
                tileCounter = 0
                for tile in row:

                    if tile.displaySymbol == 'B':
                        stdscr.addstr(tile.Y + 1, tile.X, tile.displaySymbol, curses.color_pair(1))
                    elif tile.displaySymbol == ',':
                        stdscr.addstr(tile.Y + 1, tile.X, tile.displaySymbol, curses.color_pair(3))
                    elif tile.displaySymbol == '.' or tile.displaySymbol == "#" or tile.displaySymbol == "C":
                        stdscr.addstr(tile.Y + 1, tile.X, tile.displaySymbol, curses.color_pair(4))
                    elif tile.displaySymbol == '&':
                        stdscr.addstr(tile.Y + 1, tile.X, tile.displaySymbol, curses.color_pair(4))
                    elif tile.displaySymbol == 'M':
                        stdscr.addstr(tile.Y + 1, tile.X, tile.displaySymbol, curses.color_pair(9))
                    else:
                        stdscr.addstr(tile.Y + 1, tile.X, "E", curses.color_pair(1))

                    tileCounter += 1

    def move_player(self, direction):
        if self.caveMode is False:
            if direction == 'up':
                if not self.field[self.playerClass.Y - 1][self.playerClass.X].isPassable:
                    return
                if hasattr(self.field[self.playerClass.Y - 1][self.playerClass.X], "foodAmount"):
                    self.food += self.field[self.playerClass.Y - 1][self.playerClass.X].foodAmount
                    self.field[self.playerClass.Y - 1][self.playerClass.X] = self.wasEaten(
                        self.field[self.playerClass.Y - 1][self.playerClass.X])
                if isinstance(self.currentTile, Dirt):
                    self.dirtList.append(self.currentTile)
                elif isinstance(self.currentTile, SmallWater):
                    self.smallWaterList.append(self.currentTile)
                self.field[self.playerClass.Y][self.playerClass.X] = self.currentTile
                self.playerClass.Y -= 1
                self.currentTile = self.field[self.playerClass.Y][self.playerClass.X]
                if isinstance(self.currentTile, Dirt):
                    self.dirtList.remove(self.currentTile)
                elif isinstance(self.currentTile, SmallWater):
                    self.smallWaterList.remove(self.currentTile)
                self.moveStat += 1
            elif direction == 'down':
                if not self.field[self.playerClass.Y + 1][self.playerClass.X].isPassable:
                    return
                if hasattr(self.field[self.playerClass.Y + 1][self.playerClass.X], "foodAmount"):
                    self.food += self.field[self.playerClass.Y + 1][self.playerClass.X].foodAmount
                    self.field[self.playerClass.Y + 1][self.playerClass.X] = self.wasEaten(
                        self.field[self.playerClass.Y + 1][self.playerClass.X])
                if isinstance(self.currentTile, Dirt):
                    self.dirtList.append(self.currentTile)
                elif isinstance(self.currentTile, SmallWater):
                    self.smallWaterList.append(self.currentTile)
                self.field[self.playerClass.Y][self.playerClass.X] = self.currentTile
                self.playerClass.Y += 1
                self.currentTile = self.field[self.playerClass.Y][self.playerClass.X]
                if isinstance(self.currentTile, Dirt):
                    self.dirtList.remove(self.currentTile)
                elif isinstance(self.currentTile, SmallWater):
                    self.smallWaterList.remove(self.currentTile)
                self.moveStat += 1
            elif direction == 'left':
                if not self.field[self.playerClass.Y][self.playerClass.X - 1].isPassable:
                    return
                if hasattr(self.field[self.playerClass.Y][self.playerClass.X - 1], "foodAmount"):
                    self.food += self.field[self.playerClass.Y][self.playerClass.X - 1].foodAmount
                    self.field[self.playerClass.Y][self.playerClass.X - 1] = self.wasEaten(
                        self.field[self.playerClass.Y][self.playerClass.X - 1])
                if isinstance(self.currentTile, Dirt):
                    self.dirtList.append(self.currentTile)
                elif isinstance(self.currentTile, SmallWater):
                    self.smallWaterList.append(self.currentTile)
                self.field[self.playerClass.Y][self.playerClass.X] = self.currentTile
                self.playerClass.X -= 1
                self.currentTile = self.field[self.playerClass.Y][self.playerClass.X]
                if isinstance(self.currentTile, Dirt):
                    self.dirtList.remove(self.currentTile)
                elif isinstance(self.currentTile, SmallWater):
                    self.smallWaterList.remove(self.currentTile)
                self.moveStat += 1
            elif direction == 'right':
                if not self.field[self.playerClass.Y][self.playerClass.X + 1].isPassable:
                    return
                if hasattr(self.field[self.playerClass.Y][self.playerClass.X + 1], "foodAmount"):
                    self.food += self.field[self.playerClass.Y][self.playerClass.X + 1].foodAmount
                    self.field[self.playerClass.Y][self.playerClass.X + 1] = self.wasEaten(
                        self.field[self.playerClass.Y][self.playerClass.X + 1])
                if isinstance(self.currentTile, Dirt):
                    self.dirtList.append(self.currentTile)
                elif isinstance(self.currentTile, SmallWater):
                    self.smallWaterList.append(self.currentTile)
                self.field[self.playerClass.Y][self.playerClass.X] = self.currentTile
                self.playerClass.X += 1
                self.currentTile = self.field[self.playerClass.Y][self.playerClass.X]
                if isinstance(self.currentTile, Dirt):
                    self.dirtList.remove(self.currentTile)
                elif isinstance(self.currentTile, SmallWater):
                    self.smallWaterList.remove(self.currentTile)
                self.moveStat += 1

            self.field[self.playerClass.Y][self.playerClass.X] = self.playerClass
        if self.caveMode is True:
            if direction == 'up':
                if not self.caveField[self.playerClassInCave.Y - 1][self.playerClassInCave.X].isPassable:
                    return
                if hasattr(self.caveField[self.playerClassInCave.Y - 1][self.playerClassInCave.X], "foodAmount"):
                    self.food += self.caveField[self.playerClassInCave.Y - 1][self.playerClassInCave.X].foodAmount
                    self.caveField[self.playerClassInCave.Y - 1][self.playerClassInCave.X] = self.wasEaten(
                        self.caveField[self.playerClassInCave.Y - 1][self.playerClassInCave.X])
                self.caveField[self.playerClassInCave.Y][self.playerClassInCave.X] = self.currentTile
                self.playerClassInCave.Y -= 1
                self.currentTile = self.caveField[self.playerClassInCave.Y][self.playerClassInCave.X]
                self.moveStat += 1
            elif direction == 'down':
                if not self.caveField[self.playerClassInCave.Y + 1][self.playerClassInCave.X].isPassable:
                    return
                if hasattr(self.caveField[self.playerClassInCave.Y + 1][self.playerClassInCave.X], "foodAmount"):
                    self.food += self.caveField[self.playerClassInCave.Y + 1][self.playerClassInCave.X].foodAmount
                    self.caveField[self.playerClassInCave.Y + 1][self.playerClassInCave.X] = self.wasEaten(
                        self.caveField[self.playerClassInCave.Y + 1][self.playerClassInCave.X])
                self.caveField[self.playerClassInCave.Y][self.playerClassInCave.X] = self.currentTile
                self.playerClassInCave.Y += 1
                self.currentTile = self.caveField[self.playerClassInCave.Y][self.playerClassInCave.X]
                self.moveStat += 1
            elif direction == 'left':
                if not self.caveField[self.playerClassInCave.Y][self.playerClassInCave.X - 1].isPassable:
                    return
                if hasattr(self.caveField[self.playerClassInCave.Y][self.playerClassInCave.X - 1], "foodAmount"):
                    self.food += self.caveField[self.playerClassInCave.Y][self.playerClassInCave.X - 1].foodAmount
                    self.caveField[self.playerClassInCave.Y][self.playerClassInCave.X - 1] = self.wasEaten(
                        self.caveField[self.playerClassInCave.Y][self.playerClassInCave.X - 1])
                self.caveField[self.playerClassInCave.Y][self.playerClassInCave.X] = self.currentTile
                self.playerClassInCave.X -= 1
                self.currentTile = self.caveField[self.playerClassInCave.Y][self.playerClassInCave.X]
                self.moveStat += 1
            elif direction == 'right':
                if not self.caveField[self.playerClassInCave.Y][self.playerClassInCave.X + 1].isPassable:
                    return
                if hasattr(self.caveField[self.playerClassInCave.Y][self.playerClassInCave.X + 1], "foodAmount"):
                    self.food += self.caveField[self.playerClassInCave.Y][self.playerClassInCave.X + 1].foodAmount
                    self.caveField[self.playerClassInCave.Y][self.playerClassInCave.X + 1] = self.wasEaten(
                        self.caveField[self.playerClassInCave.Y][self.playerClassInCave.X + 1])
                self.caveField[self.playerClassInCave.Y][self.playerClassInCave.X] = self.currentTile
                self.playerClassInCave.X += 1
                self.currentTile = self.caveField[self.playerClassInCave.Y][self.playerClassInCave.X]
                self.moveStat += 1

            self.caveField[self.playerClassInCave.Y][self.playerClassInCave.X] = self.playerClassInCave

    def makeTick(self):
        if self.caveMode is False:
            self.treesGrowGrass()
            self.growTrees()
            self.fishSwim()
            self.moveWolf()
            self.spawnFish()
            self.spawnWolf()
            # self.spawnDeer()
            self.growGrass()
            self.isOnCave()

        else:
            if self.playerClassInCave.X == 2 and self.playerClassInCave.Y == 2:
                if self.food >= 100:
                    print("Перемога")
                else:
                    print("Поразка")
                print("Кількість їжі", self.food)
                print("Кількість пройдених кроків:", self.moveStat)
                print("Кількість зловленої риби:", self.fishStat)
                print("Кількість зловлених вовків:", self.wolfStat)
                print("Кількість понищених дерев:", self.treeStat)

                exit(1)

    def moveWolf(self):
        wolfNumber = 1
        for wolf in self.wolfList:
            possible_moves = []

            # Check possible moves
            if wolf.Y > 0 and isinstance(self.field[wolf.Y - 1][wolf.X], Dirt) or \
                    wolf.Y > 0 and isinstance(self.field[wolf.Y - 1][wolf.X], Grass):
                possible_moves.append(('up', wolf.X, wolf.Y - 1))
            if wolf.Y < self.height - 1 and isinstance(self.field[wolf.Y + 1][wolf.X], Dirt) or \
                    wolf.Y > 0 and isinstance(self.field[wolf.Y + 1][wolf.X], Grass):
                possible_moves.append(('down', wolf.X, wolf.Y + 1))
            if wolf.X > 0 and isinstance(self.field[wolf.Y][wolf.X - 1], Dirt) or \
                    wolf.Y > 0 and isinstance(self.field[wolf.Y][wolf.X - 1], Grass):
                possible_moves.append(('left', wolf.X - 1, wolf.Y))
            if wolf.X < self.width - 1 and isinstance(self.field[wolf.Y][wolf.X + 1], Dirt) or \
                    wolf.Y > 0 and isinstance(self.field[wolf.Y][wolf.X + 1], Grass):
                possible_moves.append(('right', wolf.X + 1, wolf.Y))

            if possible_moves:
                # Check if player is nearby or at a distance of 5 tiles
                player_nearby = False
                for direction, x, y in possible_moves:
                    distance_to_player = abs(x - self.playerClass.X) + abs(y - self.playerClass.Y)
                    if distance_to_player <= 5:
                        player_nearby = True
                        break

                # Check if wolf is nearby or at a distance of 10 tiles
                wolf_nearby = False
                for direction, x, y in possible_moves:
                    for WOOOLF in self.wolfList:
                        if wolf != WOOOLF:
                            distance_to_wolf = abs(x - WOOOLF.X) + abs(y - WOOOLF.Y)
                            if distance_to_wolf <= 10:
                                wolf_nearby = True
                                break

                if player_nearby and wolf_nearby:
                    if isinstance(self.field[wolf.Y + 1][wolf.X], Player) or \
                            isinstance(self.field[wolf.Y - 1][wolf.X], Player) or \
                            isinstance(self.field[wolf.Y][wolf.X + 1], Player) or \
                            isinstance(self.field[wolf.Y][wolf.X - 1], Player):
                        self.food -= 5
                    # Wolf follows the player
                    new_moves = []
                    for direction, x, y in possible_moves:
                        if x < self.playerClass.X:
                            new_x = wolf.X + 1
                        elif x > self.playerClass.X:
                            new_x = wolf.X - 1
                        else:
                            new_x = wolf.X

                        if y < self.playerClass.Y:
                            new_y = wolf.Y + 1
                        elif y > self.playerClass.Y:
                            new_y = wolf.Y - 1
                        else:
                            new_y = wolf.Y

                        if isinstance(self.field[new_y][new_x], Dirt):
                            new_moves.append((direction, new_x, new_y))
                        if isinstance(self.field[new_y][new_x], Grass):
                            new_moves.append((direction, new_x, new_y))

                    if new_moves:
                        direction, new_x, new_y = random.choice(new_moves)
                        # Remove wolf from current location
                        if isinstance(self.field[new_y][new_x], Dirt):
                            self.dirtList.remove(self.field[new_y][new_x])
                            newTile = wolf.currentTile
                            if isinstance(newTile, Dirt):
                                self.field[wolf.Y][wolf.X] = newTile
                                self.dirtList.append(newTile)
                            if isinstance(newTile, Grass):
                                self.field[wolf.Y][wolf.X] = newTile
                                self.grassList.append(newTile)
                        elif isinstance(self.field[new_y][new_x], Grass):
                            self.grassList.remove(self.field[new_y][new_x])
                            newTile = wolf.currentTile
                            if isinstance(newTile, Dirt):
                                self.field[wolf.Y][wolf.X] = newTile
                                self.dirtList.append(newTile)
                            if isinstance(newTile, Grass):
                                self.field[wolf.Y][wolf.X] = newTile
                                self.grassList.append(newTile)
                        # Move wolf to new location
                        wolf.currentTile = self.field[new_y][new_x]
                        self.field[new_y][new_x] = wolf
                        wolf.X = new_x
                        wolf.Y = new_y
                elif player_nearby:
                    # Wolf flee away from the player
                    new_moves = []
                    for direction, x, y in possible_moves:
                        if x < self.playerClass.X:
                            new_x = wolf.X - 1
                        elif x > self.playerClass.X:
                            new_x = wolf.X + 1
                        else:
                            new_x = wolf.X

                        if y < self.playerClass.Y:
                            new_y = wolf.Y - 1
                        elif y > self.playerClass.Y:
                            new_y = wolf.Y + 1
                        else:
                            new_y = wolf.Y

                        if isinstance(self.field[new_y][new_x], Dirt):
                            new_moves.append((direction, new_x, new_y))
                        if isinstance(self.field[new_y][new_x], Grass):
                            new_moves.append((direction, new_x, new_y))

                    if new_moves:
                        direction, new_x, new_y = random.choice(new_moves)
                        # Remove wolf from current location
                        if isinstance(self.field[new_y][new_x], Dirt):
                            self.dirtList.remove(self.field[new_y][new_x])
                            newTile = wolf.currentTile
                            if isinstance(newTile, Dirt):
                                self.field[wolf.Y][wolf.X] = newTile
                                self.dirtList.append(newTile)
                            if isinstance(newTile, Grass):
                                self.field[wolf.Y][wolf.X] = newTile
                                self.grassList.append(newTile)
                        elif isinstance(self.field[new_y][new_x], Grass):
                            self.grassList.remove(self.field[new_y][new_x])
                            newTile = wolf.currentTile
                            if isinstance(newTile, Dirt):
                                self.field[wolf.Y][wolf.X] = newTile
                                self.dirtList.append(newTile)
                            if isinstance(newTile, Grass):
                                self.field[wolf.Y][wolf.X] = newTile
                                self.grassList.append(newTile)
                        # Move wolf to new location
                        wolf.currentTile = self.field[new_y][new_x]
                        self.field[new_y][new_x] = wolf
                        wolf.X = new_x
                        wolf.Y = new_y
                else:
                    # Wolf moves randomly
                    direction, new_x, new_y = random.choice(possible_moves)
                    # Remove wolf from current location
                    if isinstance(self.field[new_y][new_x], Dirt):
                        self.dirtList.remove(self.field[new_y][new_x])
                        newTile = wolf.currentTile
                        if isinstance(newTile, Dirt):
                            self.field[wolf.Y][wolf.X] = newTile
                            self.dirtList.append(newTile)
                        if isinstance(newTile, Grass):
                            self.field[wolf.Y][wolf.X] = newTile
                            self.grassList.append(newTile)
                    elif isinstance(self.field[new_y][new_x], Grass):
                        self.grassList.remove(self.field[new_y][new_x])
                        newTile = wolf.currentTile
                        if isinstance(newTile, Dirt):
                            self.field[wolf.Y][wolf.X] = newTile
                            self.dirtList.append(newTile)
                        if isinstance(newTile, Grass):
                            self.field[wolf.Y][wolf.X] = newTile
                            self.grassList.append(newTile)
                    # Move wolf to new location
                    wolf.currentTile = self.field[new_y][new_x]
                    self.field[new_y][new_x] = wolf
                    wolf.X = new_x
                    wolf.Y = new_y

    def isOnCave(self):
        if isinstance(self.currentTile, Cave):
            self.caveMode = True
            self.currentTile = Dirt(self.playerClassInCave.X, self.playerClassInCave.Y)
            return True

    def treesGrowGrass(self):
        grassCounter = 0
        whileCounter = 0
        while grassCounter < 4:
            if whileCounter > 100:  # Loop protection
                break

            if len(self.treeList) <= 0:
                return
            randomTree = random.choice(self.treeList)
            randomDirection = random.randint(1, 4)
            newX, newY = randomTree.X, randomTree.Y

            if randomDirection == 1 and newY > 0 and isinstance(self.field[newY - 1][newX], Dirt):
                newGrass = Grass(newX, newY - 1)
                self.dirtList.remove(self.field[newY - 1][newX])
                self.field[newY - 1][newX] = newGrass
                self.grassList.append(newGrass)
                grassCounter += 1
            elif randomDirection == 2 and newX < self.width - 1 and isinstance(self.field[newY][newX + 1], Dirt):
                newGrass = Grass(newX + 1, newY)
                self.dirtList.remove(self.field[newY][newX + 1])
                self.field[newY][newX + 1] = newGrass
                self.grassList.append(newGrass)
                grassCounter += 1
            elif randomDirection == 3 and newY < self.height - 1 and isinstance(self.field[newY + 1][newX], Dirt):
                newGrass = Grass(newX, newY + 1)
                self.dirtList.remove(self.field[newY + 1][newX])
                self.field[newY + 1][newX] = newGrass
                self.grassList.append(newGrass)
                grassCounter += 1
            elif randomDirection == 4 and newX > 0 and isinstance(self.field[newY][newX - 1], Dirt):
                newGrass = Grass(newX - 1, newY)
                self.dirtList.remove(self.field[newY][newX - 1])
                self.field[newY][newX - 1] = newGrass
                self.grassList.append(newGrass)
                grassCounter += 1
            whileCounter += 1

    def growGrass(self):
        grassCounter = 0
        whileCounter = 0
        if len(self.grassList) <= 0:
            return
        grassOnMap = len(self.grassList)
        if grassOnMap >= self.grassOnMapCap:
            return
        while grassCounter < 4:
            if whileCounter > 100:  # Loop protection
                break

            randomGrass = random.choice(self.grassList)
            randomDirection = random.randint(1, 4)
            newX, newY = randomGrass.X, randomGrass.Y

            if randomDirection == 1 and newY > 0 and isinstance(self.field[newY - 1][newX], Dirt):
                newGrass = Grass(newX, newY - 1)
                self.dirtList.remove(self.field[newY - 1][newX])
                self.field[newY - 1][newX] = newGrass
                self.grassList.append(newGrass)
                grassCounter += 1
            elif randomDirection == 2 and newX < self.width - 1 and isinstance(self.field[newY][newX + 1], Dirt):
                newGrass = Grass(newX + 1, newY)
                self.dirtList.remove(self.field[newY][newX + 1])
                self.field[newY][newX + 1] = newGrass
                self.grassList.append(newGrass)
                grassCounter += 1
            elif randomDirection == 3 and newY < self.height - 1 and isinstance(self.field[newY + 1][newX], Dirt):
                newGrass = Grass(newX, newY + 1)
                self.dirtList.remove(self.field[newY + 1][newX])
                self.field[newY + 1][newX] = newGrass
                self.grassList.append(newGrass)
                grassCounter += 1
            elif randomDirection == 4 and newX > 0 and isinstance(self.field[newY][newX - 1], Dirt):
                newGrass = Grass(newX - 1, newY)
                self.dirtList.remove(self.field[newY][newX - 1])
                self.field[newY][newX - 1] = newGrass
                self.grassList.append(newGrass)
                grassCounter += 1
            whileCounter += 1

    def growTrees(self):
        if len(self.dirtList) <= 0:
            return

        treesOnMap = len(self.treeList)
        if treesOnMap >= self.treesOnMapCap:
            return

        spawnChance = random.randint(1, 200)
        if spawnChance == 1:
            randomDirtTile = random.choice(self.dirtList)

            self.dirtList.remove(randomDirtTile)
            newTree = Tree(randomDirtTile.X, randomDirtTile.Y)
            self.field[randomDirtTile.Y][randomDirtTile.X] = newTree
            self.treeList.append(newTree)

    def spawnFish(self):
        if len(self.smallWaterList) <= 0:
            return

        fishOnMap = len(self.fishList)
        if fishOnMap >= self.fishOnMapCap:
            return

        spawnChance = random.randint(1, 100)
        if spawnChance == 1:
            randomWaterTile = random.choice(self.smallWaterList)
            newFish = Fish(randomWaterTile.X, randomWaterTile.Y)
            self.field[randomWaterTile.Y][randomWaterTile.X] = newFish
            self.smallWaterList.remove(randomWaterTile)
            self.fishList.append(newFish)

    def spawnWolf(self):
        if len(self.dirtList) <= 0:
            return

        wolvesOnMap = len(self.wolfList)
        if wolvesOnMap >= self.wolvesOnMapCap:
            return

        spawnChance = random.randint(1, 10)
        if spawnChance == 1:
            randomDirtTile = random.choice(self.dirtList)
            newWolf = Wolf(randomDirtTile.X, randomDirtTile.Y)
            self.field[randomDirtTile.Y][randomDirtTile.X] = newWolf
            self.dirtList.remove(randomDirtTile)
            self.wolfList.append(newWolf)

    def spawnDeer(self):
        if len(self.dirtList) <= 0:
            return

        deerOnMap = len(self.deerList)
        if deerOnMap >= self.deerOnMapCap:
            return

        spawnChance = random.randint(1, 100)
        if spawnChance == 1:
            randomDirtTile = random.choice(self.dirtList)
            newDeer = Deer(randomDirtTile.X, randomDirtTile.Y)
            self.field[randomDirtTile.Y][randomDirtTile.X] = newDeer
            self.dirtList.remove(randomDirtTile)
            self.deerList.append(newDeer)

    def wasEaten(self, tile):
        if tile.displaySymbol == "~":
            self.fishList.remove(tile)
            newSmallWater = SmallWater(tile.X, tile.Y)
            self.smallWaterList.append(newSmallWater)
            self.fishStat += 1
            return newSmallWater
        elif tile.displaySymbol == "T":
            self.treeList.remove(tile)
            newDirt = Dirt(tile.X, tile.Y)
            self.dirtList.append(newDirt)
            self.treeStat += 1
            return newDirt
        elif tile.displaySymbol == ",":
            self.grassList.remove(tile)
            newDirt = Dirt(tile.X, tile.Y)
            self.dirtList.append(newDirt)
            return newDirt
        elif tile.displaySymbol == "K":
            self.wolfList.remove(tile)
            newDirt = Dirt(tile.X, tile.Y)
            self.dirtList.append(newDirt)
            self.wolfStat += 1
            return newDirt
        elif tile.displaySymbol == "D":
            self.deerList.remove(tile)
            newDirt = Dirt(tile.X, tile.Y)
            self.dirtList.append(newDirt)
            return newDirt
        elif tile.displaySymbol == "M":
            self.mushroomList.remove(tile)
            newDirt = Dirt(tile.X, tile.Y)
            self.caveDirtList.append(newDirt)
            return newDirt
    def fishSwim(self):
        for fish in self.fishList:
            possible_moves = []

            # Check possible moves
            if fish.Y > 0 and isinstance(self.field[fish.Y - 1][fish.X], SmallWater):
                possible_moves.append(('up', fish.X, fish.Y - 1))
            if fish.Y < self.height - 1 and isinstance(self.field[fish.Y + 1][fish.X], SmallWater):
                possible_moves.append(('down', fish.X, fish.Y + 1))
            if fish.X > 0 and isinstance(self.field[fish.Y][fish.X - 1], SmallWater):
                possible_moves.append(('left', fish.X - 1, fish.Y))
            if fish.X < self.width - 1 and isinstance(self.field[fish.Y][fish.X + 1], SmallWater):
                possible_moves.append(('right', fish.X + 1, fish.Y))

            if possible_moves:
                # Check if player is nearby or at a distance of 2 tiles
                player_nearby = False
                for direction, x, y in possible_moves:
                    distance_to_player = abs(x - self.playerClass.X) + abs(y - self.playerClass.Y)
                    if distance_to_player <= 2:
                        player_nearby = True
                        break

                if player_nearby:
                    # Fish swims away from the player
                    new_moves = []
                    for direction, x, y in possible_moves:
                        if x < self.playerClass.X:
                            new_x = fish.X - 1
                        elif x > self.playerClass.X:
                            new_x = fish.X + 1
                        else:
                            new_x = fish.X

                        if y < self.playerClass.Y:
                            new_y = fish.Y - 1
                        elif y > self.playerClass.Y:
                            new_y = fish.Y + 1
                        else:
                            new_y = fish.Y

                        if isinstance(self.field[new_y][new_x], SmallWater):
                            new_moves.append((direction, new_x, new_y))

                    if new_moves:
                        direction, new_x, new_y = random.choice(new_moves)
                        self.field[fish.Y][fish.X] = SmallWater(fish.X, fish.Y)
                        self.field[new_y][new_x] = fish
                        fish.X = new_x
                        fish.Y = new_y

                else:
                    # Fish moves randomly
                    direction, new_x, new_y = random.choice(possible_moves)
                    self.field[fish.Y][fish.X] = SmallWater(fish.X, fish.Y)
                    self.field[new_y][new_x] = fish
                    fish.X = new_x
                    fish.Y = new_y


def colorInit():
    curses.init_color(curses.COLOR_WHITE, 700, 700, 700)
    curses.init_color(111, 245, 1000, 559)
    curses.init_color(88, 555, 555, 555)  # wolf
    curses.init_color(99, 612, 304, 0)  # deer
    curses.init_color(22, 306, 306, 510)  # fish

    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, 22, curses.COLOR_BLACK)
    curses.init_pair(3, 111, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(5, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(8, 88, curses.COLOR_BLACK)
    curses.init_pair(9, 99, curses.COLOR_BLACK)


def main(stdscr):
    curses.curs_set(0)

    stdscr.clear()
    stdscr.refresh()
    curses.start_color()

    colorInit()

    game = GameField(80, 20)  # -2 because of barriers

    count = 0
    nullCount = 0
    for row in game.field:
        count += len(row)

    for row in game.field:
        for tile in row:
            if tile is None:
                nullCount += 1


    while True:
        stdscr.clear()
        game.display(stdscr)
        stdscr.refresh()

        action = stdscr.getch()

        if action == curses.KEY_UP:
            direction = 'up'
        elif action == curses.KEY_DOWN:
            direction = 'down'
        elif action == curses.KEY_LEFT:
            direction = 'left'
        elif action == curses.KEY_RIGHT:
            direction = 'right'
        elif action == ord(' '):
            if game.timeStop == 0:
                game.makeTick()
            game.display(stdscr)
            continue
        elif action == ord('1'):
            direction = 'none'
            if game.timeStop == 0:
                game.timeStop = 1
            else:
                game.timeStop = 0
        elif action == 27:
            print("Клітинок в полі", count, "--- 1600?")
            print("Помиклових клітинок", nullCount)
            print("Земля", len(game.dirtList))
            print("Трава", len(game.grassList))
            print("Риба", len(game.fishList))
            print("Вовк", len(game.wolfList))
            # print("Deer", len(game.deerList))
            print("Дерева", len(game.treeList))
            print("Мала вода", len(game.smallWaterList))
            print("Велика вода", len(game.bigWaterList))
            print("Сума клітинок", len(game.dirtList) + len(game.wolfList) + len(game.grassList) + len(game.fishList) +
                  len(game.treeList) + len(game.smallWaterList) + len(game.bigWaterList) + len(game.deerList) +
                  game.width * 2 + (game.height - 2) * 2 + 1 + 1)  # +1 is player +1 is cave
            print("Земля в печері", len(game.caveDirtList))
            count = 0
            for row in game.caveField:
                count += len(row)
            print("Клітинок в печері", count)  # +1 is player
            print("Сума клітинок печери", len(game.caveDirtList) + 1 + 20 + 16)  # +1 is player
            break
        else:
            continue
        if game.timeStop == 0:
            game.makeTick()
        game.display(stdscr)
        game.move_player(direction)

    curses.endwin()


curses.wrapper(main)
