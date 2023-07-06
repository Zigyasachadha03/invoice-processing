from flask import Flask, request, render_template, send_file, make_response, Response, send_from_directory
import os
import random
import string
import utils
from keras.models import load_model
import cv2
import numpy as np
from datetime import datetime
import json
import csv


app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_uppercase + string.digits, k=32))
# app.upload_folder = 'C:\\Users\\zigya\\OneDrive\\Desktop\\Invoice-2\\static\\uploaded_files'
app.model_path = 'test_model.h5'


loaded_model = load_model(app.model_path)
# Create a dictionary to store the invoice data
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
invoice_data = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Get the uploaded file from the request
    file = request.files['invoice']
    filename = datetime.now().strftime("%Y%m%d_%H%M%S_") + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)) + '.jpg'
    img_path = file.save('C:\\Users\\zigya\\OneDrive\\Desktop\\Invoice-2\\static\\uploaded_files\\' + filename)

    
    # Read the file as an image
    invoice_image = cv2.imread('C:\\Users\\zigya\\OneDrive\\Desktop\\Invoice-2\\static\\uploaded_files\\' + filename )


    # Preprocess the image
    img_gray = cv2.cvtColor(invoice_image, cv2.COLOR_BGR2GRAY)
    img_resized = cv2.resize(img_gray, (256, 256))
    img_reshaped = img_resized.reshape(1, 256, 256, 1)

    # Get the model's predictions for the input image
    pred_probs = loaded_model.predict(img_reshaped)[0]

    # Get the predicted class label
    pred_class = np.argmax(pred_probs)

    # Map the predicted class label back to the original class name
    images, labels, idx_to_label = utils.load_data()
    pred_label = idx_to_label[pred_class]

    # Get the annotation information from the XML file and extract the text using OCR
    annotations = utils.get_annotation_info(pred_label , 'C:\\Users\\zigya\\OneDrive\\Desktop\\Invoice-2\\static\\uploaded_files\\' + filename)

    # Loop through the annotations and add the information to the dictionary
    for annotation in annotations:
        if annotation['text'] == "": 
            continue
        else:
            label = annotation['label']
            text = annotation['text']
            invoice_data[label] = text
    # Convert the dictionary to a formatted JSON string with newlines and indentation
    invoice_data_str = json.dumps(invoice_data, indent=3)

    # Add a newline after each opening curly brace and comma in the JSON string
    invoice_data_str = invoice_data_str.replace("{", "{\n").replace(",", ",\n")
    
    # Render the CSV data in the index.html template
    return render_template('index.html', output = invoice_data_str)


@app.route('/download_csv')
def download_csv():
    # Create a CSV file from the invoice data
    # Path of the folder to save the file in
    folder_path = 'C:\\Users\\zigya\\OneDrive\\Desktop\\Invoice-2\\static\\uploaded_files\\'
    
    # Path of the file to save
    filename = datetime.now().strftime("%Y%m%d_%H%M%S_") + 'invoice_data'
    file_path = os.path.join(folder_path, filename + '.csv')

    # Write the data to the CSV file
    with open(file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in invoice_data.items():
            writer.writerow([key, value.strip()])

    # Return the file as a download
    return send_file(file_path, as_attachment=True)


@app.route('/view_csv')
def view_csv():
    # generate the CSV file
    csv_data = []
    for key, value in invoice_data.items():
        csv_data.append([key, value.strip()])
    # render the data in a template
    return render_template('view_csv.html', csv_data=csv_data)
    
if __name__ == '__main__':
    app.run(debug=True)
