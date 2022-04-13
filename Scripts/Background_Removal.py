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
    plot = img_path.split('/')[-1].split('.')[-2]
    
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
    cv2.imwrite(f"{out_dir}/{plot}_Cropped.png", cropped_image)

    print('')
    print('**** Image Cropped and Saved ****')
    return cropped_image

# ----------------------------------

def create_mask(img_path, c_img):
    # Establish Plot Name
    plot = img_path.split('/')[-1].split('.')[-2]

    date = img_path.split('/')[-2]
    
    # # Load Image
    # img = cv2.imread(img_path)

    # Set Boundaries for mask
    lower = np.array([0, 52, 72], dtype = "uint16") ## Pink Tag Values are approximately (217, 149, 172; R, G, B)
    upper = np.array([95, 255, 255], dtype = "uint16")
    mask = cv2.inRange(c_img, lower, upper)

    ## Inverting the mask
    Mask = cv2.bitwise_not(mask)

    # Set out directory and create if not already in working directory
    out_dir = os.path.join('Mask_Images', str(date))

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    # Save the mask
    cv2.imwrite(f'{out_dir}/{plot}_mask.png', Mask)

    print('')
    print('**** Mask Created and Saved ****')
    return Mask

# ----------------------------------

def remove_background(img_path, c_img, Mask):
    # Establish Plot Name
    plot = img_path.split('/')[-1].split('.')[-2]
    # Establish Date
    date = img_path.split('/')[-2]

    _, Mask = cv2.threshold(Mask, thresh=180, maxval=255, type=cv2.THRESH_BINARY)

    # copy where we'll assign the new values
    no_back = np.copy(c_img)

    # boolean indexing and assignment based on mask
    no_back[(Mask==255).all(-1)] = [0,0,0]

    # Set out directory and create if not already in working directory
    out_dir = os.path.join('Clean_Images', str(date))

    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    # Save the mask
    cv2.imwrite(f'{out_dir}/{plot}_clean.png', no_back)

    print('')
    print('**** Background Removed and Saved ****')
    return no_back

# ----------------------------------

def main():

    args = get_args()

    image = args.dir
    for img in image:
        
        plot = img.split('/')[-1].split('.')[-2]

        date = img.split('/')[-2]

        cropped_image = crop_img(img)

        c_img = cv2.imread(f'Cropped_Images/{date}/{plot}_Cropped.png')

        create_mask(img, c_img)

        Mask = cv2.imread(f'Mask_Images/{date}/{plot}_mask.png')

        no_back = remove_background(img, c_img, Mask)

# ----------------------------------
if __name__ == "__main__":
    main()