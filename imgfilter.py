import sys, os
import argparse
import glob

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

from PIL import Image

from skimage import data
# from skimage.filters import try_all_threshold, sobel, threshold_mean
from skimage import io
from skimage import img_as_ubyte
from skimage.color import rgb2gray, gray2rgb
from skimage import filters, data
from skimage.morphology import disk, ball
from skimage import exposure

mpl.rcParams['axes.spines.left'] = False
mpl.rcParams['axes.spines.right'] = False
mpl.rcParams['axes.spines.top'] = False
mpl.rcParams['axes.spines.bottom'] = False


def find_files(dir_name, pattern="*.png", recursive=True):
    # Using '*' pattern 
    all_files = [] 
    for name in glob.glob('{}/**/{}'.format(dir_name, pattern), recursive=True): 
        all_files.append(name)
    return all_files 

def filter_grey2rgb(np_image, out_dir, ext="png"):

    np_image = p_image[:, :, 0] if np_image.ndim == 3 else np_image
    # rgb = gray2rgb(p_image)

    # im = Image.fromarray(np.uint8(rgb*255))
    PIL_image = Image.fromarray(np.uint8(np_image)).convert('RGB')
    return PIL_image


def filter_rgb2grey(np_image, out_dir, ext="png"):

    grayscale = rgb2gray(np_image)

    # best_image = grayscale > filters.threshold_mean(grayscale)
    
    PIL_image = Image.fromarray(np.uint8(grayscale*255))
    return PIL_image

def array2image(np_image_array):
    np_image_array = np.repeat(np_image_array[...,None],3,axis=2).astype(np.uint8)
    np_image_array = 255*np_image_array
    return Image.fromarray(np_image_array)



def filter_image(in_image, out_dir, filter="rgb2grey", ext="png"):

    # print(in_image)
    parts = in_image.split('/')

    np_image_array = io.imread(in_image)

    if filter=='rgb2grey':
        im = filter_rgb2grey(np_image_array, out_dir, ext="png")
    elif filter=='grey2rgb':
        im = filter_grey2rgb(np_image_array, out_dir, ext="png")
    elif filter=='threshold_otsu_binary':
        thresh = filters.threshold_otsu(np_image_array)
        binary = np_image_array >= thresh
        im = Image.fromarray(binary)
    elif filter=='threshold_otsu_binary_inv':
        thresh = filters.threshold_otsu(np_image_array)
        binary = np_image_array <= thresh
        im = Image.fromarray(binary)
    elif filter=='mean':
        noisy_image = img_as_ubyte(np_image_array)
        loc_mean = filters.rank.mean(noisy_image, disk(6))
        im = Image.fromarray(loc_mean)        
    elif filter=='global_contrast_enhancement':
        noisy_image = img_as_ubyte(np_image_array)
        glob = exposure.equalize_hist(noisy_image) * 255
        #im = Image.fromarray(glob, 'RGB')     
        im = Image.fromarray(np.uint8(glob))

    if im != None:
        out_img = '{}/{}'.format(out_dir,parts[-1])
        print(out_img)
        im.save(out_img)


# ======================================  
def main(argv):
    print("starting batch img processing. ")

    # Read in command-line parameters
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--in", action="store", required=True, dest="indir", help="image input directory")

    parser.add_argument("-o", "--out", action="store", required=True, dest="out", help="image output directory")

    parser.add_argument("-f", "--filter", action="store", required=True, dest="filter", help="filter name: rgb2grey")

    parser.add_argument("-e", "--ext", action="store", required=False, dest="ext", default="png", help="image output directory")

    args = parser.parse_args()

    try:
        os.makedirs(args.out)
    except OSError:
        pass

    all_files = find_files(args.indir, '*.{}'.format(args.ext))
    for file_path in all_files:
        filter_image(file_path,  args.out, filter=args.filter)
        

if __name__ == "__main__":
    main(sys.argv[1:])
