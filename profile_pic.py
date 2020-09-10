import os
from PIL import Image
from flask import url_for, current_app

def add_profile_pic(pic_upload, pet_id):
    filename = pic_upload.filename
    storage_filename = str(pet_id) + '.' + filename.split('.')[-1]

    file_path = os.path.join(current_app.root_path, 'static', storage_filename)

    pic = Image.open(pic_upload)
    pic.thumbnail((200, 200))
    pic.save(file_path)

    return storage_filename
