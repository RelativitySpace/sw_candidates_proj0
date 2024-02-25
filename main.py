import cv2
import numpy as np
import csv
from matplotlib import pyplot as plt

image = r"C:\Users\Giovanni\Desktop\Desktop\Relativity Space\sw_candidates_proj0\images\weld.png"

def image_preparation(img_path):
    # Read the input image
    img = cv2.imread(img_path, 0)
    
    # Apply median blur to reduce noise
    img = cv2.medianBlur(img, 5)

    # Find the brightest point in the image
    _, max_val, _, max_loc = cv2.minMaxLoc(img)

    # Set everything on the left side of the brightest point to 0
    img[:, :max_loc[0]] = 0

    # Apply adaptive thresholding
    th2 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    th3 = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # Perform Hough Line Transform
    lines = cv2.HoughLines(th3, 1, np.pi / 180, threshold=100)

    # Create a blank image to draw lines on
    line_img = np.zeros_like(img)

    # Draw lines on the blank image
    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(line_img, (x1, y1), (x2, y2), 255, 2)


    # Display the images
    titles = ['Original Image', 'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
    images = [img, th2, th3]

    # for i in range(3):
    #     plt.subplot(1, 3, i + 1), plt.imshow(images[i], 'gray')
    #     plt.title(titles[i])
    #     plt.xticks([]), plt.yticks([])

    # plt.show()

    plt.imshow(line_img, 'gray')
    plt.title("lines")
    plt.show()


def measure_weld_width(img):
    return 0

def process_video(video_path, output_csv):
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Open output CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Time', 'Weld Width'])

        # Process each frame
        while True:
            ret, frame = cap.read()

            if not ret:
                break

            # Measure weld width using contour detection
            weld_width = measure_weld_width(frame)

            # Write time and weld width to CSV
            time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
            csv_writer.writerow([time, weld_width])

            # Display the frame with the bead highlighted
            cv2.imshow('Frame', frame)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(50) & 0xFF == ord('q'):
                break

        # Release video capture and close CSV file
        cap.release()
        csvfile.close()

    cv2.destroyAllWindows()

# Example usage
video_file = r"C:\Users\Giovanni\Desktop\Desktop\Relativity Space\sw_candidates_proj0\videos\weld.mp4"
output_csv_file = "weld_width_measurements.csv"

#process_video(video_file, output_csv_file)

image_preparation(image)
#measure_weld_width(image)
