import sys, os
import argparse
import cutils
import textwrap

# import required classes

from PIL import Image, ImageDraw, ImageFont, ImageFilter

# create Image object with the input image
# I = numpy.asarray(Image.open('/Users/claytongraham/data/projects/nifty/colors/AdobeColor-c1.jpeg'))



    


def draw_text_shadow(im, message_text, draw, font, color, shadowcolor, xpos, ypos, offset = 6):

    (x,y) = (xpos,ypos)

    txt = Image.new('RGBA', im.size, (255,255,255,0))
    d = ImageDraw.Draw(txt)    

    d.text((x-offset, y-offset), message_text, font=font, fill=shadowcolor)
    d.text((x+offset, y-offset), message_text, font=font, fill=shadowcolor)
    d.text((x-offset, y+offset), message_text, font=font, fill=shadowcolor)
    d.text((x+offset, y+offset), message_text, font=font, fill=shadowcolor)

    # im = Image.alpha_composite(im, txt)
    return txt


def make_shadow(image, iterations, border, offset, backgroundColour, shadowColour):
    # image: base image to give a drop shadow
    # iterations: number of times to apply the blur filter to the shadow
    # border: border to give the image to leave space for the shadow
    # offset: offset of the shadow as [x,y]
    # backgroundCOlour: colour of the background
    # shadowColour: colour of the drop shadow

    
    #Calculate the size of the shadow's image
    fullWidth  = image.size[0] + abs(offset[0]) + 2*border
    fullHeight = image.size[1] + abs(offset[1]) + 2*border
    
    #Create the shadow's image. Match the parent image's mode.
    shadow = Image.new(image.mode, (fullWidth, fullHeight), backgroundColour)
    
    # Place the shadow, with the required offset
    shadowLeft = border + max(offset[0], 0) #if <0, push the rest of the image right
    shadowTop  = border + max(offset[1], 0) #if <0, push the rest of the image down
    #Paste in the constant colour
    shadow.paste(shadowColour, 
                [shadowLeft, shadowTop,
                 shadowLeft + image.size[0],
                 shadowTop  + image.size[1] ])
    
    # Apply the BLUR filter repeatedly
    for i in range(iterations):
        shadow = shadow.filter(ImageFilter.BLUR)

    # Paste the original image on top of the shadow 
    imgLeft = border - min(offset[0], 0) #if the shadow offset was <0, push right
    imgTop  = border - min(offset[1], 0) #if the shadow offset was <0, push down
    shadow.paste(image, (imgLeft, imgTop))

    return shadow



def draw_textline(im, message_text, draw, font, color, shadowcolor, xpos, ypos, offset = 3):

    (x,y) = (xpos,ypos)

    # thicker border
    draw.text((x-offset, y-offset), message_text, font=font, fill=shadowcolor)
    draw.text((x+offset, y-offset), message_text, font=font, fill=shadowcolor)
    draw.text((x-offset, y+offset), message_text, font=font, fill=shadowcolor)
    draw.text((x+offset, y+offset), message_text, font=font, fill=shadowcolor)

    draw.text((x, y), message_text, fill=color, font=font)


def draw_paragraph(im, p_text, image_draw, ttf_font_path, 
    x_pos, y_pos, title_size=45, justify=False, line_width=25, color = 'rgb(0, 0, 0)', 
    shadowcolor = 'rgb(255, 255, 255)', max_lines=10):

    font_title = ImageFont.truetype(ttf_font_path, size=title_size)

    lines = p_text.split("\n")
    if justify:
        lines = textwrap.wrap(p_text, width=line_width)

    index = 0
    for line in lines[:max_lines]:
        draw_textline(im, line, image_draw, font_title, color, shadowcolor, x_pos, y_pos+(index*title_size), offset=2)
        index += 1


def draw_title(im, title_message_text, draw, ttf_font_path, title_size=45):
    font_title = ImageFont.truetype(ttf_font_path, size=title_size)

    (x, y) = (5, 5)
    color = 'rgb(0, 0, 0)' # black color
    shadowcolor = 'rgb(255, 255, 255)' # white color

    lines = textwrap.wrap(title_message_text, width=20)
    line_height = 45
    index = 0
    for line in lines:
        draw_textline(im, line, draw, font_title, color, shadowcolor, 5, (index*line_height))
        index += 1


def draw_album_name(im, txt_message_text, draw, img, ttf_font_path, txt_size=20):
    font_album = ImageFont.truetype(ttf_font_path, size=txt_size)
    # (x, y) = (img.height-txt_size-5, 5)
    color = 'rgb(0, 0, 0)' # black color
    shadowcolor = 'rgb(255, 255, 255)' # grey color
    draw_textline(im, txt_message_text, draw, font_album, color, shadowcolor, 5, img.height-txt_size-5)


def text_overlay(image_path, title_message_text, ttf_font_path, out_dir, img_name=None):

    # image = Image.open('background.png')
    im = utils.open_image(image_path)

    # initialise the drawing context with
    # the image object as background

    # if the out dir doesnt exist the create it
    try:
        os.makedirs(out_dir)
    except OSError:
        pass

    draw = ImageDraw.Draw(im)
    draw_title(title_message_text, draw, ttf_font_path, title_size=55)
    draw_album_name("@claytantor niftyorb.com", draw, im, ttf_font_path, txt_size=30)

    # save the edited image
    img_path_parts = image_path.split('/')
    if img_name==None:
        img_name = img_path_parts[-1]

    out_img_path = '{}/{}'.format(out_dir, img_name)
    print(out_img_path)
    im.save(out_img_path, "PNG", optimize=True, quality=20)


def main(argv):
    print("starting batch img processing. ")

    # Read in command-line parameters
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--in", action="store", required=True, dest="indir", help="image input directory")

    parser.add_argument("-o", "--out", action="store", required=True, dest="out", help="image output directory")

    parser.add_argument("-t", "--text", action="store", required=True, dest="text", help="text file to render")
    
    parser.add_argument("-f", "--font", action="store", required=True, dest="font", help="ttf file to use")

    parser.add_argument("-n", "--name", action="store", required=False, dest="name", help="name to use")
    
    args = parser.parse_args()

    try:
        os.makedirs(args.out)
    except OSError:
        pass

    # load the text file

    all_files = utils.find_files(args.indir)
    for file_path in all_files:
        # scale_image(file_path, int(args.value), args.out)
        # print(file_path)
        text_overlay(file_path, args.text, args.font, args.out, args.name)
        


if __name__ == "__main__":
    main(sys.argv[1:])