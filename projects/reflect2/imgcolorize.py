import sys, os
import argparse
import glob
import json
import uuid

import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

from PIL import Image

import skimage
from skimage import data
from skimage.morphology import disk, square
from skimage.filters import try_all_threshold
from skimage.filters import threshold_mean
from skimage import io
from skimage import color
from skimage.color import rgb2gray
from skimage import img_as_float64, img_as_ubyte
from skimage import filters
from skimage.filters.thresholding import _cross_entropy
from skimage.filters import rank

import xml.etree.ElementTree as ET
import random

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


def get_random_pallet(xmlcolors):
    pallets = []
    for pallet in xmlcolors:
        pallets.append(pallet)

    return random.choice(pallets)


def floor_ceil_float(f_val, floor=0.0, ceil=1.0):
    if f_val < floor:
        return floor
    elif f_val > ceil:
        return ceil
    else:
        return f_val


def randomize_color(color_array):

    factor_l = [-0.3,0.0,0.3]
    r_push = color_array[0]+(random.random()*random.choice(factor_l))
    g_push = color_array[1]+(random.random()*random.choice(factor_l))
    b_push = color_array[2]+(random.random()*random.choice(factor_l))

    return [
        floor_ceil_float(r_push), 
        floor_ceil_float(g_push),
        floor_ceil_float(b_push)]


def get_colors(pallet):
    colors = []
    for color in pallet:
        colors.append(color)

    return colors

def get_xml(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    return root

def get_color_by_index(p_colors, index):
    return [int(p_colors[index].attrib['r'])/255, 
        int(p_colors[index].attrib['g'])/255, 
        int(p_colors[index].attrib['b'])/255]


def filter_image(in_image, out_dir, pallet, generate_id=False):
    # print(in_image)
    image_m  = {}
    parts = in_image.split('/')

    if generate_id:
        img_id = str(uuid.uuid4()).replace('-','')[:8]
    else:      
        img_id = parts[-1:][0].split('-')[0]
    
    image_m['id'] = img_id


    p_colors = get_colors(pallet)  
    c_name = p_colors[0].attrib['name']
    

    img_rgb = img_as_float64(io.imread(in_image))
    grayscale_image = color.rgb2gray(img_rgb)


    # # Create a mask selecting regions with interesting texture.
    # noisy = rank.entropy(img_rgb, np.ones((9, 9)))
    # textured_regions = noisy > 4.25
    # # Note that using `colorize` here is a bit more difficult, since `rgb2hsv`
    # # expects an RGB image (height x width x channel), but fancy-indexing returns
    # # a set of RGB pixels (# pixels x channel).

    color_multiplier_0 = randomize_color(get_color_by_index(p_colors, 0))
    color_multiplier_1 = randomize_color(get_color_by_index(p_colors, 1))
    color_multiplier_2 = randomize_color(get_color_by_index(p_colors, 2))
    color_multiplier_3 = randomize_color(get_color_by_index(p_colors, 3))
    color_multiplier_4 = randomize_color(get_color_by_index(p_colors, 4))
    image_m['colors'] = [color_multiplier_0, color_multiplier_1, color_multiplier_2, color_multiplier_3, color_multiplier_4]

    thresh = skimage.filters.threshold_otsu(grayscale_image)
    binary = grayscale_image <= thresh
      
    noisy =  rank.threshold(grayscale_image, square(9))

    n_max = noisy.mean() 

    textured_regions_0 = noisy < (n_max * .1) 
    textured_regions_1 = np.all([noisy >= (n_max * .1), noisy <= (n_max * .3)]) 
    textured_regions_2 = np.all([noisy >= (n_max * .3), noisy <= (n_max * .5)]) 
    textured_regions_3 = np.all([noisy >= (n_max * .6), noisy <= (n_max * .8)]) 
    textured_regions_4 = noisy >= (n_max * .8)    

    masked_image = img_rgb.copy()

    masked_image[textured_regions_0, :] *= color_multiplier_0
    masked_image[textured_regions_1, :] *= color_multiplier_1
    masked_image[textured_regions_2, :] *= color_multiplier_2
    masked_image[textured_regions_3, :] *= color_multiplier_3
    masked_image[textured_regions_4, :] *= color_multiplier_4
    masked_image[binary, :] *= color_multiplier_0


    out_img = '{}/{}.png'.format(out_dir, image_m['id'])
    io.imsave(out_img, img_as_ubyte(masked_image))
    print('out:{} pallete:{}'.format(out_img, c_name))
    image_m['out_img'] = out_img

    return image_m




# ======================================  
def main(argv):
    print("starting batch img processing. ")

    # Read in command-line parameters
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--in", action="store", required=True, dest="indir", help="image input directory")

    parser.add_argument("-o", "--out", action="store", required=True, dest="out", help="image output directory")

    parser.add_argument("-c", "--colors", action="store", required=True, dest="colors", help="colors file")

    parser.add_argument("--generate_id", help="generate new id", action="store_true")

    args = parser.parse_args()

    try:
        os.makedirs(args.out)
    except OSError:
        pass

    colors = get_xml(args.colors)

    all_files = find_files(args.indir)
    images_m = {}
    index = 0
    for file_path in all_files:
        img_model = filter_image(file_path, args.out, get_random_pallet(colors), generate_id=args.generate_id)
        images_m[img_model['id']] = img_model
        index += 1

    f = open("{}/colorized_images.json".format(args.out), "w")
    f.write(json.dumps(images_m, indent=4))
    f.close()
        

if __name__ == "__main__":
    main(sys.argv[1:])
