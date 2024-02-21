import numpy as np
import cv2
from matplotlib import pyplot as plt

img_path = r"C:\Users\Giovanni\Desktop\Desktop\Relativity Space\sw_candidates_proj0\images\weld.png"

def find_brightest_area(image_path):
    # Read the image in grayscale
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Find the column index with the maximum sum (brightest area)
    column_sums = np.sum(img, axis=0)
    brightest_column = np.argmax(column_sums)

    # Crop the image to keep everything to the right of the brightest area
    img_cropped = img[:, brightest_column:]

    return img_cropped

def extract_width():

    img = find_brightest_area(img_path)
    edges = cv2.Canny(img, 15, 30)

    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, maxLineGap=1000)

    # Filter lines based on y-coordinate range
    y_range = (150, 275)
    filtered_lines = [line[0] for line in lines if y_range[0] <= line[0][1] <= y_range[1]]

    # Define slope threshold for considering a line as straight
    slope_threshold = 0.001  # You may adjust this value based on your requirements

    # Create a blank image to draw the connected straight lines
    img_connected = np.zeros_like(img)

    for line in filtered_lines:
        x1, y1, x2, y2 = line

        # Calculate the slope of the line
        slope = (y2 - y1) / (x2 - x1 + 1e-6)  # Adding a small value to avoid division by zero

        # Check if the slope is within the specified threshold
        if abs(slope) < slope_threshold:
            cv2.line(img_connected, (x1, y1), (x2, y2), (255, 0, 0), 1)

    plt.imshow(img_connected, cmap='gray')
    plt.show()


extract_width()

