#!/bin/bash

which conda

if [ $? -eq 1 ]
then
  echo "conda is not found"
  exit 1
fi

which chromium
if [ $? -eq 1 ]
then
  echo "chromium is not found"
  exit 1
fi

conda create --name scrap --file package-list.txt
conda activate scrap