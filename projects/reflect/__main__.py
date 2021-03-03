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
images_path_target = "/Users/claytongraham/data/projects/nifty/faces/reflect01_txt"


def get_random_pallet(xmlcolors):
    pallets = []
    for pallet in xmlcolors:
        pallets.append(pallet)

    return random.choice(pallets)

def get_xml(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    return root

def get_id_from_imgpath(img_path):
    # /Users/claytongraham/data/projects/nifty/faces/reflect01_colorize/bc26ce0c-c09a-43d4-864b-a5faf765ec23.png

    img_name = img_path.split('/')[-1:]
    #"a/b/c/d".split('/')[-1:]
    return img_name[0].split('-')[0]

def make_rgb_string(color_i):
    return 'rgb({},{},{})'.format(
        int(color_i[0]*255), int(color_i[1]*255), int(color_i[2]*255))

def get_rgb_color(colors, index):
    color_i = colors[index]
    return make_rgb_string(color_i)
    

def get_brightest(colors):
    result = list(map(lambda x: numpy.mean(x), colors)) 
    m = max(result)
    max_index = [i for i, j in enumerate(result) if j == m] 
    # print(max_index[0], colors[max_index[0]])
    return make_rgb_string(colors[max_index[0]])

def get_darkest(colors):
    result = list(map(lambda x: numpy.mean(x), colors)) 
    m = min(result)
    min_index = [i for i, j in enumerate(result) if j == m] 
    # print(min_index[0], colors[min_index[0]])
    return make_rgb_string(colors[min_index[0]])

def draw_img_id(img_id, image_draw, ttf_font_path, img_height, text_size=20, color = 'rgb(0, 0, 0)', shadowcolor = 'rgb(255, 255, 255)'):
    font_album = ImageFont.truetype(ttf_font_path, size=text_size)
    # color = 'rgb(0, 0, 0)' # black color
    # shadowcolor = 'rgb(255, 255, 255)' # grey color
    draw_textline(img_id, image_draw, font_album, color, shadowcolor, 10, img_height-text_size-20)

def draw_sig(sig_txt, image_draw, ttf_font_path, img_height, img_width, text_size=10, color = 'rgb(0, 0, 0)', shadowcolor = 'rgb(255, 255, 255)'):
    font_album = ImageFont.truetype(ttf_font_path, size=text_size)
    # color = 'rgb(0, 0, 0)' # black color
    # shadowcolor = 'rgb(255, 255, 255)' # grey color
    draw_textline(sig_txt, image_draw, font_album, color, shadowcolor, img_width-(text_size*len(sig_txt))+50, img_height-text_size-20, offset=2)

def draw_image_model(img_model, out_dir):

    # image = Image.open('background.png')
    im = utils.open_image(img_model['image_path'])

    # initialise the drawing context with
    # the image object as background

    # if the out dir doesnt exist the create it
    try:
        os.makedirs(out_dir)
    except OSError:
        pass

    image_draw = ImageDraw.Draw(im)

    # p_color = 'rgb(0, 0, 0)'
    # p_color = get_rgb_color(img_model['colors'],3)
    # p_shadowcolor = get_rgb_color(img_model['colors'],1)

    p_color = get_darkest(img_model['colors'])
    p_shadowcolor = get_brightest(img_model['colors'])


    # the poem
    draw_paragraph(img_model['text'].replace('|','\n'), image_draw, img_model['font_path'],
        10, 5, title_size=45, color = p_color, 
        shadowcolor = p_shadowcolor)
    
    # the id
    draw_img_id(img_model['id'], image_draw, img_model['font_path'], im.height, text_size=80, color = p_color, shadowcolor = p_shadowcolor)

    # sig
    draw_sig('@claytantor', image_draw, img_model['font_path'], im.height, im.width, text_size=25, color = p_color, shadowcolor = p_shadowcolor)
    
    out_img_path = '{}/{}'.format(out_dir, '{}.png'.format(img_model['id']))
    print(out_img_path)
    im.save(out_img_path, "PNG", optimize=True, quality=20)


def save_data(images_data):
    f = open("images_final.json", "w")
    f.write(json.dumps(images_data, indent=4))
    f.close()


if __name__ == "__main__":

    pathdir = pathlib.Path(__file__).parent.absolute()

    # get the colors file
    c_images_file = os.path.join(pathdir,"colorized_images.json")
    colors_f = open(c_images_file, "r")
    colors_m = json.loads(colors_f.read())

    # glob 1
    images_paths = utils.find_files(images_path, pattern="*.png")

    # glob 2
    txt_paths = utils.find_files(text_path, pattern="*.txt")

    images_data = []

    index = 0
    for img_p in images_paths:

        img_model = {
            'font_path': font_path_OCR
        }
        img_model['image_path'] = img_p
        img_model['author'] = "@claytantor"
        
        img_id = get_id_from_imgpath(img_p)
        img_model['id'] = img_id
        img_model['colors'] = colors_m[img_id]['colors']

        text_fp = os.path.join(text_path, txt_paths[index]) 
        text_file = open(text_fp, "r") 
        text_file_content = text_file.read()
        text_file_content_lines = text_file_content.replace('\n','|')
        img_model['text'] = text_file_content_lines

        file_name = '{}.png'.format(img_id)

        images_data.append(img_model)

        draw_image_model(img_model, images_path_target)

        index+=1

    save_data(images_data)

