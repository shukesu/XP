import sys
import cv2

cap = cv2.VideoCapture(0)
while(1):
    ret, frame = cap.read()
    cv2.imshow("Capture", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

