import os
import cv2
import numpy as np
from keras.utils import to_categorical
import xml.etree.ElementTree as ET
import pytesseract
import csv
from pdf2image import convert_from_path


def load_data():
    # Load images and labels
    data_path = 'C:\\Users\\zigya\\OneDrive\\Desktop\\Project\\Invoice-2\\data\\images' 
    label_path = 'C:\\Users\\zigya\\OneDrive\\Desktop\\Project\\Invoice-2\\data\\labels' 
    images = []
    labels =[]
    for filename in os.listdir(data_path):
        img = cv2.imread(os.path.join(data_path, filename))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, (256, 256))
        images.append(img)
        label_file = os.path.join(label_path, os.path.splitext(filename)[0] + '.xml')
        with open(label_file, 'r') as f:
            label_data = f.read()
            label_data = label_data.strip()
            labels.append(label_data)

    # Convert labels to one-hot encoding
    label_classes = sorted(list(set(labels)))
    label_to_idx = {label: i for i, label in enumerate(label_classes)}
    idx_to_label = {i: label for i, label in enumerate(label_classes)}
    labels = [label_to_idx[label] for label in labels]
    labels = to_categorical(labels, num_classes=len(label_classes))

    return np.array(images), np.array(labels), idx_to_label

def get_annotation_info(xml_file_path, img_path):
    root = ET.fromstring(xml_file_path)
    annotations = [] # list to store the annotations
    img = cv2.imread(img_path) # reading the input image
    norm_img = np.zeros((img.shape[0], img.shape[1]))
    img = cv2.normalize(img, norm_img, 0, 255, cv2.NORM_MINMAX)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # converting the image to grayscale
    thresh = cv2.threshold(gray, 64, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1] # applying threshold to the image
    for obj in root.findall('object'):
        # Extract the label name
        annotation = {}
        annotation['label'] = obj.find('name').text

        # Extract the bounding box coordinates
        bbox = obj.find('bndbox')
        xmin = int(bbox.find('xmin').text)
        ymin = int(bbox.find('ymin').text)
        xmax = int(bbox.find('xmax').text)
        ymax = int(bbox.find('ymax').text)
        cropped_img = thresh[ymin:ymax, xmin:xmax] # cropping the image based on the bounding box coordinates
        annotation['text'] = pytesseract.image_to_string(cropped_img) # using OCR to extract the text from the cropped image
        annotations.append(annotation) # adding the annotation to the list

    return annotations # returning the list of annotations

def create_csv(invoice_data, file_path):
    with open(file_path ,'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Label', 'Text'])
        for key, value in invoice_data.items():
            writer.writerow([key, value])
            
def pdf_to_jpg(pdf_file, output_file):
    # Convert the PDF file to a PIL image object
    pages = convert_from_path(pdf_file)
    img = pages[0]

    # Save the image as a JPEG file
    img.save(output_file, 'JPEG')
    
    return output_file
