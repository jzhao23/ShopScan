import io
import os

from google.cloud import vision
from google.cloud.vision import types

def detect_text(path):
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('\n"{}"'.format(texts[0].description))

if __name__ == "__main__":
    detect_text("/Users/jasonzhao/Documents/GitHub/ShopScan/receipt_scanner/images/test4.JPG")
