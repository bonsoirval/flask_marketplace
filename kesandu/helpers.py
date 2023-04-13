from flask import send_from_directory, current_app as app, send_file
import os

def load_image(image): #, path = app.config['SELLERS_UPLOAD']):
    pass
#     # image_path = os.path.abspath(os.path.dirname(image))
#     # image = send_file(image_path)
#     # # image = send_from_directory(image_path, 'nri_isi_seller_1.jpg') # 
#     # return f"Hello, world! {image}".lower()
#     print(send_from_directory(app.config['SELLERS_PRODUCT'], 'nri_isi_seller_1.jpg'))
#     return True