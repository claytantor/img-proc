import glob
import sys, os
import argparse
import uuid
import shutil

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

    args = parser.parse_args()

    try:
        os.makedirs(args.out)
    except OSError:
        pass

    all_files = find_files(args.indir, pattern="*.png")
    for file_path in all_files:
        parts = file_path.split('/')
        out_img = '{}/{}.png'.format(args.out,str(uuid.uuid4()))     
        shutil.copy(file_path, out_img)
        print('copy src:{} dest:{}'.format(file_path,out_img))
        

if __name__ == "__main__":
    main(sys.argv[1:])