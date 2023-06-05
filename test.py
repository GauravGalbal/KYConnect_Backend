import pytesseract
import numpy as np
from PIL import Image
import re
import json
import os
import urllib.request
import sys
import psutil
import cv2

from pyzbar.pyzbar import decode
from pyaadhaar.utils import isSecureQr
from pyaadhaar.decode import AadhaarSecureQr
from deepface import DeepFace
from datetime import datetime

# Defining tesserct Path
cwd = os.getcwd()
relative_path = "tesseract_OCR"
filename = "tesseract.exe"
full_path = os.path.join(cwd, relative_path, filename)
pytesseract.pytesseract.tesseract_cmd = full_path  

# Save the Pan Card Path URL
# pan_card_image_path = "http://localhost:8000/profile/pan.jpg"
pan_card_image = sys.argv[1]


# Save the Aadhaar Card QR Path URL
# aadhaar_card_QR_path = "http://localhost:8000/profile/aadhaar_back.jpg"
aadhaar_card_QR = sys.argv[2]



def aadhaar_verification_extraction():

    now = datetime.now() 
    aadhaar_QR_path = now.strftime("%Y%m%d_%H%M%S")
    urllib.request.urlretrieve(
    aadhaar_card_QR,
    aadhaar_QR_path)

    image = cv2.imread(aadhaar_QR_path)

    original = image.copy()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7,7), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    # Morph close
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
    close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)

    # Find contours and filter for QR code using contour area, approximation, and aspect ratio
    cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        x,y,w,h = cv2.boundingRect(approx)
        area = cv2.contourArea(c)
        ar = w / float(h)
        if len(approx) == 4 and area > 1000 and (ar > .85 and ar < 1.3):
            cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 3)
            ROI = original[y:y+h, x:x+w]


    # Display
    # cv2.imshow('thresh', thresh)
    # cv2.imshow('close', close)
    # cv2.imshow('image', image)
    # cv2.imshow('ROI', ROI)


    img2 = cv2.resize(ROI, (ROI.shape[1]*2, ROI.shape[0]*2), interpolation=cv2.INTER_LANCZOS4)  # Resize by x2 using LANCZOS4 interpolation method.

    cv2.imwrite('image2.png', img2)
    gray_QR = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    #qrData = Qr_img_to_text(image_file_name
    # cv2.imshow('image2', img2)

    code = decode(gray_QR)
    # print(code)
    try:
        qrData = code[0].data
        isSecureQR = (isSecureQr(qrData))

        if isSecureQR:
            secure_qr = AadhaarSecureQr(int(qrData))
            decoded_secure_qr_data = secure_qr.decodeddata()
            # print(decoded_secure_qr_data)

            # json_object = json.dumps(decoded_secure_qr_data, indent=4)
            # # print(json_object)
            # return json_object
            dataCompare = {
                "name": decoded_secure_qr_data['name'],
                "pincode": decoded_secure_qr_data['pincode'],
                "aadhaar_no": decoded_secure_qr_data['adhaar_last_4_digit'],
                "dob": decoded_secure_qr_data['dob'],
                # "gender": decoded_secure_qr_data['gender'],
                # "district": decoded_secure_qr_data['district'],
                # "landmark": decoded_secure_qr_data['landmark'],
                # "location": decoded_secure_qr_data['location'],
                # "street": decoded_secure_qr_data['street'],
                # "state": decoded_secure_qr_data['state'],
                # "email_linked_with_aadhaar": decoded_secure_qr_data['email'],
                # "mobilenumber_linked_with_aadhaar": decoded_secure_qr_data['mobile'],
            }

            information = json.dumps(dataCompare)
            return information

            # print(200)

    except IndexError:
        aadhaar_error = "False"
        dataCompare = {"name": aadhaar_error}
        information = json.dumps({"name": aadhaar_error})
        return information

def pancard_extraction():

    now = datetime.now() 
    pan_path = now.strftime("%Y%m%d_%H%M%S")
    urllib.request.urlretrieve(
    pan_card_image,
    pan_path)

    img_pancard = cv2.imread(pan_path)
    np.save('image.npy', img_pancard)
    img = np.load(r'image.npy')
    image_arr = img[100:334, 0:700]
    image = Image.fromarray(image_arr)
    pan_card_text = pytesseract.image_to_string(img_pancard, lang='eng', config='--psm 6')


    output_text = pan_card_text.replace('\n', ' ')
    pattern = "[A-Z]{5}[0-9]{4}[A-Z]{1}"

    matches = re.findall(pattern, output_text)


    if not matches:
        error = 'False'
        return error
    else:

        return matches
    



final_info = aadhaar_verification_extraction()
pan_number = pancard_extraction()

append_pan = {"pan_number": pan_number}
data = json.loads(final_info)
data.update(append_pan)
final_info = json.dumps(append_pan, indent=4)
print(final_info)
