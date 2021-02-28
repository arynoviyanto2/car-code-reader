import pytesseract
import argparse
import cv2
import os
from utils import hocr_character_parser


def analyse_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    config = '-c hocr_char_boxes=1 hocr'
    args = [gray, 'hocr', None, config, 0, 0]

    hocr = pytesseract.run_and_get_output(*args)
    for character in hocr_character_parser(hocr):
        print("{} - {} - {} conf: {:.2f}".format(character['line_id'], character['word_id'], character['text'],
                                                 character['conf']))
        (x1, y1, x2, y2) = character["bbox"]
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255), 1)
        cv2.putText(image, character['text'], (x1 - 10, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    cv2.imshow("image", image)
    cv2.waitKey()


ap = argparse.ArgumentParser()
ap.add_argument("-f", required=True,
                help="image filename")
ap.add_argument("-d", default="images",
                help="image directory")

# python3 main.py -f Cars77.png
if __name__ == "__main__":
    args = vars(ap.parse_args())

    file_path = os.path.join(args["d"], args["f"])
    in_image = cv2.imread(file_path)

    analyse_image(in_image)

