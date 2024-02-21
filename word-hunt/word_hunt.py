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
    
def manualFix(puzzle):
    r = ""
    c = ""
    v = ""

    while(True):
        r = input("Row: ")
        if r == "": break
        else: r = int(r)
        c = int(input("Column: "))
        v = input("Value: ")
        
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





    
    