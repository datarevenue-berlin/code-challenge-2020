#!/usr/bin/env bash
if test -z "$var"
then
      echo "Usage ./build-task-images.sh VERSION"
      echo "Version was passed!"
      exit 1
fi

VERSION=$1
docker build -t code-challenge/download-data:$VERSION download_data
docker build -t code-challenge/make-dataset:$VERSION make_dataset
