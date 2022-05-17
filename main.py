import re
from tkinter import Y

class GameEngine():
    def __init__(self):
        self.row_size = 10
        self.col_size = 10
        self.player1 = Board(self.row_size,self.col_size)
        self.setupBoard(self.player1)

    def setupBoard(self, player):
        shipSizes = [5,4,3,3,2]
        player.printBoard()
        while len(shipSizes) > 0:
            coordinates = input("Ship Coordinates:").upper().split(',')
            if len(coordinates) in shipSizes:
                if all(player.checkCoordinate(coordinate) for coordinate in coordinates):
                    if player.checkShipsOrientation(coordinates):
                        player.createShip(coordinates)
                        shipSizes.remove(len(coordinates))
                        print("Ship Created: " + str(coordinates) + " size: " + str(len(coordinates)))
                        player.printShips()

                else:
                    print('ERROR')
            else:
                print("ERROR")
                


class Board():
    def __init__(self, row_size, col_size):
        self.row_size = row_size
        self.col_size = col_size
        self.board = [[0] * col_size for x in range(row_size)]
        self.ships = []

    def createShip(self, coordinates):
        self.ships += [Ship(coordinates)]

    def checkCoordinate(self, coordinate):
        if ord(coordinate[0]) >= ord('A') and ord(coordinate[0]) < ord('A') + self.col_size:
            if coordinate[1:].isnumeric():
                if int(coordinate[1:]) >= 0 and int(coordinate[1:]) <= self.col_size:
                    return True
        return False
    
    def checkShipsOrientation(self, coordinates):
        xCoordinates = sorted([ord(coordinate[0]) - ord('A') for coordinate in coordinates])
        yCoordinates = sorted([int(coordinate[1:]) for coordinate in coordinates])
        x = all(cordinaat == xCoordinates[0] for cordinaat in xCoordinates)
        y = all(cordinaat == yCoordinates[0] for cordinaat in yCoordinates)
        if x != y:
            if x: return all(y-x==1 for x,y in zip(yCoordinates, yCoordinates[1:]))
            if y: return all(y-x==1 for x,y in zip(xCoordinates, xCoordinates[1:]))
        return False

    def checkCordinaatAnyShip(self, coordinate):
        return any(ship.checkCoordinate(coordinate) for ship in self.ships)
       
    def printBoard(self):
        print("\n   " + " ".join(chr(x + ord('A')) for x in range(0, self.col_size )))
        for r in range(self.row_size):
            print(str(r + 1) + ("  " if r <= 8 else " ") +  " ".join(str(c) for c in self.board[r]))
        print()

    def printShips(self):
        print("\n   " + " ".join(chr(x + ord('A')) for x in range(0, self.col_size )))
        for r in range(self.row_size):
            print(str(r + 1) + ("  " if r <= 8 else " ") +  " ".join(str('x' if self.checkCordinaatAnyShip([c,r+1]) else self.board[c][r]) for c in range(self.col_size)))
        print()

class Ship():
    def __init__(self, coordinates):
        self.coordinates = [[ord(coordinate[0])-ord('A'),int(coordinate[1:])] for coordinate in coordinates]
        self.size = len(coordinates)

    def checkCoordinate(self, coordinate):
        if coordinate in self.coordinates:
            return True
        return False



gameEngine = GameEngine()