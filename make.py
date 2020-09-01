import cv2
import glob
import os
import urllib.request
import random
import argparse
import numpy as np

def load(totalimg):
    num = 0
    count = 1
    totalimg = totalimg * args.n

    for a in range(0, args.n):
        for file in glob.glob(args.b + "*.jpg"):
            print(file)
            img = cv2.imread(file, cv2.IMREAD_UNCHANGED)

            rocket = cv2.imread(args.i, cv2.IMREAD_UNCHANGED)
            scale = random.randint(20, 50)
            rocket = resize(rocket, scale)

            pwd = os.popen("cd").read()

            try:
                pos = (random.randint(0, img.shape[1]), random.randint(0, img.shape[0]))
                print("At: X:" + str(pos[0]) + " Y:" + str(pos[1]) + " Scale: " + str(scale))

                insert(img, rocket[:, :, 0:3], pos, rocket[:, :, 3] / 255.0)
                
                if not os.path.exists(args.b):
                    os.makedirs(args.b) 

                if count / totalimg * 100 <= 20.0:
                    imagepath = args.t + str(count) + ".jpg"
                    xmlpath = args.t + "/" + str(count) + ".xml"
                elif count / totalimg * 100 >= 20.0:
                    imagepath = args.r + str(count) + ".jpg"
                    xmlpath = args.r + "/" + str(count) + ".xml"

                print(str(round((count / totalimg) * 100, 5)) + "%")

                count += 1

                print(str(imagepath))

                write(xmlpath, imagepath, pos, img, rocket, scale)
                cv2.imwrite(imagepath, img)
            except Exception as e:
                print("Failed to open " + file)
                print(e)
        
def download(link):
    file = open(args.l, "r")
    links = file.readlines()
    pic_num = 1
        
    if not os.path.exists(args.b):
        os.makedirs(args.b)
            
    for i in links:
        try:
            print(i)
            urllib.request.urlretrieve(i, args.b + str(pic_num) + ".jpg")
            pic_num += 1
                
        except Exception as e:
            print(str(e))

def resize(img, scale):
    width = int(img.shape[1] * scale / 100)
    height = int(img.shape[0] * scale / 100)
    dim = (width, height)

    return cv2.resize(img, dim, interpolation = cv2.INTER_NEAREST)

def insert(img, img_overlay, pos, alpha_mask):
    x, y = pos

    y1, y2 = max(0, y), min(img.shape[0], y + img_overlay.shape[0])
    x1, x2 = max(0, x), min(img.shape[1], x + img_overlay.shape[1])

    y1o, y2o = max(0, -y), min(img_overlay.shape[0], img.shape[0] - y)
    x1o, x2o = max(0, -x), min(img_overlay.shape[1], img.shape[1] - x)

    if y1 >= y2 or x1 >= x2 or y1o >= y2o or x1o >= x2o:
        return

    channels = img.shape[2]

    alpha = alpha_mask[y1o:y2o, x1o:x2o]
    alpha_inv = 1.0 - alpha

    for c in range(channels):
        try:
            img[y1:y2, x1:x2, c] = (alpha * img_overlay[y1o:y2o, x1o:x2o, c] + alpha_inv * img[y1:y2, x1:x2, c])
        except Exception as e:
            print(str(e))

def write(filename, folder, pos, background, front, scale):
    x, y = pos
    file = open(filename, "w")
    file.write('''<annotation>
    <folder>{}</folder>
    <filename>{}</filename>
    <path>{}</path>
    <source>
        <database>Unknown</database>
	</source>
	<size>
		<width>{}</width>
		<height>{}</height>
		<depth>{}</depth>
	</size>
	<segmented>0</segmented>
	<object>
		<name>{}</name>
		<pose>Unspecified</pose>
		<truncated>0</truncated>
		<difficult>0</difficult>
		<bndbox>
			<xmin>{}</xmin>
			<ymin>{}</ymin>
			<xmax>{}</xmax>
			<ymax>{}</ymax>
		</bndbox>
	</object>
</annotation>'''.format(folder, 
                        filename, 
                        folder, 
                        str(background.shape[1]), 
                        str(background.shape[0]), 
                        str(background.shape[2]), 
                        args.o, 
                        str(x), 
                        str(y), 
                        str(x + front.shape[1]), 
                        str(y + front.shape[0])))
    file.close()

def countimg():
    lcount = 0
    for file in glob.glob(args.b + "*.jpg"):
        lcount += 1

    return lcount

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Makes training data for tensorflow')
    parser.add_argument("-b", type=str, required=True, help="Path for the background images")
    parser.add_argument("-i", type=str, required=True, help="Image you would like to detect")
    parser.add_argument("-t", type=str, required=True, help="Training dir")
    parser.add_argument("-r", type=str, required=True, help="Testing dir")
    parser.add_argument("-o", type=str, required=True, help="Objects name")

    parser.add_argument("-d", type=bool, help="Download Images")
    parser.add_argument("-l", type=str, help="Text file that has links to all of the images you would like to download")

    parser.add_argument("-n", type=int, default=1, help="Number of times each background image will be used")

    args = parser.parse_args()

    if args.d:
        download(args.l)
        print("Delete all of the image you dont want to use")
        print("Also Delete images that are small")
        input()
    
    totalimg = countimg()

    load(totalimg)