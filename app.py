import sys, os
import argparse
import glob

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

from skimage import data
from skimage.filters import try_all_threshold
from skimage.filters import threshold_mean
from skimage import io
from skimage.color import rgb2gray
from skimage import filters
from skimage.filters.thresholding import _cross_entropy

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

def filter_image(in_image, out_dir):
    # print(in_image)
    parts = in_image.split('/')

    image = io.imread(in_image)
    grayscale = rgb2gray(image)

    best_image = grayscale > filters.threshold_li(grayscale)

    plt.box(False)
    plt.imshow(best_image, cmap=plt.cm.gray)
    plt.axis('off')

    out_img = '{}/{}'.format(out_dir,parts[-1])
    print(out_img)
    plt.savefig(out_img, bbox_inches='tight')

# ======================================  
def main(argv):
    print("starting batch img processing. ")

    # Read in command-line parameters
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--in", action="store", required=True, dest="indir", help="image input directory")

    parser.add_argument("-o", "--out", action="store", required=True, dest="out", help="image output directory")

    args = parser.parse_args()

    all_files = find_files(args.indir)
    for file_path in all_files:
        filter_image(file_path, args.out)
        


if __name__ == "__main__":
    main(sys.argv[1:])
