# Reproduction Example

Here we show how to make a reproduction submission. The reproduction of your inference code must be packed as a Docker image. We show how to do this by packing our baseline solution.

## Setup

First, you need to install Docker. Please see the [official instructions](https://docs.docker.com/engine/install/).

## Sample Input

For testing your Docker image, you are encouraged to use the `train_sample` images. Note that during the reproduction, you won't be able to access links to the images, so let's download them by running

```bash
python download_imgs.py
```

## Building an Image

You can use our example of a `dockerfile`. To build it, run
```bash
docker build . --tag wsdm2023 --network=host 
```

## How to Run the Solution

We will run your solution by the following command:
```bash
mkdir output
docker run --rm -it --gpus all --network host -v /ABSOLUTE_PATH_TO/WSDMCup2023/reproduction/data:/mnt/data -v /ABSOLUTE_PATH_TO/reproduction/output:/mnt/output wsdm2023
```

The input file will be stored in `/mnt/data/test.csv` and the input images will be at `/mnt/data/imgs`. Your solution must write a single file to `/mnt/output/answer.csv`.

## Hardware Requirements

We will run your solution on a machine with one Nvidia A100 80 GB GPU, 16 CPU cores, and 200 GB of RAM. Your Docker image must perform the inference in at most 3 hours on this machine. In other words, the `docker run` command must finish in 3 hours.

## Sharing Your Image

You will need to [push your image to Docker Hub](https://docs.docker.com/docker-hub/repos/) and share a link with us.
