import sys, os
import argparse
import utils
import image_slicer


def slice_img(slice_img_path, out_dir, cols=2, rows=2):
    pil_image = utils.open_image(slice_img_path)
    tiles = image_slicer.slice(slice_img_path, int(cols*rows), save=False)
    # image_slicer.save_tiles(tiles)
    slice_img_path_parts = slice_img_path.split('/')
    # return
    index = 0
    for tile in tiles:
        slice_name = slice_img_path_parts[-1].replace('.png','_{}.png'.format(index))
        out_img = '{}/{}'.format(out_dir, slice_name)
        tile.image.save(out_img, "PNG")
        print(out_img, tile.image.format, "%d w %d h" % tile.image.size, tile.image.mode)
        index += 1


# ======================================  
def main(argv):
    print("starting batch img processing. ")

    # Read in command-line parameters
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--in", action="store", required=True, dest="indir", help="image input directory")

    parser.add_argument("-o", "--out", action="store", required=True, dest="out", help="image output directory")

    parser.add_argument("-c", "--cols", action="store", required=True, dest="cols", help="column slices")

    parser.add_argument("-r", "--rows", action="store", required=True, dest="rows", help="row slices")


    args = parser.parse_args()

    try:
        os.makedirs(args.out)
    except OSError:
        pass

    all_files = utils.find_files(args.indir)
    for file_path in all_files:
        slice_img(file_path, args.out, int(args.cols), int(args.rows))
        


if __name__ == "__main__":
    main(sys.argv[1:])