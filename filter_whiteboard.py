import cv2
import numpy as np

def filter_white_background(input_path, output_path):
    img = cv2.imread(input_path)
    if img is None:
        raise ValueError("Image not found or invalid format")

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define white range
    lower_white = np.array([0, 0, 200])
    upper_white = np.array([180, 30, 255])

    # Create mask to remove background
    mask = cv2.inRange(hsv, lower_white, upper_white)
    mask_inv = cv2.bitwise_not(mask)
    result = cv2.bitwise_and(img, img, mask=mask_inv)

    # Save filtered image
    cv2.imwrite(output_path, result)
