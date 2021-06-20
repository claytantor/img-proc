BASE_DIR=/home/clay/data/projects/nifty
PROJECT_DIR="${BASE_DIR}/${1}"

i_id=$2

TARGET_DIR="${BASE_DIR}/${i_id}"


# SOURCE_DIR=$BASE_DIR/all
# base_name=$1
# TARGET_DIR="${BASE_DIR}/${2}"
# PROJECT_DIR=$(pwd)/projects/reflect2
# TEXT_DIR=/home/clay/data/projects/nifty/all/txt_reflect2_2

mkdir -p $TARGET_DIR

cp ${PROJECT_DIR}/i_colorize/${i_id}.png ${TARGET_DIR}/${i_id}_colorize.png
cp ${PROJECT_DIR}/i_rgb_contrast/${i_id}.png ${TARGET_DIR}/${i_id}_rgb_contrast.png
cp ${PROJECT_DIR}/i_png_scaled/${i_id}*.png ${TARGET_DIR}/${i_id}_png_scaled.png
cp ${PROJECT_DIR}/i_grey_contrast/${i_id}*.png ${TARGET_DIR}/${i_id}_grey_contrast.png
cp ${PROJECT_DIR}/i_txt/${i_id}*.txt ${TARGET_DIR}/${i_id}.txt
cp ${PROJECT_DIR}/i_final_png/${i_id}*.png ${TARGET_DIR}/${i_id}_final_png.png
cp ${PROJECT_DIR}/i_final_svg/${i_id}*.svg ${TARGET_DIR}/${i_id}_final.svg