import glob
import os.path
from os import path
from PIL import Image

def load_yaml(yamlFilePath):
    cfg = None
    with open(yamlFilePath, 'r') as ymlfile:
        cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
    return cfg


def find_files(dir_name, pattern="*.png", recursive=True):
    # Using '*' pattern 
    all_files = [] 
    for name in glob.glob('{}/**/{}'.format(dir_name, pattern), recursive=True): 
        all_files.append(name)
    return all_files 

def open_image(img_path):
    try:
        with Image.open(img_path) as im:
            
            im.load()
            im = im.convert('RGBA')
            print(img_path, im.format, "%dx%d" % im.size, im.mode)
            return im
    except IOError:
        print('error')
        pass


def find_files(dir_name, pattern="*.png", recursive=True):
    # Using '*' pattern 
    all_files = [] 
    for name in glob.glob('{}/**/{}'.format(dir_name, pattern), recursive=True): 
        all_files.append(name)
    return all_files 