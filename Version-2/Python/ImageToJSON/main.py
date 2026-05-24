import cv2
import numpy as np

imagePath = "C:\\Not_Onedrive\\GitHub\\SIP-Project-2026\\Version-2\\Python\\ImageToJSON\\Images\\Test_Square.png"

image = cv2.imread(imagePath, 0)

imageBlurred = cv2.GaussianBlur(image, (3,3), 0)
imageEdges = cv2.Canny(image=imageBlurred, threshold1=80, threshold2=90) # Canny Edge Detection

cv2.imwrite("C:\\Not_Onedrive\\GitHub\\SIP-Project-2026\\Version-2\\Python\\ImageToJSON\\Images\\Detected_Edges.png", imageEdges)


cdstP = cv2.cvtColor(imageEdges, cv2.COLOR_GRAY2BGR)

lines = cv2.HoughLinesP(imageEdges, 1, np.pi / 180, 50, None, 5, 100)

if lines is not None:
    for i in range(0, len(lines)):
        l = lines[i][0]
        cv2.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 4, cv2.LINE_AA)

cv2.imwrite("C:\\Not_Onedrive\\GitHub\\SIP-Project-2026\\Version-2\\Python\\ImageToJSON\\Images\\Detected_Lines.png", cdstP)

scaleAmount = 0.4
imageScaled = cv2.resize(cdstP, None, fx=scaleAmount, fy=scaleAmount, interpolation=cv2.INTER_LINEAR)
imageRotated = cv2.rotate(imageScaled, cv2.ROTATE_90_CLOCKWISE)

cv2.imshow('Test', imageRotated)

cv2.waitKey()