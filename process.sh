rm -rvf /Users/claytongraham/data/projects/nifty/faces/reflect01_colorize
rm -rvf /Users/claytongraham/data/projects/nifty/faces/reflect01_grey
#rm -rvf /Users/claytongraham/data/projects/nifty/faces/reflect01_png_split
#rm -rvf /Users/claytongraham/data/projects/nifty/faces/reflect01_png_scaled
#rm -rvf /Users/claytongraham/data/projects/nifty/faces/reflect01_png

#python imgcopy.py -i /Users/claytongraham/data/projects/nifty/faces/reflect01_jpg -o /Users/claytongraham/data/projects/nifty/faces/reflect01_png -s jpg -t png

#python imgxform.py -i /Users/claytongraham/data/projects/nifty/faces/reflect01_png -o /Users/claytongraham/data/projects/nifty/faces/reflect01_png_scaled -x scale -v 800

#python imgslice.py -i /Users/claytongraham/data/projects/nifty/faces/reflect01_png_scaled -o /Users/claytongraham/data/projects/nifty/faces/reflect01_png_split -c 16 -r 1 

python imgfilter.py -i /Users/claytongraham/data/projects/nifty/faces/reflect01_png_split -o /Users/claytongraham/data/projects/nifty/faces/reflect01_grey

python imgcolorize.py -i /Users/claytongraham/data/projects/nifty/faces/reflect01_grey -o /Users/claytongraham/data/projects/nifty/faces/reflect01_colorize -c /Users/claytongraham/data/projects/nifty/colors/colors.xml


#/Users/claytongraham/data/projects/nifty/orbs/base150

# python imgfilter.py -i /Users/claytongraham/data/projects/nifty/orbs/base150 -o /Users/claytongraham/data/projects/nifty/orbs/base150_grey
