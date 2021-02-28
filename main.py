import pytesseract
import argparse
import cv2
import os
from utils import hocr_character_parser


def analyse_image(gray):
    config = '-c hocr_char_boxes=1 hocr'
    args = [gray, 'hocr', None, config, 0, 0]

    hocr = pytesseract.run_and_get_output(*args)
    for character in hocr_character_parser(hocr):
        print("{} - {} - {} conf: {:.2f}".format(character['line_id'], character['word_id'], character['text'],
                                                 character['conf']))


ap = argparse.ArgumentParser()
ap.add_argument("-f", required=True,
                help="image filename")
ap.add_argument("-d", default="images",
                help="image directory")

# python3 main.py -f Cars77.png
if __name__ == "__main__":
    args = vars(ap.parse_args())

    file_path = os.path.join(args["d"], args["f"])
    image = cv2.imread(file_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    analyse_image(gray)

