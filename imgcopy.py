import glob
import sys, os
import argparse
import uuid
import shutil
from PIL import Image

def find_files(dir_name, pattern="*.png", recursive=True):
    # Using '*' pattern 
    all_files = [] 
    for name in glob.glob('{}/**/{}'.format(dir_name, pattern), recursive=True): 
        all_files.append(name)
    return all_files 

def copy_file(from_file, to_file):
    pass


# ======================================  
def main(argv):
    print("starting batch img copy. ")

    # Read in command-line parameters
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--in", action="store", required=True, dest="indir", help="image input directory")
    
    parser.add_argument("-o", "--out", action="store", required=True, dest="out", help="image output directory")

    parser.add_argument("-s", "--source", action="store", required=True, dest="source", help="image source format")
    
    parser.add_argument("-t", "--target", action="store", required=True, dest="target", help="image target format")
    
    args = parser.parse_args()

    try:
        os.makedirs(args.out)
    except OSError:
        pass

    all_files = find_files(args.indir, pattern="*.{}".format(args.source))
    for file_path in all_files:
        im = Image.open(file_path)  
        parts = file_path.split('/')
        out_img = '{}/{}.{}'.format(args.out,str(parts[-1:][0][:-4]), args.target)  
        im.save(out_img)
        print('copy src:{} dest:{}'.format(file_path,out_img))
        

if __name__ == "__main__":
    main(sys.argv[1:])