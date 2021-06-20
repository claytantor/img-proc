# FROM python:3.8.2
FROM nvcr.io/nvidia/pytorch:20.06-py3

WORKDIR /usr/src/app

# USER root
RUN apt-get update -y

RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8003

# USER imgproc
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8003"]


