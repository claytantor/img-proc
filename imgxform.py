import sys, os
import argparse
import utils


def scale_image(image_path, value, out_dir):

    # print(image_path)
    im = utils.open_image(image_path)
    im.seek(0)

    img_path_parts = image_path.split('/')

    new_hw = (int(im.width*(value/100.0)), int(im.height*(value/100.0)))
    # print(new_hw)
    
    out_img = im.resize(new_hw)
    out_img_path = '{}/{}'.format(out_dir, img_path_parts[-1])
    print(out_img_path)
    out_img.save(out_img_path, "PNG", optimize=True, quality=20)

# ======================================  
def main(argv):
    print("starting batch img processing. ")

    # Read in command-line parameters
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--in", action="store", required=True, dest="indir", help="image input directory")

    parser.add_argument("-o", "--out", action="store", required=True, dest="out", help="image output directory")

    parser.add_argument("-x", "--xform", action="store", required=True, dest="xform", help="scale, rotate")
    
    parser.add_argument("-v", "--value", action="store", required=True, dest="value", help="value to use for transformation")
    

    args = parser.parse_args()

    try:
        os.makedirs(args.out)
    except OSError:
        pass

    all_files = utils.find_files(args.indir)
    for file_path in all_files:
        scale_image(file_path, int(args.value), args.out)
        


if __name__ == "__main__":
    main(sys.argv[1:])