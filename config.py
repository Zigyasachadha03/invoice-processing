# from dotenv import load_dotenv
# import os

# load_dotenv()

# class Config:
#     # SECRET_KEY = os.getenv('SECRET_KEY')
#     UPLOAD_FOLDER = os.getenv('static/uploaded_files')
#     MODEL_PATH = os.getenv('test_model.h5')
#     # XML_PATH = os.getenv('XML_PATH')


import utils

images, labels, idx_to_label = utils.load_data()

print(idx_to_label)
