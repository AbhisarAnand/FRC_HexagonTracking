import math

import cv2
import imutils
import numpy as np

global smallRatio
smallRatio = 0.2
global bigRatio
bigRatio = 0.5
global color
color = (0, 0, 255)
global i
i = 0
global cap
cap = cv2.VideoCapture("/dev/video0")
# cap = cv2.VideoCapture("/dev/video2")
global last_cnts
last_cnts = []


def get_angle(a, b, c):
    ang = int(abs(math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))))
    return ang


def distance_calc(width):
    distance = (40 * 56) // width
    return distance


def distance_from_center_to_hexagon(hexCenterX, hexCenterY, midpointX, midpointY):
    distance1 = math.sqrt((hexCenterX - midpointX) ** 2 + (hexCenterY - midpointY) ** 2)
    return distance1


def detection():
    f = 0
    if len(cnts) == 1:
        print("CONTOURS: ", len(cnts))
        for cnt in cnts:
            area = cv2.contourArea(cnt)
            if area > threshold_area:
                cv2.drawContours(frame, cnts, -1, color, 2)
                rect = cv2.boundingRect(cnt)
                boundingboxArea: rect.width * rect.height
                cv2.contourArea(cnt)
                assert isinstance(rect, object)
                x, y, w2, h2 = rect
                M = cv2.moments(cnt)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                print(area // boundingboxArea)
                if (smallRatio > area // boundingboxArea > bigRatio):
                    cv2.rectangle(frame, (x, y), (x + w2, y + h2), color, 2)
                    cv2.putText(frame, 'Hexagon Detected', (x + w2 + 10, y + h2), 0, 0.3, color)
                    cv2.circle(frame, (cX, cY), 2, color, 4)
                    print("Angle: " + str(get_angle((w1, h1), (w1, h), (cX, cY))))
                    print("Distance: ", distance_calc(w2))
                    print("HexDistance: ", distance_from_center_to_hexagon(cX, cY, w1, h1))
                    if len(last_cnts) == 1:
                        last_cnts.pop()
                    else:
                        pass
                    last_cnts.extend(cnts)
                    f = 0
    else:
        if f < 500:
            for i in last_cnts:
                usePreviousLocation = True
                area = cv2.contourArea(i)
                if area > threshold_area:
                    cv2.drawContours(frame, last_cnts, -1, color, 2)
                    rect1 = cv2.boundingRect(i)
                    boundingboxArea: rect1.width * rect1.height
                    cv2.contourArea(i)
                    assert isinstance(rect1, object)
                    x1, y1, w3, h3 = rect1
                    M = cv2.moments(i)
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    if (smallRatio > area // boundingboxArea > bigRatio):
                        cv2.rectangle(frame, (x1, y1), (x1 + w3, y1 + h3), color, 2)
                        cv2.putText(frame, 'Hexagon Detected', (x1 + w3 + 10, y1 + h3), 0, 0.3, color)
                        cv2.circle(frame, (cX, cY), 2, color, 4)
                        print("Angle: " + str(get_angle((w1, h1), (w1, h), (cX, cY))))
                        print("Distance: ", distance_calc(w3))
                        print("HexDistance: ", distance_from_center_to_hexagon(cX, cY, w1, h1))

            f += 1
        else:
            pass


while True:
    _, yframe = cap.read()
    frame = cv2.cvtColor(yframe, cv2.COLOR_BGR2HSV)
    frame = cv2.resize(frame, (640, 480))
    low_green = np.array([49, 87, 103])
    high_green = np.array([85, 244, 255])
    green_mask = cv2.inRange(frame, low_green, high_green)
    green = cv2.bitwise_and(frame, frame, _, mask=green_mask)
    thresh = cv2.threshold(green, 140, 180, cv2.THRESH_BINARY)[1]
    gray = cv2.cvtColor(thresh, cv2.COLOR_BGR2GRAY)
    cnts = cv2.findContours(gray.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    threshold_area = 10
    (h, w) = frame.shape[:2]
    w1 = w // 2
    h1 = h // 2
    cv2.circle(frame, (w1, h1), 2, color, 4)
    cv2.circle(frame, (w1, h), 2, color, 4)
    detection()
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)
    if key == 27:
        break
