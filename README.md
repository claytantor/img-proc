# img-proc

## building the container
docker build -t img-proc:latest .

## running from the container
docker run -it --rm -v $(pwd)/workspace:/workspace img-proc:latest python imgfilter.py -i /workspace/in -o /workspace/out

docker run -it --rm -v $(pwd)/workspace:/workspace img-proc:latest python imgslice.py -i /workspace/out -o /workspace/sliced


