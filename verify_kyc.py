from PIL import Image
import numpy as np
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
pan_path = ''


# Save the Aadhaar Card QR Path URL
# aadhaar_card_QR_path = "http://localhost:8000/profile/aadhaar_back.jpg"
aadhaar_card_QR = sys.argv[2]
aadhaar_QR_path = ''


# # Save the Aadhaar Card Photo Path URL
# aadhaar_card_image = "http://localhost:8000/profile/aadhaar_front.jpg"
aadhaar_card_image = sys.argv[3]


# # Save the Selfie Path URL
# selfie_image_path = "http://localhost:8000/profile/selfie.jpg"
selfie_image = sys.argv[4]
selfie_path = ''



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

    # json_data = json.dumps(xmltodict.parse(qrData), indent=4)
    # print(json_data)

def face_verification():

    now = datetime.now() 
    aadhaar_image_path = now.strftime("%Y%m%d_%H%M%S")
    urllib.request.urlretrieve(
    aadhaar_card_image,
    aadhaar_image_path)

    img = cv2.imread(aadhaar_image_path)

    # Convert into grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Load the cascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    # Draw rectangle around the faces and crop the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        faces = img[y:y + h, x:x + w]
        # cv2.imshow("faces", faces)
        cv2.imwrite('face.jpg', faces)

    # Display the output
    cv2.imwrite('detcted.jpg', img)
    # cv2.imshow("img", img)
    cv2.waitKey()
    faces = cv2.resize(faces, (350, 350), interpolation=cv2.INTER_LINEAR)

    # cv2.imshow("faces", faces)
    # cv2.waitKey(10000)

    # img1 = cv2.imread(r'C:\Users\Lenovo\Downloads\imgonline-com-ua-resize-qJ8lJHADWluU.jpg')
    now = datetime.now() 
    selfie_path = now.strftime("%Y%m%d_%H%M%S")
    urllib.request.urlretrieve(
    selfie_image,
    selfie_path)

    img2 = cv2.imread(selfie_path)

    # print("brightness")
    # print(brightness)

    img2 = cv2.resize(img2, (350, 350), interpolation=cv2.INTER_LINEAR)
    # cv2.imshow("img2", img2)

    try:

        result = DeepFace.verify(faces, img2)

        if result["verified"]:
            # print(
                # "Congratulations! Face verification is successful. You are now authenticated to proceed with your KYC process.")
            face_success = "Successful"
            return face_success

        else:
            # print("Sorry!!, Face verification unsuccessful, Try again with a clear and well-lit photo.")
            face_fail = "False"
            return face_fail

    except ValueError:

        # print("Face could not be detected. Please ensure that the picture is a face photo!!")
        
        face_detect = "False"
        return face_detect

final_info = aadhaar_verification_extraction()
pan_number = pancard_extraction()

append_pan = {"pan_number": pan_number[0]}
data = json.loads(final_info)
data.update(append_pan)
final_info = json.dumps(data, indent=4)

face_verfication_result = face_verification()
face_verfication = {"face_verfication_result": face_verfication_result}
final_data = json.loads(final_info)
final_data.update(face_verfication)
final_info = json.dumps(final_data, indent=4)

ram = {"RAM Used (GB)": psutil.virtual_memory()[3]/1000000000}
ram_data = json.loads(final_info)
ram_data.update(ram)
final_info = json.dumps(ram_data, indent=4)

# filepath = os.path.join(os.getcwd(), aadhaar_QR_path)
# os.remove(filepath)
# filepath = os.path.join(os.getcwd(), pan_path)
# os.remove(filepath)
# filepath = os.path.join(os.getcwd(), selfie_path)
# os.remove(filepath)
filepath = os.path.join(os.getcwd(), 'image.npy')
os.remove(filepath)
filepath = os.path.join(os.getcwd(), 'image2.png')
os.remove(filepath)
filepath = os.path.join(os.getcwd(), 'detcted.jpg')
os.remove(filepath)
filepath = os.path.join(os.getcwd(), 'face.jpg')
os.remove(filepath)

print(final_info)




















# import pytesseract
# from PIL import Image
# import numpy as np
# import re
# import json
# import os
# import urllib.request
# import sys
# import psutil
# import cv2
# from deepface import DeepFace
# from datetime import datetime

# # Defining tesserct Path
# cwd = os.getcwd()
# relative_path = "tesseract-OCR"
# filename = "tesseract.exe"
# full_path = os.path.join(cwd, relative_path, filename)
# pytesseract.pytesseract.tesseract_cmd = full_path  

# # Save the Pan Card Path URL
# # pan_card_image_path = "http://localhost:8000/profile/pan.jpg"
# # pan_card_image = sys.argv[1]
# # pan_card_image=r'pan.jpg'
# pan_path = ''


# # Save the Aadhaar Card QR Path URL
# # aadhaar_card_QR = "http://localhost:8000/profile/face.jpg"
# aadhaar_card_QR = sys.argv[3]
# # aadhaar_card_Qr=r'aadhaar_back.jpg'
# aadhaar_QR_path = ''


# # # Save the Aadhaar Card Photo Path URL
# # aadhaar_card_image = "http://localhost:8000/profile/aadhaar_front.jpg"
# # aadhaar_card_image = sys.argv[3]
# # aadhaar_card_image=r'face.jpg'

# # # Save the Selfie Path URL
# # selfie_image_path = "http://localhost:8000/profile/selfie.jpg"
# # selfie_image = sys.argv[4]
# # selfie_image =r"selfie.jpg"

# selfie_path = ''


# def pancard_extraction():

#     now = datetime.now() 
#     pan_path = now.strftime("%Y%m%d_%H%M%S")
#     urllib.request.urlretrieve(
#     pan_card_image,
#     pan_path)

#     img_pancard = cv2.imread(pan_path)
#     np.save('image.npy', img_pancard)
#     img = np.load(r'image.npy')
#     image_arr = img[100:334, 0:700]
#     image = Image.fromarray(image_arr)
#     pan_card_text = pytesseract.image_to_string(img_pancard, lang='eng', config='--psm 6')


#     output_text = pan_card_text.replace('\n', ' ')
#     pattern = "[A-Z]{5}[0-9]{4}[A-Z]{1}"

#     matches = re.findall(pattern, output_text)


#     if not matches:
#         error = 'False'
#         return error
#     else:

#         return matches
    
# def face_verification():

#     now = datetime.now() 
#     aadhaar_image_path = now.strftime("%Y%m%d_%H%M%S")
#     urllib.request.urlretrieve(
#     aadhaar_card_image,
#     aadhaar_image_path)

#     img = cv2.imread(aadhaar_image_path)

#     # Convert into grayscale
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     # Load the cascade
#     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')

#     # Detect faces
#     faces = face_cascade.detectMultiScale(gray, 1.1, 4)

#     # Draw rectangle around the faces and crop the faces
#     for (x, y, w, h) in faces:
#         cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
#         faces = img[y:y + h, x:x + w]
#         # cv2.imshow("faces", faces)
#         cv2.imwrite('face.jpg', faces)

#     # Display the output
#     cv2.imwrite('detcted.jpg', img)
#     # cv2.imshow("img", img)
#     cv2.waitKey()
#     faces = cv2.resize(faces, (350, 350), interpolation=cv2.INTER_LINEAR)

#     # cv2.imshow("faces", faces)
#     # cv2.waitKey(10000)

#     # img1 = cv2.imread(r'C:\Users\Lenovo\Downloads\imgonline-com-ua-resize-qJ8lJHADWluU.jpg')
#     now = datetime.now() 
#     selfie_path = now.strftime("%Y%m%d_%H%M%S")
#     # urllib.request.urlretrieve(
#     # selfie_image,
#     # selfie_path)

#     img2 = cv2.imread("aadhaar_front.jpg")

#     # print("brightness")
#     # print(brightness)

#     img2 = cv2.resize(img2, (350, 350), interpolation=cv2.INTER_LINEAR)
#     # cv2.imshow("img2", img2)

#     try:

#         result = DeepFace.verify(faces, img2)

#         if result["verified"]:
#             # print(
#                 # "Congratulations! Face verification is successful. You are now authenticated to proceed with your KYC process.")
#             face_success = "Successful"
#             return face_success

#         else:
#             # print("Sorry!!, Face verification unsuccessful, Try again with a clear and well-lit photo.")
#             face_fail = "False"
#             return face_fail

#     except ValueError:

#         # print("Face could not be detected. Please ensure that the picture is a face photo!!")
        
#         face_detect = "False"
#         return face_detect

# def aadhaar_verification_extraction():

#     now = datetime.now() 
#     aadhaar_QR_path = now.strftime("%Y%m%d_%H%M%S")
#     urllib.request.urlretrieve(
#     aadhaar_card_QR,
#     aadhaar_QR_path)

#     img_aadcard = cv2.imread(aadhaar_QR_path)
#     aadhaar_card_text = pytesseract.image_to_string(img_aadcard, lang='eng', config='--psm 6')
#     output_text = aadhaar_card_text.replace('\n', ' ')

#     aadhaar_pattern = r"\d{4}\s?\d{4}\s?\d{4}"
#     aadhaar_numbers = re.findall(aadhaar_pattern, output_text)

#     dob = r"\b(\d{1,2})/(\d{1,2})/(\d{4})\b"
#     match = re.search(dob, output_text)
#     if match:
#         day = match.group(1)
#         month = match.group(2)
#         year = match.group(3)
#         birthdate = f"{day}/{month}/{year}"
#         # print(birthdate)
#     else:
#         print("No date of birth found in the text.")
#     # print(aadhaar_numbers)

#     gender_pattern = re.compile(r"\b(?:MALE|FEMALE|OTHERS)\b", re.IGNORECASE)
#     genders = gender_pattern.findall(output_text)

#     # print(genders)

#     name_pattern = re.compile(r"([A-Z][a-z]+)\s*(?:([A-Z][a-z]+)\s*)?([A-Z][a-z]+)")
#     match = name_pattern.search(output_text)

#     if match:
#         name = match.group(1)
#         father_name = match.group(2)
#         surname = match.group(3)
#         # print(f"Name: {name}\nFather's name: {father_name}\nSurname: {surname}")
#     else:
#         print("No name found in the text.")

#     now = datetime.now() 
#     aadhaar_card_back_path = now.strftime("%Y%m%d_%H%M%S")
#     urllib.request.urlretrieve(
#     # aadhaar_card_image,
#     aadhaar_card_QR,
#     aadhaar_card_back_path)
#     # aadhaar_card_back_path = r"aadhaar_back.jpg"
#     img_backcard = cv2.imread(aadhaar_card_back_path)

#     aadhaar_back_text = pytesseract.image_to_string(img_backcard, lang='eng', config='--psm 6')

#     back_output = aadhaar_back_text.replace('\n', ' ')

#     pincode_pattern = re.compile(r"\b(\d{6})\b")
#     pcode = pincode_pattern.search(back_output)

#     # if pcode:
#     #     pincode = pcode.group(1)
#     #     # print(f"Pincode: {pincode}")
#     # else:
#     #     print("No pincode found in the text.")

#     aadhaar_info_dict = {
#         "DOB": birthdate,
#         "Aadhaar_number": aadhaar_numbers[0],
#         "Gender": genders[0],
#         "Name": name,
#         "Father's Name": father_name,
#         "Surname": surname,
#         # "Pincode": pincode
#     }

#     json_object = json.dumps(aadhaar_info_dict, indent=4)
#     return json_object


#      #image = cv2.imread(r'C:\Users\Lenovo\Desktop\testing photos\test1.png')
#     #
#     #
#     #
#     # original = image.copy()
#     #
#     # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     # blur = cv2.GaussianBlur(gray, (7,7), 0)
#     # thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
#     #
#     # # Morph close
#     # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
#     # close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)
#     #
#     # # Find contours and filter for QR code using contour area, approximation, and aspect ratio
#     # cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     # cnts = cnts[0] if len(cnts) == 2 else cnts[1]
#     # for c in cnts:
#     #     peri = cv2.arcLength(c, True)
#     #     approx = cv2.approxPolyDP(c, 0.04 * peri, True)
#     #     x,y,w,h = cv2.boundingRect(approx)
#     #     area = cv2.contourArea(c)
#     #     ar = w / float(h)
#     #     if len(approx) == 4 and area > 1000 and (ar > .85 and ar < 1.3):
#     #         cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 3)
#     #         ROI = original[y:y+h, x:x+w]
#     #
#     # original = image.copy()
#     #
#     # try:
#     #
#     #
#     #
#     #     # Display
#     #     cv2.imshow('thresh', thresh)
#     #     cv2.imshow('close', close)
#     #     cv2.imshow('image', image)
#     #     cv2.imshow('ROI', ROI)
#     #
#     #
#     #     img2 = cv2.resize(ROI, (ROI.shape[1]*2, ROI.shape[0]*2), interpolation=cv2.INTER_LANCZOS4)  # Resize by x2 using LANCZOS4 interpolation method.
#     #
#     #     cv2.imwrite('image2.png', img2)
#     #     gray_QR = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
#     #     #qrData = Qr_img_to_text(image_file_name
#     #     cv2.imshow('image2', img2)
#     #
#     #     code = decode(gray_QR)
#     #     # print(code)
#     #     try:
#     #         qrData = code[0].data
#     #         isSecureQR = (isSecureQr(qrData))
#     #
#     #         if isSecureQR:
#     #             secure_qr = AadhaarSecureQr(int(qrData))
#     #             decoded_secure_qr_data = secure_qr.decodeddata()
#     #             # print(decoded_secure_qr_data)
#     #
#     #             # json_object = json.dumps(decoded_secure_qr_data, indent=4)
#     #             # # print(json_object)
#     #             # return json_object
#     #             dataCompare = {
#     #                 "name": decoded_secure_qr_data['name'],
#     #                 "pincode": decoded_secure_qr_data['pincode'],
#     #                 "aadhaar_no": decoded_secure_qr_data['adhaar_last_4_digit'],
#     #                 "dob": decoded_secure_qr_data['dob'],
#     #                 "gender": decoded_secure_qr_data['gender'],
#     #                 "district": decoded_secure_qr_data['district'],
#     #                 "landmark": decoded_secure_qr_data['landmark'],
#     #                 "location": decoded_secure_qr_data['location'],
#     #                 "street": decoded_secure_qr_data['street'],
#     #                 "state": decoded_secure_qr_data['state'],
#     #                 "email_linked_with_aadhaar": decoded_secure_qr_data['email'],
#     #                 "mobilenumber_linked_with_aadhaar": decoded_secure_qr_data['mobile'],
#     #
#     #             }
#     #
#     #             information = json.dumps(dataCompare)
#     #             return information

#                 # print(200)

#     #     except IndexError:
#     #         aadhaar_error = "No information found, Try again with better image !!"
#     #         dataCompare = {"error": aadhaar_error}
#     #         information = json.dumps(dataCompare)
#     #         return information
#     #
#     #     # json_data = json.dumps(xmltodict.parse(qrData), indent=4)
#     #     # print(json_data)
#     # except UnboundLocalError:
#     #     text = "information not found !!"

# final_info = aadhaar_verification_extraction()
# # pan_number = pancard_extraction()

# # append_pan = {"pan_number": pan_number[0]}
# # data = json.loads(final_info)
# # data.update(append_pan)
# # final_info = json.dumps(data, indent=4)

# # face_verfication_result = face_verification()
# # face_verfication = {"face_verfication_result": face_verfication_result}
# # final_data = json.loads(final_info)
# # final_data.update(face_verfication)
# # final_info = json.dumps(final_data, indent=4)

# ram = {"RAM Used (GB)": psutil.virtual_memory()[3]/1000000000}
# ram_data = json.loads(final_info)
# ram_data.update(ram)
# final_info = json.dumps(ram_data, indent=4)

# # filepath = os.path.join(os.getcwd(), aadhaar_QR_path)
# # os.remove(filepath)
# # filepath = os.path.join(os.getcwd(), pan_path)
# # os.remove(filepath)
# # filepath = os.path.join(os.getcwd(), selfie_path)
# # os.remove(filepath)
# # filepath = os.path.join(os.getcwd(), 'image.npy')
# # os.remove(filepath)
# # filepath = os.path.join(os.getcwd(), 'image2.png')
# # os.remove(filepath)
# # filepath = os.path.join(os.getcwd(), 'detcted.jpg')
# # os.remove(filepath)
# # filepath = os.path.join(os.getcwd(), 'face.jpg')
# # os.remove(filepath)

# print(final_info)
