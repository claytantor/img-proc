import pathlib
import os, sys
import string
import numpy
import json
from imgtext import draw_paragraph, draw_textline
import xml.etree.ElementTree as ET
import random
import glob
import utils
from PIL import Image, ImageDraw, ImageFont

text_path = "/Users/claytongraham/data/projects/nifty/txt"
colors_path = "/Users/claytongraham/data/projects/nifty/colors"
images_path = "/Users/claytongraham/data/projects/nifty/faces/reflect01_colorize"
font_path_OCR = "/Users/claytongraham/data/projects/nifty/fonts/OCRA.ttf"
images_path_txt = "/Users/claytongraham/data/projects/nifty/faces/reflect01_txt"
images_path_thumb = "/Users/claytongraham/data/projects/nifty/faces/reflect01_thumb"



# def find_files(dir_name, pattern="*.png", recursive=True):
#     # Using '*' pattern 
#     all_files = [] 
#     for name in glob.glob('{}/**/{}'.format(dir_name, pattern), recursive=True): 
#         all_files.append(name)
#     return all_files 


if __name__ == "__main__":

    pathdir = pathlib.Path(__file__).parent.absolute()

    

