from PIL import Image
from pathlib import Path
from os import listdir
from cv2 import imread, matchTemplate, TM_CCOEFF_NORMED
from tqdm.contrib.concurrent import process_map
from typing import Tuple
import numpy as np

# constants

HEIGHT = 1792
WIDTH = 828

def crop(arg: Tuple[str, int]):
    image_path, idx = arg

    # Find divider positions
    image = imread(image_path)
    divider = imread('divider.png')
    result = matchTemplate(image, divider, TM_CCOEFF_NORMED)
    y, _ = np.where(result >= 0.85)

    # Crop image
    im = Image.open(image_path)
    for offset, (start, end) in enumerate(zip(y, y[1:])):
        new = im.crop((0, start, WIDTH, end))
        w, h = new.size

        # Ignore if dividers are not correctly found.
        if h > 400:
            print(image_path)
            continue

        # Crop out the bottom and the upvote button
        try:
            new = new.crop((0, 0, w-88, h-136))
            path = str(Path("./cropped/").resolve()) + '/' + str(idx * 3 + offset) + ".png"
            new.save(fp = path)
        # Ignore crops that are just the divider and nothing else.
        except ValueError:
            pass

def main():
    p = Path("./raw/")
    prefix = str(p.resolve()) + '/'
    files = [prefix + x for x in listdir(p)]
    files = [(val, idx) for idx, val in enumerate(files)]

    # for idx, image in enumerate(files):
    #     crop(image, idx)

    r = process_map(crop, files)

if __name__ == "__main__":
    main()
    
    