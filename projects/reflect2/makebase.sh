BASE_DIR=/home/clay/data/projects/nifty
SOURCE_DIR=$BASE_DIR/all
base_name=$1
TARGET_DIR="${BASE_DIR}/${2}"
PROJECT_DIR=$(pwd)/projects/reflect2
TEXT_DIR=/home/clay/data/projects/nifty/all/txt_reflect2_2

mkdir -p $TARGET_DIR

XF_SCALE=800

# the base processing
# python imgcopy.py -i "$SOURCE_DIR/${base_name}" -o $TARGET_DIR/i_png -s jpg -t png
# python imgslice.py -i $TARGET_DIR/i_png -o $TARGET_DIR/i_png_split -c 16 -r 1 -s 128
# python imgxform.py -i $TARGET_DIR/i_png_split -o $TARGET_DIR/i_png_scaled -x scale -v $XF_SCALE

# python imgfilter.py -i $TARGET_DIR/i_png_scaled -o $TARGET_DIR/i_grey -f rgb2grey
# python imgfilter.py -i $TARGET_DIR/i_grey -o $TARGET_DIR/i_grey_contrast -f local_contrast_enhancement

# python imgfilter.py -i $TARGET_DIR/i_grey_contrast -o $TARGET_DIR/i_g_rgb -f grey2rgb
# python $PROJECT_DIR/imgcolorize.py -i $TARGET_DIR/i_g_rgb -o $TARGET_DIR/i_colorize -c $PROJECT_DIR/colors.xml
# python imgfilter.py -i $TARGET_DIR/i_colorize -o $TARGET_DIR/i_rgb_contrast -f rescale_intensity

# # # # # # now text overlay /home/clay/data/projects/nifty/target_r2_1/reflect02_colorize
# python -m projects.reflect2 -i $TARGET_DIR/i_rgb_contrast -o $TARGET_DIR/i_final_png -t $TEXT_DIR -c $TARGET_DIR/i_colorize/colorized_images.json -f $SOURCE_DIR/font/OCRA.ttf

python img2svg.py -i $TARGET_DIR/i_final_png -o $TARGET_DIR/i_final_svg