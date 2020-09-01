# Tensorflow Image Synthetic Data Generator
## Setup
Download the make.py script and put it in your working directory.
<br/>Make a text file with links to all of the images you would like to download.
<br/>I used [Fatkun Batch Download Image (Chrome Extension)](https://chrome.google.com/webstore/detail/fatkun-batch-download-ima/nnjjahlikiabnchcpehcpkdeckfgnohf) and saved it to a text file
## Running
``` python
arguments:
  -h, --help  show this help message and exit
  -b B        Path for the background images
  -i I        Image you would like to detect
  -t T        Training dir
  -r R        Testing dir
  -o O        Objects name
  -l L        Text file that has links to all of the images you would like to download
  -d D        Download Images
  -n N        Number of times each background image will be used
  -p P        Percent of images in train dir
```
Example
``` python
python make.py -b img/ -i rocket.png -t images/train/ -r images/test/ -o Rocket -l links.txt -d True -n 2
```