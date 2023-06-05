import cv2
import numpy as np
from pyzbar.pyzbar import decode
from pyaadhaar.utils import isSecureQr
from pyaadhaar.decode import AadhaarSecureQr
import xmltodict
import json
import sys
from datetime import datetime
import urllib.request
from PIL import Image
import os
import pytesseract

cwd = os.getcwd()
relative_path = "tesseract_OCR"
filename = "tesseract.exe"
full_path = os.path.join(cwd, relative_path, filename)
pytesseract.pytesseract.tesseract_cmd = full_path
pan_card_image_path =r"http://localhost:8000/profile/aadhaar.jpg"

# print(full_path)
aadhar_card_image_path = r"C:\Users\Lenovo\Downloads\imgonline-com-ua-resize-j3RtF5VEyM.jpg"

# link = sys.argv[1]

now = datetime.now() 
time_str = now.strftime("%Y%m%d_%H%M%S")  

urllib.request.urlretrieve(
    pan_card_image_path,
    time_str)

img_pancard = cv2.imread(time_str)
np.save('image.npy', img_pancard)
img = np.load(r'image.npy')
image_arr = img[100:334, 0:700]
image = Image.fromarray(image_arr)
pan_card_text = pytesseract.image_to_string(img_pancard, lang='eng', config='--psm 6')

print(pan_card_text)
  
# # # image = Image.open("gfg.jpg")
# # # img.show()

# # Load imgae, grayscale, Gaussian blur, Otsu's threshold
# # image = cv2.imread(r"C:\Users\ASUS\Pictures\aadhar_2.jpg")

# image = cv2.imread(time_str)
# original = image.copy()
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# blur = cv2.GaussianBlur(gray, (7,7), 0)
# thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# # Morph close
# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
# close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)

# # Find contours and filter for QR code using contour area, approximation, and aspect ratio
# cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# cnts = cnts[0] if len(cnts) == 2 else cnts[1]
# for c in cnts:
#     peri = cv2.arcLength(c, True)
#     approx = cv2.approxPolyDP(c, 0.04 * peri, True)
#     x,y,w,h = cv2.boundingRect(approx)
#     area = cv2.contourArea(c)
#     ar = w / float(h)
#     if len(approx) == 4 and area > 1000 and (ar > .85 and ar < 1.3):
#         cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 3)
#         ROI = original[y:y+h, x:x+w]
#         # cv2.imwrite('ROI.png', ROI)

# # Display
# # cv2.imshow('thresh', thresh)
# # cv2.imshow('close', close)
# # cv2.imshow('image', image)
# # cv2.imshow('ROI', ROI)


# img2 = cv2.resize(ROI, (ROI.shape[1]*2, ROI.shape[0]*2), interpolation=cv2.INTER_LANCZOS4)  # Resize by x2 using LANCZOS4 interpolation method.

# cv2.imwrite('image2.png', img2)
# gray_QR = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
# #qrData = Qr_img_to_text(image_file_name
# # cv2.imshow('image2', img2)

# code = decode(gray_QR)

# qrData = code[0].data
# # json_data = json.dumps(xmltodict.parse(qrData), indent=4)
# # print(json_data)
# isSecureQR = (isSecureQr(qrData))

# if isSecureQR:
#     secure_qr = AadhaarSecureQr(int(qrData))
#     decoded_secure_qr_data = secure_qr.decodeddata()
#     # print(decoded_secure_qr_data)
#     # json_data = json.dumps(xmltodict.parse(decoded_secure_qr_data), indent=4)
#     # json_object = json.dumps(decoded_secure_qr_data, indent=4)

#     dataCompare = {
#     "name" : decoded_secure_qr_data['name'],
#     "pincode" : decoded_secure_qr_data['pincode'],
#     "aadhaar_no" : decoded_secure_qr_data['adhaar_last_4_digit'],
#     "dob" : decoded_secure_qr_data['dob'],
#     }

#     person = json.dumps(dataCompare)
#     print(person)
    
# filepath = os.path.join(os.getcwd(), time_str)
# os.remove(filepath)
# filepath = os.path.join(os.getcwd(), 'image2.png')
# os.remove(filepath)
#     # print(decoded_secure_qr_data['name'])