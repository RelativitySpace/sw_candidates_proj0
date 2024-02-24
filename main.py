import cv2
import numpy as np
import csv

def measure_weld_width(image):
    # Assuming the weld bead is a bright object on a dark background
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
            cv2.THRESH_BINARY,11,2)

    # Find contours in the binary image
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Assuming there is only one weld bead in the frame
    if contours:
        # Get the bounding rectangle of the weld bead
        x, y, w, h = cv2.boundingRect(contours[0])

        # Draw a rectangle around the weld bead
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return w

    return None

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

process_video(video_file, output_csv_file)

