# Tensorflow Image Synthetic Data Generator
## Setup
Download the make.py script and put it in your working directory.
<br/>Make a text file with links to all of the images you would like to download.
<br/>I used [Fatkun Batch Download Image (Chrome Extension)](https://chrome.google.com/webstore/detail/fatkun-batch-download-ima/nnjjahlikiabnchcpehcpkdeckfgnohf) and put all link in a text file
## Running
```
optional arguments:
  -h, --help  show this help message and exit
  -b B        Path for the background images
  -i I        The dir that has all of the object you would like to detect
  -t T        Training dir
  -r R        Testing dir
  -o O        Objects name
  -l L        Text file that has links to all of the images you would like to download
  -d D        Download Images
  -n N        Number of times each background image will be used
  -p P        Percent of images in train dir
  -c C        Convert xml to csv
  -f F        Dir you want the csv files to be made Example
```
### Example Command
``` bash
python make.py -b img/ -i rocket/ -t images/train/ -r images/test/ -o Rocket -l links.txt -d True -c True -f data/ -n 2
```