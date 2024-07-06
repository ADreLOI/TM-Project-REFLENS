import math
import sys
import os
import importlib

#sys.path.append(os.path.join(os.path.abspath(__file__), '..', 'Dynamics'))

max_x = 1.0
max_y = 0.0
min_x = 0.0
min_y = 1.0
distance = 0.0


def detect_fouls(handsLandmarks, bodyLandamrks, cv2, frame):
    # Landmarks of each hand's point
    palm = handsLandmarks.landmark[0]
    thumb_b = handsLandmarks.landmark[1]
    thumb_p = handsLandmarks.landmark[2]
    thumb_ip = handsLandmarks.landmark[3]
    thumb_tip = handsLandmarks.landmark[4]
    index_b = handsLandmarks.landmark[5]
    index_p = handsLandmarks.landmark[6]
    index_ip = handsLandmarks.landmark[7]
    index_tip = handsLandmarks.landmark[8]
    middle_b = handsLandmarks.landmark[9]
    middle_p = handsLandmarks.landmark[10]
    middle_ip = handsLandmarks.landmark[11]
    middle_tip = handsLandmarks.landmark[12]
    ring_b = handsLandmarks.landmark[13]
    ring_p = handsLandmarks.landmark[14]
    ring_ip = handsLandmarks.landmark[15]
    ring_tip = handsLandmarks.landmark[16]
    pinky_b = handsLandmarks.landmark[17]
    pinky_p = handsLandmarks.landmark[18]
    pinky_ip = handsLandmarks.landmark[19]
    pinky_tip = handsLandmarks.landmark[20]

    global max_x, max_y, min_x, min_y, distance
    #print("MAX E MIN Y" + str(max_y) + " " + str(min_y))
    #print("LANDMARKS Y" + str(handsLandmarks.landmark[0].y) + " " + str(handsLandmarks.landmark[12].y))

    # Regolare la chiamata in base alla distanza Confrontate frame per frame che la differenza tra le coordinate y
    # delle dita dal polso sia uguale alla distanza polso dita!
    change = False
    # Normalized Y
    # Check to determines the max and min y and x
    if handsLandmarks.landmark[0].y > max_y and handsLandmarks.landmark[12].y < min_y:
        if handsLandmarks.landmark[0].y < 1.0 and handsLandmarks.landmark[12].y > 0.0:
            #print("CHANGE")
            change = True
            max_y = handsLandmarks.landmark[0].y
            min_y = handsLandmarks.landmark[12].y
    nMiddleY = normalizeYCoordinates(max_y, min_y, middle_tip.y)
    nWristY = normalizeYCoordinates(max_y, min_y, thumb_tip.y)

    # Normalized X
    if handsLandmarks.landmark[20].x > max_x and handsLandmarks.landmark[4].x < min_x:
        max_x = handsLandmarks.landmark[20].x
        min_x = handsLandmarks.landmark[4].x
    nMiddleX = normalizeXCoordinates(max_x, min_x, middle_tip.x)
    nWristX = normalizeXCoordinates(max_x, min_x, thumb_tip.x)

    if change:
        distance = math.sqrt((nWristX - nMiddleX) ** 2 + (nWristY - nMiddleY) ** 2)

    diff_y = nWristY - nMiddleY
    #print("Difference between middle finger and wrist:" + str(diff_y))
    #print("Distance between middle finger and wrist:" + str(distance))

    if diff_y >= distance:
        cv2.putText(
            img=frame,
            text="Middle AND Wrist TOGETHER",
            org=(200, 200),
            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
            fontScale=1,
            color=(125, 246, 55),
            thickness=3
        )

    """
    cv2.waitKey(500) --> Pause the frame for 500 ms
    if distance < 0.10:
        cv2.putText(
            img=frame,
            text="THUMB AND MIDDLE TOGETHER",
            org=(200, 200),
            fontFace=cv2.FONT_HERSHEY_DUPLEX,
            fontScale=3.0,
            color=(125, 246, 55),
            thickness=3
        )
    """


def normalizeXCoordinates(max_x, min_x, x_to_normalize):
    normalizedX = (x_to_normalize - min_x) / (max_x - min_x)
    return normalizedX


def normalizeYCoordinates(max_y, min_y, y_to_normalize):
    normalizedY = (y_to_normalize - min_y) / (max_y - min_y)
    return normalizedY
