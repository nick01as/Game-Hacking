import cv2
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import time
from sentence_transformers import SentenceTransformer, util
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import numpy.ma as ma

processor = TrOCRProcessor.from_pretrained('microsoft/trocr-small-printed')
model = VisionEncoderDecoderModel.from_pretrained('microsoft/trocr-small-printed')

def processFrame(frame):
    return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


def findPhone(frame):
    frame = imutils.resize(frame, height = 500)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 50, 200, 255)

    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = [c for c in cnts if cv2.contourArea(c) > 120000]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    if len(cnts) > 0:
        cnts = cnts[0]
        displayCnt = None

        peri = cv2.arcLength(cnts, True)
        approx = cv2.approxPolyDP(cnts, 0.02 * peri, True)

        if len(approx) == 4:
            displayCnt = approx
        
        if displayCnt is not None:
            warped = four_point_transform(gray, displayCnt.reshape(4, 2))
            warped = cv2.resize(warped, (540,540))
            # cv2.imshow("warped",warped)
            # cv2.waitKey()
            return (True, warped)
    return (False, None)

def ocr(image):
    pixel_values = processor(image, return_tensors='pt').pixel_values
    generated_ids = model.generate(pixel_values)
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return generated_text

def detectNumber(cell):

    digit = 0
    if np.mean(cell) < 245:
        cell = Image.fromarray(cell)

        try:
            digit = int(ocr(cell))
        except:
            print("Please rescan puzzle: \n  - Hold phone flat and parallel to screen\n  - Center puzzle\n  - Reduce glare")
            return -1

    return digit

def getCells(puzzle):

    thresh = cv2.adaptiveThreshold(puzzle, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 5)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    puzzle = ((puzzle < thresh).astype(np.uint8)) * 255
    puzzle = cv2.morphologyEx(puzzle, cv2.MORPH_OPEN, kernel, iterations=1) 

    allCells = np.zeros(shape=(9,9))
    for i in range(9):
        for j in range(9):
            x,y,w,h, = (i * 60 + 5, j * 60 + 5, 50,50)
            cell = puzzle[x:x+w, y:y+h].copy()
            cell = cv2.cvtColor(cell, cv2.COLOR_GRAY2RGB)
            allCells[i][j] = detectNumber(cell)
            if int(allCells[i][j]) == -1:
                return None

    return allCells