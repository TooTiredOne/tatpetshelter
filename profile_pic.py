import os
from PIL import Image
from flask import url_for, current_app

def add_profile_pic(pic_upload, pet_id):
    filename = pic_upload.filename
    ext_type = filename.split('.')[-1]
    storage_filename = str(pet_id) + '.' + ext_type

    file_path = os.path.join(current_app.root_path, 'static', storage_filename)

    output_size = (200, 200)

    pic = Image.open(pic_upload)
    pic.thumbnail(output_size)
    pic.save(file_path)

    return storage_filename
