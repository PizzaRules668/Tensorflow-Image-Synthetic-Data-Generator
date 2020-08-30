# Tensorflow Image Synthetic Data Generator
## Setup
Download the make.py script and put it in your working directory.
Make a text file with links to all of the images you would like to download.
I used [Fatkun Batch Download Image (Chrome Extension)](https://chrome.google.com/webstore/detail/fatkun-batch-download-ima/nnjjahlikiabnchcpehcpkdeckfgnohf) and saved it to a text file
## Running
``` python
arguments:
  -h, --help  show this help message and exit
  -b B        Path for the background images
  -i I        Image you would like to detect
  -t T        Where the Images will go
  -o O        Objects name
  -d D        Download Images
  -l L        Link to download the images
```
Example
``` python
python make.py -b background/ -i myimg.png -t images/ -o Myobject -d True -l link.txt
```