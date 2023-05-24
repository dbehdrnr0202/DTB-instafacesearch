
from PIL import Image
import face_recognition
import os

img_folder = "C:/GITHUB/DTB-instafacesearch/python_code_tmp"
members = ["JENNIE", "JISOO", "LISA", "ROSE"]

if not os.path.isdir(f'{img_folder}/img_crop'):
    os.mkdir(f'{img_folder}/img_crop')

for member in members:
    file_list = os.listdir(f"{img_folder}/img/{member}")
    
    if not os.path.isdir(f'{img_folder}/img_crop/{member}'):
        os.mkdir(f'{img_folder}/img_crop/{member}')

    for img_name in file_list:
        image = face_recognition.load_image_file(f"{img_folder}/img/{member}/{img_name}")
        face_locations = face_recognition.face_locations(image)

        for face_location in face_locations:
            top, right, bottom, left = face_location
            face_image = image[top:bottom, left:right]

            pil_image = Image.fromarray(face_image)
            pil_image.save(f"{img_folder}/img_crop/{member}/{img_name}")
            print(f"{member} {img_name} img saved.")