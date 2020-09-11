import cv2
import glob
import os
import urllib.request
import random
import argparse
import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET
import imutils

# Make the Synthetic images
def edit(totalimg):
    num = 0
    imagecount = 0
    count = 1
    totalimg = totalimg * args.n

    for a in range(0, args.n):
        for image in glob.glob(args.i + "*.png"):
            for file in glob.glob(args.b + "*.jpg"):
                print(file)
                img = cv2.imread(file, cv2.IMREAD_UNCHANGED)

                scale = random.randint(20, 50)

                pwd = os.popen("cd").read() + "\\"
                pwd = pwd.replace("\n", "")

                background = cv2.imread(image, cv2.IMREAD_UNCHANGED)
                background = resize(background, scale)
                
                background = cv2.copyMakeBorder(background, 0, 0, int(background.shape[0]/2), int(background.shape[0]/2), cv2.BORDER_CONSTANT)

                try:

                    pos = (random.randint(0, img.shape[1]), random.randint(0, img.shape[0]))
                    angle = random.randint(0, 360)

                    shape = background.shape

                    matrix = cv2.getRotationMatrix2D((background.shape[1]/2, background.shape[0]/2), angle, 1)
                    background = cv2.warpAffine(background, matrix, (background.shape[1], background.shape[0]))

                    print("At: X:" + str(pos[0]) + " Y:" + str(pos[1]) + " Scale: " + str(scale) + " Angle: " + str(angle))

                    insert(img, background[:, :, 0:3], pos, background[:, :, 3] / 255.0)
                    
                    if not os.path.exists(args.b):
                        os.makedirs(args.b) 

                    if count / totalimg * 100 <= args.p:
                        imagepath = args.t + str(count) + ".jpg"
                        xmlpath = args.t + str(count) + ".xml"
                        folder = args.t

                    elif count / totalimg * 100 >= args.p:
                        imagepath = args.r + str(count) + ".jpg"
                        xmlpath = args.r + str(count) + ".xml"
                        folder = args.r

                    folder = folder.split("/")

                    print(str(round((count / totalimg) * 100, 5)) + "%")

                    imagepath = imagepath.replace("/", "\\")
                    xmlpath = xmlpath.replace("/", "\\")

                    print(str(imagepath))

                    modpos, pos = IfToLarge(pos, background, img)

                    write(xmlpath, folder[-2], pos, img, background, scale, pwd, count, modpos)
                    cv2.imwrite(imagepath, img)
                except Exception as e:
                    print("Failed to open " + file)
                    print(e)
                
                count += 1

    imagecount += 1
        
# Make the xml file
def write(filename, folder, pos, background, front, scale, pwd, count, modpos):
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
                        str(count)+".jpg", 
                        pwd + folder, 
                        str(background.shape[1]), 
                        str(background.shape[0]), 
                        str(background.shape[2]), 
                        args.o, 
                        str(x), 
                        str(y), 
                        str(modpos[0]), 
                        str(modpos[1])))
    file.close()

# Check to see if bounding box goes off the image
# If it does it makes the bounding box smaller
def IfToLarge(pos, front, back):
    oldx = pos[0]
    oldy = pos[1]

    x = oldx + front.shape[1]
    y = oldy + front.shape[0]

    while x > back.shape[1]:
        x -= 1

    while y > back.shape[0]:
        y -= 1

    return (x, y), (oldx, oldy)

# Downloads images from text file
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

# Resizes the image
def resize(img, scale):
    width = int(img.shape[1] * scale / 100)
    height = int(img.shape[0] * scale / 100)
    dim = (width, height)

    return cv2.resize(img, dim, interpolation=cv2.INTER_NEAREST)

# Puts the image you would like to put on the backgroud
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

# Counts the total amount of images in you background folder
def countimg():
    lcount = 0
    icount = 0
    for file in glob.glob(args.b + "*.jpg"):
        lcount += 1
    
    for file in glob.glob(args.i + "*.png"):
        icount += 1

    return lcount * icount

# Convert the xml file to csv file
def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df

if __name__ == '__main__':
    # File arguments
    parser = argparse.ArgumentParser(description='Makes training data for tensorflow')
    parser.add_argument("-b", type=str, required=True, help="Path for the background images")
    parser.add_argument("-i", type=str, required=True, help="The dir that has all of the object you would like to detect")
    parser.add_argument("-t", type=str, required=True, help="Training dir")
    parser.add_argument("-r", type=str, required=True, help="Testing dir")
    parser.add_argument("-o", type=str, required=True, help="Objects name")

    parser.add_argument("-l", type=str, help="Text file that has links to all of the images you would like to download")
    parser.add_argument("-d", type=bool, help="Download Images")

    parser.add_argument("-n", type=int, default=1, help="Number of times each background image will be used")
    parser.add_argument("-p", type=float, default=20, help="Percent of images in train dir")

    parser.add_argument("-c", type=bool, default=False, help="Convert xml to csv")
    parser.add_argument("-f", type=str, help="Dir you want the csv files to be made")

    args = parser.parse_args()

    # If you want to download images
    if args.d:
        download(args.l)
        print("Delete all of the image you dont want to use")
        print("Also Delete images that are small")
        #input()

    # Counts the total amount of files
    totalimg = countimg()

    # Make the Synthetic images
    edit(totalimg)

    # If you want to convert xml to csv
    if args.c:
        for folder in [args.t, args.r]:
            filename = folder.split("/")[-2]

            xml_df = xml_to_csv(folder)
            xml_df.to_csv((args.f + filename + '_labels.csv'), index=None)
            print('Successfully converted xml to csv.')