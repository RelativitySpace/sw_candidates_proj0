import numpy as np
import cv2

im_path = r"C:\Users\Giovanni\Desktop\Desktop\Relativity Space\sw_candidates_proj0\images\weld_width.png"

def extract_width(im_path):
    # Get image in grayscale
    im = cv2.imread(im_path, 0)

    # Display the original image
    cv2.imshow('Original Image', im)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()

extract_width(im_path)