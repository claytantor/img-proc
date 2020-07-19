import glob
from PIL import Image

def open_image(img_path):
    try:
        with Image.open(img_path) as im:
            # print(img_path, im.format, "%dx%d" % im.size, im.mode)
            im.load()
            return im
    except IOError:
        print('error')
        pass


def find_files(dir_name, pattern="*.png", recursive=True):
    # Using '*' pattern 
    all_files = [] 
    for name in glob.glob('{}/**/{}'.format(dir_name, pattern), recursive=True): 
        all_files.append(name)
    return all_files 