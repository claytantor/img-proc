import sys, os
import argparse
import utils
import image_slicer
from PIL import Image
import uuid

def crop(out_path, input, height, width, k, page, area):
    im = Image.open(input)
    imgwidth, imgheight = im.size
    for i in range(0,imgheight,height):
        for j in range(0,imgwidth,width):
            box = (j, i, j+width, i+height)
            a = im.crop(box)
            try:
                o = a.crop(area)
                o.save(os.path.join(out_path,"PNG","%s" % page,"IMG-%s.png" % k))
            except:
                pass
            k +=1


def slice_img(slice_img_path, out_dir, cols=2, rows=2, tile_size=1024, ext="png"):

    lookup = {
        'png':'PNG',
        'jpg':"JPEG"
    }

    pil_image = utils.open_image(slice_img_path)
    print(pil_image.size)

    page = 0
    for r_val in range(0, rows):
        print(r_val)
        for c_val in range(0, cols):
            print('{} row:{} col:{}'.format(slice_img_path, r_val, c_val))

            # crop(out_dir, slice_img_path, height, width, k, page, area)

            # Setting the points for cropped image 
            left = c_val * tile_size
            top = r_val * tile_size
            right = (c_val+1) * tile_size
            bottom = (r_val+1) * tile_size
            box = (left, top, right, bottom)
            print(box)
            
            # Cropped image of above dimension 
            # (It will not change orginal image) 
            im1 = pil_image.crop(box)
            out_img = '{}/{}.{}'.format(out_dir, str(uuid.uuid4()), ext)  
            im1.save(out_img)



    # tiles = image_slicer.slice(slice_img_path, int(cols*rows), save=False)
    # # image_slicer.save_tiles(tiles)
    # slice_img_path_parts = slice_img_path.split('/')
    # # return
    # index = 0
    # for tile in tiles:
    #     slice_name = slice_img_path_parts[-1].replace('.{}'.format(ext),'_{}.{}'.format(index, ext))
    #     out_img = '{}/{}'.format(out_dir, slice_name)
    #     tile.image.save(out_img, lookup[ext])
    #     print(out_img, tile.image.format, "%d w %d h" % tile.image.size, tile.image.mode)
    #     index += 1


# ======================================  
def main(argv):
    print("starting batch img processing. ")

    # Read in command-line parameters
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--in", action="store", required=True, dest="indir", help="image input directory")

    parser.add_argument("-o", "--out", action="store", required=True, dest="out", help="image output directory")

    parser.add_argument("-c", "--cols", action="store", required=True, dest="cols", help="column slices")

    parser.add_argument("-r", "--rows", action="store", required=True, dest="rows", help="row slices")

    parser.add_argument("-e", "--ext", action="store", required=False, default='png', dest="ext", help="image type")


    args = parser.parse_args()

    try:
        os.makedirs(args.out)
    except OSError:
        pass

    print(args.indir)
    all_files = utils.find_files(args.indir, pattern="*.{}".format(args.ext))
    print(all_files)
    for file_path in all_files:
        slice_img(file_path, args.out, int(args.cols), int(args.rows))
        


if __name__ == "__main__":
    main(sys.argv[1:])