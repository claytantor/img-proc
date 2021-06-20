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
import argparse

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

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
    img_name = img_path.split('/')[-1:]
    #"a/b/c/d".split('/')[-1:]
    return img_name[0].split('.')[0]

def make_rgb_string(color_i):
    return 'rgb({},{},{})'.format(
        int(color_i[0]*255), int(color_i[1]*255), int(color_i[2]*255))

def get_rgb_color(colors, index):
    color_i = colors[index]
    return make_rgb_string(color_i)
    

def get_color_by_index(index, colors):
    # result = list(map(lambda x: numpy.mean(x), colors)) 
    # m = max(result)
    # max_index = [i for i, j in enumerate(result) if j == m] 
    # # print(max_index[0], colors[max_index[0]])
    return make_rgb_string(colors[index])


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

def draw_img_id(im, img_id, image_draw, ttf_font_path, img_height, text_size=20, color = 'rgb(0, 0, 0)', shadowcolor = 'rgb(255, 255, 255)'):
    font_album = ImageFont.truetype(ttf_font_path, size=text_size)
    # color = 'rgb(0, 0, 0)' # black color
    # shadowcolor = 'rgb(255, 255, 255)' # grey color
    draw_textline(im, img_id, image_draw, font_album, color, shadowcolor, 10, img_height-text_size-20)

def draw_sig(im, sig_txt, image_draw, ttf_font_path, img_height, img_width, text_size=10, color = 'rgb(0, 0, 0)', shadowcolor = 'rgb(255, 255, 255)'):
    font_album = ImageFont.truetype(ttf_font_path, size=text_size)
    # color = 'rgb(0, 0, 0)' # black color
    # shadowcolor = 'rgb(255, 255, 255)' # grey color
    draw_textline(im, sig_txt, image_draw, font_album, color, shadowcolor, img_width-(text_size*len(sig_txt))+50, img_height-text_size-20, offset=2)

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

    # p_color = get_darkest(img_model['colors'])
    # p_shadowcolor = get_brightest(img_model['colors'])

    p_color = make_rgb_string(img_model['colors'][2])
    p_shadowcolor = make_rgb_string(img_model['colors'][3])
    

    # the poem
    draw_paragraph(im, img_model['text'].replace('|','\n'), image_draw, img_model['font_path'],
        10, 5, title_size=32, justify=False, line_width=25, color = p_color, 
        shadowcolor = p_shadowcolor)
    
    # the id
    draw_img_id(im, img_model['id'], image_draw, img_model['font_path'], im.height, text_size=80, color = p_color, shadowcolor = p_shadowcolor)

    # sig
    draw_sig(im, '@claytantor', image_draw, img_model['font_path'], im.height, im.width, text_size=25, color = p_color, shadowcolor = p_shadowcolor)
    
    out_img_path = '{}/{}'.format(out_dir, '{}.png'.format(img_model['id']))
    print(out_img_path)
    im.save(out_img_path, "PNG", optimize=True, quality=20)


def save_data(images_data):
    f = open("images_final.json", "w")
    f.write(json.dumps(images_data, indent=4))
    f.close()


def generate_colors_model(id_list):
    for id_val in id_list:
        print(id_val)


def main(argv):
    print("starting batch img processing. ")

    # Read in command-line parameters
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--in", action="store", required=True, dest="indir", help="image input directory")
    parser.add_argument("-o", "--out", action="store", required=True, dest="out", help="image output directory")
    parser.add_argument("-t", "--text", action="store", required=True, dest="text_path", help="directory to find text")  
    parser.add_argument("-c", "--colors_file", action="store", required=True, dest="colors_file", help="file containing the colorized_images info")
    parser.add_argument("-f", "--font_ttf", action="store", required=True, dest="font_ttf", help="true type font to use")

    args = parser.parse_args()

    out_path = Path(args.out)
    parent = out_path.parent
    txt_path = "{}/i_txt".format(out_path.parent)

    try:
        os.makedirs(args.out)    
    except OSError:
        pass

    try:
        os.makedirs(txt_path)     
    except OSError:
        pass

    pathdir = pathlib.Path(__file__).parent.absolute()

    # get the colors file
    #c_images_file = os.path.join(args.colors_dir)
    colors_f = open(args.colors_file, "r")
    colors_m = json.loads(colors_f.read())


    # id_list = json.loads(colors_f.read())
    # colors_m = generate_colors_model(id_list)

    # glob 1
    images_paths = list(utils.find_files(args.indir, pattern="*.png"))
    images_paths.sort()

    # glob 2
    txt_paths = list(utils.find_files(args.text_path, pattern="*.txt"))
    txt_paths.sort()

    images_data = []

    index = 0
    # print(images_paths)
    for img_p in images_paths:

        # print(img_p)

        img_model = {
            'font_path': args.font_ttf
        }
        img_model['image_path'] = img_p
        img_model['author'] = "@claytantor"
        
        img_id = get_id_from_imgpath(img_p)
        # print(img_id)
        img_model['id'] = img_id
        img_model['colors'] = colors_m[img_id]['colors']

        text_fp = os.path.join(args.text_path, txt_paths[index]) 
        print("text",text_fp)
        text_file = open(text_fp, "r") 
        text_file_content = text_file.read()
        text_file_content_lines = text_file_content.replace('\n','|')
        img_model['text'] = text_file_content_lines

        file_name = '{}.png'.format(img_id)

        images_data.append(img_model)

        draw_image_model(img_model, args.out)

        # save the indexed file os.makedirs("{}/i_txt".format(args.out))   
        text_file_n = open("{}/{}.txt".format(txt_path, img_model['id']), "w") 
        text_file_n.write(text_file_content)
        text_file_n.close()

        index+=1

    save_data(images_data)
   





if __name__ == "__main__":
    main(sys.argv[1:])


