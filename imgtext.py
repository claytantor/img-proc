import sys, os
import argparse
import utils
import textwrap

# import required classes

from PIL import Image, ImageDraw, ImageFont

# create Image object with the input image

def draw_textline(message_text, draw, font, color, shadowcolor, xpos, ypos):

    (x,y) = (xpos,ypos)

    # thicker border
    draw.text((x-2, y-2), message_text, font=font, fill=shadowcolor)
    draw.text((x+2, y-2), message_text, font=font, fill=shadowcolor)
    draw.text((x-2, y+2), message_text, font=font, fill=shadowcolor)
    draw.text((x+2, y+2), message_text, font=font, fill=shadowcolor)

    draw.text((x, y), message_text, fill=color, font=font)


def draw_title(title_message_text, draw, ttf_font_path, title_size=45):
    font_title = ImageFont.truetype(ttf_font_path, size=title_size)

    (x, y) = (5, 5)
    color = 'rgb(0, 0, 0)' # black color
    shadowcolor = 'rgb(255, 255, 255)' # grey color

    lines = textwrap.wrap(title_message_text, width=20)
    line_height = 35
    index = 0
    for line in lines:
        draw_textline(line, draw, font_title, color, shadowcolor, 5, (index*line_height))
        index += 1


def draw_album_name(txt_message_text, draw, img, ttf_font_path, txt_size=20):
    font_album = ImageFont.truetype(ttf_font_path, size=txt_size)
    # (x, y) = (img.height-txt_size-5, 5)
    color = 'rgb(0, 0, 0)' # black color
    shadowcolor = 'rgb(255, 255, 255)' # grey color
    draw_textline(txt_message_text, draw, font_album, color, shadowcolor, 5, img.height-txt_size-5)


def text_overlay(image_path, title_message_text, ttf_font_path, out_dir):

    # image = Image.open('background.png')
    im = utils.open_image(image_path)

    # initialise the drawing context with
    # the image object as background


    draw = ImageDraw.Draw(im)
    draw_title(title_message_text, draw, ttf_font_path, title_size=45)
    draw_album_name("the richest family", draw, im, ttf_font_path, txt_size=20)

    # save the edited image
    img_path_parts = image_path.split('/')
    out_img_path = '{}/{}'.format(out_dir, img_path_parts[-1])
    print(out_img_path)
    im.save(out_img_path, "PNG", optimize=True, quality=20)


def main(argv):
    print("starting batch img processing. ")

    # Read in command-line parameters
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--in", action="store", required=True, dest="indir", help="image input directory")

    parser.add_argument("-o", "--out", action="store", required=True, dest="out", help="image output directory")

    parser.add_argument("-t", "--text", action="store", required=True, dest="text", help="text to render")
    
    parser.add_argument("-f", "--font", action="store", required=True, dest="font", help="ttf file to use")
    
    
    args = parser.parse_args()

    try:
        os.makedirs(args.out)
    except OSError:
        pass

    all_files = utils.find_files(args.indir)
    for file_path in all_files:
        # scale_image(file_path, int(args.value), args.out)
        # print(file_path)
        text_overlay(file_path, args.text, args.font, args.out)
        


if __name__ == "__main__":
    main(sys.argv[1:])