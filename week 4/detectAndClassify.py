#Takes an image, detects traffic lights, classifies them, and then outputs image with bounding boxes
import cv2
import numpy as np
from ultralytics import YOLO
import os.path as path

input_image = "Path/to/input/image"
ouput_image = "Path/to/output/image"

model = YOLO("yolo11n.pt")
img = cv2.imread(input_image)
result = model.predict(img)
data = result[0].boxes.data.cpu().numpy() #tensor in [x1, y1, x2, y2, confidence, class] format
classes = result[0].names
font = cv2.FONT_HERSHEY_SIMPLEX

lower_red1 = np.array([0,30,100])
upper_red1 = np.array([18,255,255])
lower_red2 = np.array([170,30,200])
upper_red2 = np.array([180,255,255])
lower_green = np.array([50,60,150])
upper_green = np.array([100,255,255])
lower_yellow = np.array([20,115,150])
upper_yellow = np.array([35,255,255])

def find_largest_contour(mask):
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        return max(contours, key=cv2.contourArea)
    else:
        return []

for row in data:
    if classes[row[5]] == "traffic light":
        tf_img = cv2.cvtColor(img[int(row[1]):int(row[3]), int(row[0]):int(row[2])], cv2.COLOR_BGR2HSV)
        contour_red = len(find_largest_contour(cv2.bitwise_or(cv2.inRange(tf_img, lower_red1, upper_red1), cv2.inRange(tf_img, lower_red2, upper_red2))))
        contour_yellow = len(find_largest_contour(cv2.inRange(tf_img, lower_yellow, upper_yellow)))
        contour_green = len(find_largest_contour(cv2.inRange(tf_img, lower_green, upper_green)))
        light_value = max([contour_red, contour_yellow, contour_green])

        if light_value == contour_red:
            light = "red"
        elif light_value == contour_yellow:
            light = "yellow"
        elif light_value == contour_green:
            light = "green"
        img = cv2.rectangle(img, (int(row[0]), int(row[1])), (int(row[2]), int(row[3])), (0, 255, 0), 3)
        img = cv2.putText(img, light, (int(row[0]), int(row[1])), font, 1, (0,0,0), 3)

cv2.imwrite(ouput_image, img)