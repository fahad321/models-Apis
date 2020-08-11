import cv2
import pytesseract
import imutils
import numpy as np
import os

# pytesseract.pytesseract.tesseract_cmd = "C:\Program Files\Tesseract-OCR\\tesseract.exe"

root_dir_path = os.path.dirname(os.path.abspath("app.py"))
saving_path = root_dir_path + "/models/contianerNumbet/croppedImage/"

# currently not working because ROI selector is disabled
def container_number(image):

    # RGB to Gray scale conversion
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Noise removal with iterative bilateral filter(removes noise while preserving edges)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    # ROI Selector
    # r = cv2.selectROI(gray)
    width_start, height_start, width_end, height_end = r
    cropped_img = gray[
        height_start : height_start + height_end, width_start : width_start + width_end
    ]
    cv2.imwrite(saving_path + "CroppedImage.jpg", cropped_img)  # Saving Cropped Image

    # Image Inverted
    imagem = cv2.bitwise_not(cropped_img)

    # Bilateral Filtering
    gray_new = cv2.bilateralFilter(imagem, 11, 17, 17)
    st = pytesseract.image_to_string(gray_new)
    print(" Container Number = ", st)  # Try 1 (BEST RESULT IN MOST CASES)

    return {"number": st}

