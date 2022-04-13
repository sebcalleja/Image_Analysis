#!/usr/bin/env python3

import pandas as pd
from PIL import Image
import cv2
import sys
import numpy as np
import os
import argparse

# ----------------------------------

def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description="Individual plant temperature extraction",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("dir", metavar="dir", help="Directory containing geoTIFFs", nargs = '+')

    return parser.parse_args()

# ----------------------------------

def crop_img(img_path):
    plot = img_path.split('/')[-1][-9:-4]
    print(plot)

    date = img_path.split('/')[-2]

    img = cv2.imread(img_path)

    # Cropping an image
    cropped_image = img[200:1450, 700:2200] #[pixels in the vertical direction, pixels in the horizontal direction]

    # Set out directory and create if not already in working directory
    out_dir = os.path.join('Cropped_Images', str(date))

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    # Save the cropped image
    cv2.imwrite(f"{out_dir}/{plot}_Cropped.jpg", cropped_image)

    print('Image Cropped and Saved')

# ----------------------------------

def main():

    args = get_args()

    image = args.dir
    for img in image:
        
        cropped_images = crop_img(img)

# ----------------------------------
if __name__ == "__main__":
    main()