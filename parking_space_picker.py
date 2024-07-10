import cv2
import pickle
import os
from math import sqrt

width, height = 40, 23
pt1_x, pt1_y, pt2_x, pt2_y = None, None, None, None
line_count = 0

try:
    with open('park_positions', 'rb') as f:
        park_positions = pickle.load(f)
except:
    park_positions = []

def parking_line_counter():
    global line_count
    line_count = int((sqrt((pt2_x - pt1_x) ** 2 + (pt2_y - pt1_y) ** 2)) / height)
    return line_count

def mouse_events(event, x, y, flags, param):
    global pt1_x, pt1_y, pt2_x, pt2_y, park_positions

    if event == cv2.EVENT_LBUTTONDOWN:
        pt1_x, pt1_y = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        pt2_x, pt2_y = x, y
        parking_spaces = parking_line_counter()
        if parking_spaces == 0:
            park_positions.append((x, y))
        else:
            for i in range(parking_spaces):
                park_positions.append((pt1_x, pt1_y + i * height))

    elif event == cv2.EVENT_RBUTTONDOWN:
        # Check if right-click is within any parking space
        removed = False
        for i, position in enumerate(park_positions):
            x1, y1 = position
            if x1 < x < x1 + width and y1 < y < y1 + height:
                park_positions.pop(i)
                removed = True
                break
        
        # If no parking space removed, clear all with 'C' key
        if not removed:
            pass  # Do nothing on right-click

    with open('park_positions', 'wb') as f:
        pickle.dump(park_positions, f)

# Ensure correct file path to the image
img_path = 'input/parking.png'
full_img_path = os.path.abspath(img_path)
print(f"Loading image from path: {full_img_path}")

if not os.path.exists(full_img_path):
    print(f"Error: File does not exist at path: {full_img_path}")
    exit(1)

img = cv2.imread(full_img_path)

if img is None:
    print(f"Error: Could not load image at path: {full_img_path}")
    exit(1)

while True:
    img_copy = img.copy()

    for position in park_positions:
        cv2.rectangle(img_copy, position, (position[0] + width, position[1] + height), (255, 0, 255), 3)

    cv2.namedWindow('image', cv2.WINDOW_NORMAL)
    cv2.setWindowProperty('image', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    cv2.imshow('image', img_copy)
    cv2.setMouseCallback('image', mouse_events)

    key = cv2.waitKey(30)
    if key == ord('c'):  # Press 'C' key to clear all parking spots
        park_positions = []  # Clear all parking positions
        with open('park_positions', 'wb') as f:
            pickle.dump(park_positions, f)
        print("All parking spots cleared.")

    elif key == 27:  # Esc key to exit
        break

cv2.destroyAllWindows()
