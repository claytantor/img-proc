# img-proc

## building the container
docker build -t img-proc:latest .

## running from the container
docker run -it --rm -v $(pwd)/workspace:/workspace img-proc:latest python imgfilter.py -i /workspace/in -o /workspace/out

docker run -it --rm -v $(pwd)/workspace:/workspace img-proc:latest python imgslice.py -i /workspace/out -o /workspace/sliced

docker run -it --rm -v $(pwd)/workspace:/workspace img-proc:latest python imgslice.py -r 1 -c 16 -i /workspace/in/gan_reflect01 -o /workspace/sliced -e jpg


## image copy

docker run -it --rm -v $(pwd)/workspace:/workspace img-proc:latest python imgcopy.py -i /workspace/in/mirrors -o /workspace/out/mirrors
