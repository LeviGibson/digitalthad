import easyocr
import matplotlib.pyplot as plt
from PIL import Image
import random
import jellyfish
import os
import numpy as np
import glob
import skimage
import shutil
import cv2
from operator import itemgetter
from tensorflow import keras


___ = None

reader = easyocr.Reader(["en"])

#ChatGPT
def add_white_border(image, border_size, zero=False):
    """
    Add a white border around the image.

    Parameters:
    - image: NumPy array representing the input image.
    - border_size: Size of the border to be added around the image.

    Returns:
    - bordered_image: NumPy array representing the image with a white border.
    """
    # Determine the dimensions of the new image
    new_height = image.shape[0] + 2 * border_size[0]
    new_width = image.shape[1] + 2 * border_size[1]

    # Create a new array filled with white pixels
    bordered_image = np.ones((new_height, new_width, 3), dtype=np.uint8) * 255
    if zero:
        bordered_image *= 0

    # Calculate the position to place the original image in the new array
    y_offset = (new_height - image.shape[0]) // 2
    x_offset = (new_width - image.shape[1]) // 2

    # Place the original image in the center of the new array
    bordered_image[y_offset:y_offset + image.shape[0], x_offset:x_offset + image.shape[1]] = image

    return bordered_image

#a product of chatgpt
def add_border(image_array, border_width=6):
    # Ensure the image is in uint8 format
    image_array = image_array.astype(float)

    # Get the height and width of the original image
    height, width = image_array.shape

    # Create a new array filled with zeros (assuming black border)
    bordered_image = np.zeros((height, width), dtype=float)

    # Copy the original image into the center of the new array
    bordered_image[border_width:height-border_width, border_width:width-border_width] = image_array[border_width:height-border_width, border_width:width-border_width]

    return bordered_image

# header_number_examples = []
# for i in range(10):
#     diget = np.array(Image.open("header_numbers/{}.png".format(i))).astype(float)

#     diget /= 255
#     diget *= 2
#     diget -= 1
    
#     diget = diget[:,:,1]
#     header_number_examples.append(diget)
#     # plt.imshow(diget)
#     # plt.show()

# def match_header_diget(diget):
#     maxscore = -100000000
#     maxnum = None
#     for i in range(10):
#         score = np.mean(np.array(diget) * header_number_examples[i])
#         if score > maxscore:
#             maxscore = score
#             maxnum = i
            
#     return maxnum

HEADER_DIGET_MODEL = keras.models.load_model("header_numbers/model/")

def match_header_diget(diget):
    diget = np.array(diget)
    diget = diget.astype(float) / 255
    diget = diget.flatten().reshape((1,-1,1))
    prediction = HEADER_DIGET_MODEL.predict([diget]).flatten()
    
    maxval = -10000000000
    maxnum = None
    for i in range(10):
        if prediction[i] > maxval:
            maxval = prediction[i]
            maxnum = i
    
    return maxnum
    

#Please don't read this function
#You won't enjoy it
def read_header_number(obj):
    original = obj.copy()
    
    obj = cv2.cvtColor(obj, cv2.COLOR_BGR2GRAY)
    ret, obj = cv2.threshold(obj, 100, 255, cv2.THRESH_BINARY_INV)
    contours, hi = cv2.findContours(obj, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.drawContours(original, contours, -1, (0,255,0), 3)
    # print(contours[0])
    # print(contours[0][:,:,0])
    
    nums = []
    
    for c in contours:
        left = min(c[:,:,0])[0]
        right = max(c[:,:,0])[0]
        top = min(c[:,:,1])[0]
        bottom = max(c[:,:,1])[0]
        
        height = (bottom - top)
        width = (right - left)
        if width % 2 != 0:
            right+=1
        if height % 2 != 0:
            bottom+=1
        height = (bottom - top)
        width = (right - left)
        
        if height < 5 or width < 5:
            continue
        
        if abs(33 - height) > 10:
            # n = random.randint(0,100000000)
            # print("Throwing out diget due to height {} filename {}".format(height, n))
            # if (height > 10 and width > 0):
                # plt.imsave("tmp/{}.png".format(n), original[top:bottom,left:right])
            continue
        if abs(17 - width) > 18:
            # print("Throwing out diget due to width {}".format(width))
            continue
        
        center = (left+right)//2
        diget = (original[top:bottom,left:right])
        o = diget.copy()
        
        diget = add_white_border(diget, (((60)-height)//2, ((46)-width)//2))
        
        diget = cv2.cvtColor(diget, cv2.COLOR_BGR2GRAY)
        ret, diget = cv2.threshold(diget, 100, 255, cv2.THRESH_BINARY_INV)
        
        # name = random.randint(0, 1000000)
        # plt.imsave("header_numbers/{}.png".format(name), diget, cmap='gray')
        # plt.imsave("header_numbers/original/{}.png".format(name), o, cmap='gray')
        
        # print(match_header_diget(diget))
        # plt.imshow(diget)
        # plt.show()
        
        nums.append((diget, center))
    
    nums = list(sorted(nums, key=itemgetter(1)))
    numstring = ""
    for n in nums:
        numstring += str(match_header_diget(n[0]))
        
    # plt.imshow(np.array(original))
    # plt.show()
    return (numstring)
    pass

def read_printed_header(obj, number=True):
    if number:
        return read_header_number(obj)
    
    global ___
    
    obj = skimage.color.rgb2gray(obj)
    obj = np.where(obj<.5, 1, 0)
    obj = add_border(obj)
    ___ = obj
    
    # plt.imshow(obj)
    # plt.show()
    
    r = random.randint(0, 100000000000)
    fname = "./tmp/IMG_{}.png".format(r)
    
    plt.imsave(fname, obj)
    output = reader.readtext(fname)
    
    maxval = -1000
    maxthing = None
    for i in output:
        if i[-1] > maxval:
            maxval = i[-1]
            maxthing = i[-2]
            
    os.remove(fname)
    return maxthing

# def tesseract_read_round(obj):
#     obj = skimage.color.rgb2gray(obj)
#     obj = np.where(obj<.5, 1, 0)
#     obj = add_border(obj)
#     # ___ = obj
#     # plt.imshow(obj)
#     # plt.show()
    
#     r = random.randint(0, 100000000000)
#     fname = "./tmp/IMG_{}.png".format(r)
    
#     plt.imsave(fname, obj)
#     output = pytesseract.image_to_string(fname, config='-c tessedit_char_whitelist=1234 --psm 10')
    
#     return output

def read_id(obj, round=False):
    r = (read_printed_header(obj))
    # keras_read_number(obj)
    try:
        r = int(r)
    except:
        plt.imsave("ref.png", obj)
        return 1
        return int(input("Image not readable. Please enter the number in the image ref.png:"))
    #7 often gets mixed up with 1 by ocr
    if r == 7 and round:r = 1
    return r

# eventIds = {
#     "2x2x2 Cube":"222",
#     "3x3x3 Cube":"333",
#     "3x3x3 Blindfolded":"333bf",
#     "3x3x3 One-Handed":"333oh",
#     "4x4x4 Cube":	"444",
#     "4x4x4 Blindfolded":	"444bf",
#     "5x5x5 Cube":	"555",
#     "5x5x5 Blindfolded":	"555bf",
#     "6x6x6 Cube":	"666",
#     "7x7x7 Cube":	"777",
#     "Clock":	"clock",
#     "Megaminx":	"minx",
#     "Pyraminx":	"pyram",
#     "Skewb":	"skewb",
#     "Square-1":	"sq1"
# }

eventNames = ["2x2x2 Cube", "3x3x3 Cube", "3x3x3 Blindfolded", "3x3x3 One-Handed", "4x4x4 Cube", "4x4x4 Blindfolded", "5x5x5 Cube", "5x5x5 Blindfolded", "6x6x6 Cube", "7x7x7 Cube", "Clock", "Megaminx", "Pyraminx", "Skewb", "Square-1"]

eventIds = ["222", "333", "333bf", "333oh", "444", "444bf", "555", "555bf", "666", "777", "clock", "minx", "pyram", "skewb", "sq1"]

def read_event(obj):
    text = read_printed_header(obj, number=False)
    
    maxVal = -10000
    maxObj = None
    for i in range(len(eventIds)):
        val = jellyfish.jaro_similarity(text, eventNames[i])
        if val > maxVal:
            maxVal = val
            maxObj = eventIds[i]
    
    return maxObj



if __name__ == '__main__':
    g = glob.glob("./header_numbers/*.png")
    for fname in g:
        img = np.array(Image.open(fname)).astype(float)
        img /= 255
        img = img[:,:,1]
        match = match_header_diget(img)
        ran = random.randint(0,10000000000)
        shutil.move(fname, "./header_numbers/{}/{}.png".format(match, ran))
