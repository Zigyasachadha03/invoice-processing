# Invoice Processing

The Invoice Processing project is designed to extract information from Amazon invoices. It takes an Amazon invoice as an input file and extracts the following information:

- Name
- Company Name
- Address
- Item Description
- Item Amount
- Total Amount

## Project Description

This project utilizes a deep learning Convolutional Neural Network (CNN) to process Amazon invoices. The model has been trained specifically for Amazon invoices using the labelImg tool for annotation. The annotation process involved creating bounding boxes around the relevant information on the invoice, and then extracting the text from these bounding boxes using OCR (Optical Character Recognition) technology. The pytesseract OCR engine was used in this project.

## Usage

1. Clone the repository:
   ```
   git clone https://github.com/Zigyasachadha03/invoice-processing.git
   ```
   
2. Install the required dependencies.
  
3. Launch the application:
   ```
   python app.py
   ```
   
4. Open your web browser.

5. Upload an Amazon invoice file (supported formats: PNG, JPG, JPEG, PDF).

6. Once the file is uploaded, the application will extract the relevant information from the invoice, including the name, company name, address, item description, item amount, and total amount.

7. You have the option to view the extracted information online or download it in a CSV file.



