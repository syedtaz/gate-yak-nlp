from PIL import Image, ImageOps
import pytesseract
import os
from csv import writer

RAW_IMAGE_PATH = os.path.join(os.getcwd(), 'cropped')
DATA_PATH = os.path.join(os.getcwd(), 'data', 'yikyak.csv')
config = '--psm 6'

f = open(DATA_PATH, 'w')
outfile = writer(f)
for img_name in os.listdir(RAW_IMAGE_PATH):
    img_path = os.path.join(RAW_IMAGE_PATH, img_name)
    image = ImageOps.invert(Image.open(img_path).convert("L"))
    text = pytesseract.image_to_string(image, lang='eng')
    
    text = text.strip().replace("\n", " ")
    outfile.writerow([text])

f.close()

    
    
