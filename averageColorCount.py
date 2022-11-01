import numpy as np
from PIL import Image
import sys
import cv2
from tkinter import filedialog
import os

Image.MAX_IMAGE_PIXELS = 224834385
np.set_printoptions(threshold=sys.maxsize)


def findRegionAverage(img, cStart, colWidthValue, rStart, rowHeightValue, colCount, rowCount):
    color = np.full(3, 0)
    count = 0
    for xPosition in range(int(colWidthValue)):
        for yPosition in range(int(rowHeightValue)):
            pixel = img[int(rStart + yPosition), int(cStart + xPosition), :]
            # if not :
            color += pixel
            count += 1
    if count == 0:
        count = 1

    print("Average Calculated For Cell (%2d, %2d)"% (rowCount+1, colCount+1))

    if np.all(np.isin(color, [0, 0, 0])):
        return [0, 1, 1]
    else:
        return color * 1 / count


imageFile = filedialog.askopenfilename(title='Select Image File')

print("Loaded File: " + imageFile)

pimRGB = Image.open(imageFile)
pimgrey = pimRGB.convert('L')
nimRGB = np.array(pimRGB)
nimgrey = np.array(pimgrey)

rowmeans = np.mean(nimgrey, axis=1)
rowthresh = np.where(rowmeans < 1, 255, 0)
diffs = rowthresh[:-1] - rowthresh[1:]
rowStarts, rowEnds = [0], []
for i, v in enumerate(diffs):
    if v > 0:
        rowStarts.append(i)
    if v < 0:
        rowEnds.append(i)

rowEnds.append(nimgrey.shape[0])

colmeans = np.mean(nimgrey, axis=0)
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
    colEnds.append(nimgrey.shape[1])

colWidth = np.array(colEnds) - np.array(colStarts)
rowHeight = np.array(rowEnds) - np.array(rowStarts)

print("Identified Grid of Shape (%2d, %2d)" % (len(rowHeight), len(colWidth)))

averageColor = np.full((len(rowHeight), len(colWidth), 3), -1)

image_tt = cv2.imread(imageFile)

for i in range(len(colWidth)):
    for j in range(len(rowHeight)):
        averageColor[j, i, :] = findRegionAverage(image_tt, colStarts[i], colWidth[i], rowStarts[j], rowHeight[j], i, j)

cv2.imwrite(os.path.join(os.path.dirname(imageFile), os.path.basename(imageFile)[:-5]+'_averagePixel.png'),
            averageColor)
# np.savetxt(os.path.join(os.path.dirname(imageFile), os.path.basename(imageFile)[:-5]+"_averageBlueData.csv"),
#            averageColor[:, :, 0], delimiter=",")
# np.savetxt(os.path.join(os.path.dirname(imageFile), os.path.basename(imageFile)[:-5]+"_averageGreenData.csv"),
#            averageColor[:, :, 1], delimiter=",")
# np.savetxt(os.path.join(os.path.dirname(imageFile), os.path.basename(imageFile)[:-5]+"_averageRedData.csv"),
#            averageColor[:, :, 2], delimiter=",")
np.savetxt(os.path.join(os.path.dirname(imageFile), os.path.basename(imageFile)[:-5]+"_averageBlueRatio.csv"),
           averageColor[:, :, 0]/(averageColor[:, :, 1]+averageColor[:, :, 2]), delimiter=",")
