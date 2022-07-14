import cv2
import numpy as np
import sys
from tkinter import filedialog
import csv
import os

np.set_printoptions(threshold=sys.maxsize)

imageFile = filedialog.askopenfilename(title='Select Image File')

image = cv2.imread(imageFile)

cols = 0
rows = 0
width = 0
colWidth = np.zeros(0)
height = 0
rowHeight = np.zeros(0)

for i in range(image.shape[1]):
    if np.all(np.isin(image[5, i, :], [0, 0, 0])):
        cols += 1
        colWidth = np.append(colWidth, width)
        width = -1
    elif i == image.shape[1] - 1:
        colWidth = np.append(colWidth, width)

    width += 1

for i in range(image.shape[0]):
    if np.all(np.isin(image[i, 5, :], [0, 0, 0])):
        rows += 1
        rowHeight = np.append(rowHeight, height)
        height = -1
    elif i == image.shape[0] - 1:
        rowHeight = np.append(rowHeight, height)

    height += 1

if rowHeight[0] == 0:
    rowHeight = rowHeight[1:]
if colWidth[0] == 0:
    colWidth = colWidth[1:]


def findRegionAverage(img, cStart, colWidthValue, rStart, rowHeightValue):
    color = np.full(3, 0)
    count = 0
    for xPosition in range(int(colWidthValue)):
        for yPosition in range(int(rowHeightValue)):
            color += img[int(rStart + yPosition), int(cStart + xPosition), :]
            # print(img[cStart + xPosition, rStart + yPosition, :][0], img[cStart + xPosition, rStart + yPosition, :][1], img[cStart + xPosition, rStart + yPosition, :][2])
            count += 1
        # print(' ')

    if count == 0:
        count = 1

    return color * 1/count


colStart = 0

averageColor = np.full((len(rowHeight), len(colWidth), 3), -1)

for i in range(len(colWidth)):
    rowStart = 0
    for j in range(len(rowHeight)):
        averageColor[j, i, :] = findRegionAverage(image, colStart, colWidth[i], rowStart, rowHeight[j])
        rowStart = rowStart + rowHeight[j] + 1
    colStart = colStart + colWidth[i] + 1


cv2.imwrite(os.path.join(os.path.dirname(imageFile), os.path.basename(imageFile)[:-5]+'_averagePixel.png'), averageColor)
# np.savetxt(os.path.join(os.path.dirname(imageFile), os.path.basename(imageFile)[:-5]+"_averageBlueData.csv"), averageColor[:, :, 0], delimiter=",")
# np.savetxt(os.path.join(os.path.dirname(imageFile), os.path.basename(imageFile)[:-5]+"_averageGreenData.csv"), averageColor[:, :, 1], delimiter=",")
# np.savetxt(os.path.join(os.path.dirname(imageFile), os.path.basename(imageFile)[:-5]+"_averageRedData.csv"), averageColor[:, :, 2], delimiter=",")

