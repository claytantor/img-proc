import sys, os
import os.path
from os import path
import json
import argparse
import cutils
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


def slice_img(slice_img_path, out_dir, image_number, id_list, cols=2, rows=2, tile_size=1024, ext="png"):

    lookup = {
        'png':'PNG',
        'jpg':"JPEG"
    }

    pil_image = utils.open_image(slice_img_path)
    print(pil_image.size)

    page = 0
    index_id = 0
    for r_val in range(0, rows):
        for c_val in range(0, cols):

            # get the id
            id_index_offset = image_number*rows*cols+index_id
            id_uuid = id_list[id_index_offset]


            print('{} row:{} col:{} id:{}'.format(slice_img_path, r_val, c_val, id_uuid))

            # Setting the points for cropped image 
            left = c_val * tile_size
            top = r_val * tile_size
            right = (c_val+1) * tile_size
            bottom = (r_val+1) * tile_size
            box = (left, top, right, bottom)
            # print(box)
            
            # Cropped image of above dimension 
            # (It will not change orginal image) 
            im1 = pil_image.crop(box)
            out_img = '{}/{}.{}'.format(out_dir, id_uuid, ext)  
            im1.save(out_img)

            index_id+=1



def generate_ids(count=1000):
    ids = []
    for i in range(0,count):
        ids.append(str(uuid.uuid4()))
    return ids



# ======================================  
def main(argv):
    print("starting batch img processing. ")

    # Read in command-line parameters
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--in", action="store", required=True, dest="indir", help="image input directory")

    parser.add_argument("-o", "--out", action="store", required=True, dest="out", help="image output directory")

    parser.add_argument("-c", "--cols", action="store", required=True, dest="cols", help="column slices")

    parser.add_argument("-r", "--rows", action="store", required=True, dest="rows", help="row slices")

    parser.add_argument("-s", "--size", action="store", required=True, dest="size", help="tile size")

    parser.add_argument("-e", "--ext", action="store", required=False, default='png', dest="ext", help="image type")


    args = parser.parse_args()

    try:
        os.makedirs(args.out)
    except OSError:
        pass


    id_list=[]
    # look to see if there is an id list in the output dir
    ids_file = '{}/ids.json'.format(args.out)
    if path.exists(ids_file) :
        # load id_list as json file
        with open(ids_file) as f:
            id_list = json.load(f)
        
    else:
        # create id_list
        id_list = generate_ids(count=300)

        with open(ids_file, 'w') as json_file:
            json.dump(id_list, json_file)

    print(args.indir)
    all_files = utils.find_files(args.indir, pattern="*.{}".format(args.ext))
    print(all_files)
    image_number = 0
    for file_path in all_files:
        slice_img(file_path, args.out, image_number, id_list, int(args.cols), int(args.rows), tile_size=int(args.size))
        image_number+=1
        

if __name__ == "__main__":
    main(sys.argv[1:])