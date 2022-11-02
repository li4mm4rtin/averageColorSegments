import numpy as np
import sys
import cv2
from tkinter import filedialog
import os

np.set_printoptions(threshold=sys.maxsize)


# Find the average of a region of the image based on the region borders passed as arguments.
# img: array of color data, cStart: int defining the start of the cell in the x-direction in the array, colWidthValue:
# int defining the width of the cell, rStart: int defining the start of the cell in the y-direction, rowHeightValue:
# int defining the height of the cell, colCount: int defining col, rowCount: int defining row
def findRegionAverage(img: np.ndarray, cStart: int, colWidthValue: int, rStart: int, rowHeightValue: int,
                      colCount: int, rowCount: int):
    color = np.full(3, 0)
    count = 0
    for xPosition in range(int(colWidthValue)):
        for yPosition in range(int(rowHeightValue)):
            pixel = img[int(rStart + yPosition), int(cStart + xPosition), :]
            color += pixel
            count += 1
    if count == 0:
        count = 1

    print("Average Calculated For Cell (%2d, %2d)" % (rowCount + 1, colCount + 1))

    if np.all(np.isin(color, [0, 0, 0])):
        return [0, 1, 1]
    else:
        return color * 1 / count


imageFile = filedialog.askopenfilename(title='Select Image File')

print("Loaded File: " + imageFile)

image = cv2.imread(imageFile)
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Calculate the mean of the rows. Identifies the grid lines in the x-direction
rowmeans = np.mean(image_gray, axis=1)
rowthresh = np.where(rowmeans < 1, 255, 0)
diffs = rowthresh[:-1] - rowthresh[1:]
rowStarts, rowEnds = [0], []

for i, v in enumerate(diffs):
    if v > 0:
        rowStarts.append(i)
    if v < 0:
        rowEnds.append(i)

rowEnds.append(image_gray.shape[0])

# Calculate the mean of the cols. Identifies the grid lines in the y-direction
colmeans = np.mean(image_gray, axis=0)
colthresh = np.where(colmeans < 1, 255, 0)
diffs = colthresh[:-1] - colthresh[1:]

if not colmeans[0] == 0:
    colStarts, colEnds = [0], []
else:
    colStarts, colEnds = [], []
for i, v in enumerate(diffs):
    if v > 0:
        colStarts.append(i)
    if v < 0:
        colEnds.append(i)

if len(colStarts) > len(colEnds):
    colEnds.append(image_gray.shape[1])

colWidth = np.array(colEnds) - np.array(colStarts)
rowHeight = np.array(rowEnds) - np.array(rowStarts)

print("Identified Grid of Shape (%2d, %2d)" % (len(rowHeight), len(colWidth)))

averageColor = np.full((len(rowHeight), len(colWidth), 3), -1)

for i in range(len(colWidth)):
    for j in range(len(rowHeight)):
        averageColor[j, i, :] = findRegionAverage(image, colStarts[i], colWidth[i], rowStarts[j], rowHeight[j], i, j)

cv2.imwrite(os.path.join(os.path.dirname(imageFile), os.path.basename(imageFile)[:-5] + '_averagePixel.png'),
            averageColor)
# np.savetxt(os.path.join(os.path.dirname(imageFile), os.path.basename(imageFile)[:-5]+"_averageBlueData.csv"),
#            averageColor[:, :, 0], delimiter=",")
# np.savetxt(os.path.join(os.path.dirname(imageFile), os.path.basename(imageFile)[:-5]+"_averageGreenData.csv"),
#            averageColor[:, :, 1], delimiter=",")
# np.savetxt(os.path.join(os.path.dirname(imageFile), os.path.basename(imageFile)[:-5]+"_averageRedData.csv"),
#            averageColor[:, :, 2], delimiter=",")
np.savetxt(os.path.join(os.path.dirname(imageFile), os.path.basename(imageFile)[:-5] + "_averageBlueRatio.csv"),
           averageColor[:, :, 0] / (averageColor[:, :, 1] + averageColor[:, :, 2]), delimiter=",")
