BASE_DIR=/home/clay/data/projects/nifty
SOURCE_DIR=$BASE_DIR/all
TARGET_DIR=$BASE_DIR/$1
PROJECT_DIR=$(pwd)/projects
TEXT_DIR=/home/clay/data/github.com/claytantor/textrnn-pytorch/workspace/out/reflect/mar_3_2021

mkdir -p $TARGET_DIR

XF_SCALE=800

# the base processing
python imgcopy.py -i $SOURCE_DIR/reflect01_jpg -o $TARGET_DIR/reflect01_png -s jpg -t png
python imgxform.py -i $TARGET_DIR/reflect01_png -o $TARGET_DIR/reflect01_png_scaled -x scale -v $XF_SCALE
python imgslice.py -i $TARGET_DIR/reflect01_png_scaled -o $TARGET_DIR/reflect01_png_split -c 16 -r 1 
python imgcolorize.py -i $TARGET_DIR/reflect01_png_split -o $TARGET_DIR/reflect01_colorize -c $(pwd)/projects/reflect/colors.xml

# # now text overlay
python -m projects.reflect -i $TARGET_DIR/reflect01_colorize -o $TARGET_DIR/reflect01_txt -t $TEXT_DIR -c $TARGET_DIR/reflect01_colorize/colorized_images.json -f $SOURCE_DIR/font/OCRA.ttf
