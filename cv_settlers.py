import cv2
import matplotlib.pyplot as plt
import numpy as np

cap = cv2.VideoCapture(1)
img = None
frame = None
cont = None
tiles = []

while cap.isOpened():
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    image, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cont = contours[1:]

    # For finding the baseline measurement of the area of a 2inx2in cube
    # largest = 0
    # for shape in cont:
    #     area = cv2.contourArea(shape)
    #     if area > largest:
    #         largest = area
    #
    # for shape in cont:
    #     if cv2.contourArea(shape) >= largest or cv2.contourArea(shape) < largest - 100:
    #         large_cont = shape

    # frame = cv2.drawContours(frame, [large_cont], -1, (0, 255, 0), 3)
    frame = cv2.drawContours(frame, cont, -1, (0, 255, 0), 3)

    cv2.imshow('contour detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # img = frame
        break

# print(largest)

while cap.isOpened():
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    final = np.zeros(frame.shape, np.uint8)
    mask = np.zeros(gray.shape, np.uint8)

    for i in range(0, len(cont)):
        if cv2.contourArea(cont[i]) > 18500:
            mask[...] = 0
            cv2.drawContours(mask, cont, i, 255, -1)
            cv2.drawContours(frame, cont, i, cv2.mean(frame, mask), -1)

    cv2.imshow('colored contours', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
