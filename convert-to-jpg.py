from PIL import Image
import os
from pdf2image import convert_from_path

# specify the input and output directories
input_img_dir = 'C:\\Users\\zigya\\OneDrive\\Desktop\\Invoice-2\\'
output_img_dir = 'C:\\Users\\zigya\\OneDrive\\Desktop\\Invoice-2\\'


filename= "amazon-262.pdf"

if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.pdf') or filename.endswith('.jpeg'):           # check if the file is an image
    if filename.endswith('.pdf'):
        # convert the PDF to a list of PIL images
        pages = convert_from_path(os.path.join(input_img_dir, filename))
        if len(pages) == 1:
            # if there's only one page, save it as a JPEG image
            pages[0].save(os.path.join(output_img_dir, f"{filename.split('.')[0]}.jpg"))
        else:
            # save each page as a separate JPEG image
            for i, page in enumerate(pages):
                page.save(os.path.join(output_img_dir, f"{filename.split('.')[0]}_{i}.jpg"))
    else:
        img = Image.open(os.path.join(input_img_dir, filename))              # open the image using Pillow
        img = img.convert('RGB')          # convert the image to JPG format
        img.save(os.path.join(output_img_dir, filename.split('.')[0] + '.jpg'))           # save the converted image to the output directory
