#!/usr/bin/env bash
if test -z "$1"
then
      echo "Usage ./build-task-images.sh VERSION"
      echo "No version was passed! Please pass a version to the script e.g. 0.1"
      exit 1
fi

VERSION=$1
docker build -t code-challenge/download-data:$VERSION download_data
docker build -t code-challenge/make-dataset:$VERSION make_dataset
docker build -t code-challenge/train-models:$VERSION train_models
docker build -t code-challenge/evaluate:$VERSION evaluate