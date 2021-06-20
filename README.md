# img-proc

# creating a pyenv
```
pyenv virtualenv 3.8.0 img-proc
pyenv activate img-proc
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## building the container
docker build -t img-proc:latest .

## running from the container
docker run -it --rm -v $(pwd)/workspace:/workspace img-proc:latest python imgfilter.py -i /workspace/in -o /workspace/out

docker run -it --rm -v $(pwd)/workspace:/workspace img-proc:latest python imgslice.py -i /workspace/out -o /workspace/sliced

docker run -it --rm -v $(pwd)/workspace:/workspace img-proc:latest python imgslice.py -r 1 -c 16 -i /workspace/in/gan_reflect01 -o /workspace/sliced -e jpg


## image copy
image copy will copy and format such as change a TIF to a PNG. 

## image colorize
image colorize will use skimage filters to change a file. 

`python imgcolorize.py -i "$IMG_ROOT/reflect01_png_split" -o "$IMG_ROOT/reflect01_colorize" -c "$(pwd)/projects/$PROJECT/colors.xml"`

## image filter
`python imgfilter.py -i /Users/claytongraham/data/projects/nifty/faces/reflect01_png_split -o /Users/claytongraham/data/projects/nifty/faces/reflect01_grey`

## image slice
`python imgslice.py -i /Users/claytongraham/data/projects/nifty/faces/reflect01_png_scaled -o /Users/claytongraham/data/projects/nifty/faces/reflect01_png_split -c 16 -r 1`

# image xform
`python imgxform.py -i /home/clay/data/projects/nifty/all/reflect01_txt -o /home/clay/data/projects/nifty/all/reflect01_thumb -x scale -v 25`

# image text
add text overlays
`python imgtext.py -i /home/clay/data/projects/nifty/all/reflect01_txt -o /home/clay/data/projects/nifty/all/reflect01_thumb -x scale -v 25`


# running project scripts
bash $(pwd)/projects/reflect/makebase.sh target_1

# SCRATCH





python imgxform.py -i /home/clay/data/github.com/claytantor/img-proc/workspace/ghosts_gan/gengan -o /home/clay/data/github.com/claytantor/img-proc/workspace/ghosts_gan/gengan_s -x scale -v 2.775067751


python imgfilter.py -i /home/clay/data/github.com/claytantor/img-proc/workspace/ghosts_gan/gengan_s -o /home/clay/data/github.com/claytantor/img-proc/workspace/ghosts_gan/gengan_g -f rgb2grey



FLASK_APP=app.py APP_CONFIG=app.cfg flask run --host=0.0.0.0 --port=8003



## building the container
```
docker build -t claytantor/loa-img-proc:latest .
```
### from docker
```bash
docker run -p 8003:8003 --gpus all --shm-size=1g --ulimit memlock=-1 \
    -e FLASK_ENV=development -e FLASK_APP=app.py -e APP_CONFIG=app.cfg \
    --ulimit stack=67108864 -it --rm -v $(pwd)/workspace:/workspace \
    claytantor/loa-img-proc:latest
```