
from PIL import Image
import face_recognition

img_folder = "C:/GITHUB/DTB-instafacesearch/python_code_tmp"
members = ["JENNIE", "JISOO", "LISA", "ROSE"]

for member in members:
    for i in range(1000):
        image = face_recognition.load_image_file(f"{img_folder}/img/{member}/{i}.jpg")
        face_locations = face_recognition.face_locations(image)

        for face_location in face_locations:
            top, right, bottom, left = face_location
            face_image = image[top:bottom, left:right]

            pil_image = Image.fromarray(face_image)
            pil_image.save(f"{img_folder}/img_crop/{member}/{i}.jpg")
            print(f"{member} {i} img saved.")