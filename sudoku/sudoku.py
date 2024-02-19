import cv2
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import time
import sys
import warnings

import camera
import parseFrame

solution = None

def getNextCell(puzzle):
    for i in range(9):
        for j in range(9):
            if int(puzzle[i][j]) == 0:return (i,j)
    return (-1,-1)

def used(puzzle, r, c, val):
    for i in range(9):
        if (val == puzzle[r][i]) or (val == puzzle[i][c]):
            return True
        
    x = (r // 3) * 3
    y = (c // 3) * 3

    for i in range(x, x + 3):
        if val in puzzle[i][y:y+3]:
            return True

    return False

def solvePuzzle(puzzle, r, c, depth):
    if r == -1: return puzzle

    for num in range(1,10):
        if not used(puzzle, r, c, num):
            puzzle[r][c] = num

            if getNextCell(puzzle) == -1:
                return puzzle
            else:
                new_r, new_c = getNextCell(puzzle)
                sol = solvePuzzle(puzzle, new_r, new_c, depth+1)

                if sol is not None and getNextCell(sol)[0] == -1:
                    return sol
                else:
                    puzzle[r][c] = 0
    
    return None
    
def manualFix(puzzle):
    r = ""
    c = ""
    v = ""

    while(True):
        r = input("Row: ")
        if r == "": break
        else: r = int(r)
        c = int(input("Column: "))
        v = int(input("Value: "))
        
        puzzle[r-1][c-1] = v
        print("\n")
        print(puzzle)
        print("\n")

    print("\n")
    return puzzle

def getInputs():
    puzzle = None
    correct = None

    while(puzzle is None or correct != 'y'):
        puzzle = camera.scanPuzzle()
        puzzle = parseFrame.getCells(puzzle)

        if puzzle is not None:
            puzzle = puzzle.astype(np.uint8)
            print(puzzle)

            correct = input("Correct Puzzle? (y/n): ").lower()
            
            if correct == 'n':
                option = input("Retry scan / Manual fix: (r/m): ").lower()

                if option == 'm':
                    puzzle = manualFix(puzzle)
                    break

    return puzzle

if __name__ == "__main__":
    warnings.filterwarnings('ignore')
    sys.setrecursionlimit(10000)

    puzzle = getInputs()

    print("\nsolving...")
    r, c = getNextCell(puzzle)
    if r != -1:
        print("\nSolution: ")
        print(solvePuzzle(puzzle, r, c, 0))



    
    