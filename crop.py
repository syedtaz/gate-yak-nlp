from PIL import Image
from pathlib import Path
from os import listdir
from tqdm.contrib.concurrent import process_map
from typing import Tuple

# constants

HEIGHT = 1792
WIDTH = 828

def crop(arg: Tuple[str, int]):
    image, idx = arg
    im = Image.open(image)
    new = im.crop((0, 185, WIDTH, HEIGHT-475))
    path = str(Path("./cropped/").resolve()) + '/' + str(idx) + ".png"
    new.save(fp = path)

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
    
    