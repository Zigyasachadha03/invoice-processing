import cv2
import numpy as np
import pytesseract
import xml.etree.ElementTree as ET
from app import Flask, render_template, request, redirect, url_for
from utils import idx_to_label, get_annotation_info, create_csv
from keras.models import load_model

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Get the uploaded file from the request
    file = request.files['file']

    # Read the file as an image
    invoice_image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)

    # Load the trained model
    loaded_model = load_model('test_model.h5')

    # Preprocess the image
    img_gray = cv2.cvtColor(invoice_image, cv2.COLOR_BGR2GRAY)
    img_resized = cv2.resize(img_gray, (256, 256))
    img_reshaped = img_resized.reshape(1, 256, 256, 1)

    # Get the model's predictions for the input image
    pred_probs = loaded_model.predict(img_reshaped)[0]

    # Get the predicted class label
    pred_class = np.argmax(pred_probs)

    # Map the predicted class label back to the original class name
    pred_label = idx_to_label[pred_class]

    # Get the annotation information from the XML file and extract the text using OCR
    annotations = get_annotation_info(pred_label , file)

    # Create a dictionary to store the invoice data
    invoice_data = {}

    # Loop through the annotations and add the information to the dictionary
    for annotation in annotations:
        if annotation['text'] == "": 
            continue
        else:
            label = annotation['label']
            text = annotation['text']
            invoice_data[label] = text

    # Create a CSV file from the invoice data
    csv_data = create_csv(invoice_data)

    # Render the CSV data in the index.html template
    return render_template('index.html', csv_data=csv_data)

if __name__ == '__main__':
    app.run(debug=True)
