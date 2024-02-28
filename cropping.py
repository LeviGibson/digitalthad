from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cv2
from scipy import ndimage
import math
import time
import statistics

def scan(img, kernel):
    method = cv2.TM_CCOEFF
    result = cv2.matchTemplate(img, kernel, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    return max_loc

def rotate(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.

    The angle should be given in radians.
    """
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy

# Crop to scorecard
def scan_for_references(img):
    #convert image to np array
    img = np.array(img)
    
    #loading in referenaces (kernels)
    ref1 = np.array(Image.open("ref1.jpg"))
    ref2 = np.array(Image.open("ref2.jpg"))
    
    ref1loc = scan(img, ref1)
    ref2loc = scan(img, ref2)
    
    # print(ref1loc, ref2loc)
    img = img[ref1loc[1]-1200:ref1loc[1]+200, ref1loc[0]-50:ref1loc[0]+1100]
    
    # plt.imshow(img)
    # plt.show()
    # pass
    return img

def fix_rect_rotation(rects):
    for i, rect in enumerate(rects):
        rect = list(rect)
        if abs(abs(rect[2]) - 90) < abs(rect[2]):
            rect[1] = (rect[1][1], rect[1][0])
            if rect[2] < 0:
                rect[2] += 90
            else:
                rect[2] -= 90
                
        if abs(abs(rect[2]) - 90) < abs(rect[2]):
            rect[1] = (rect[1][1], rect[1][0])
            if rect[2] < 0:
                rect[2] += 90
            else:
                rect[2] -= 90
                
        rects[i] = rect
    return rects

def average_rect_rotation(rects):
    arr = []
    for i in rects:
        arr.append(i[2])
    
    return statistics.median(arr)
    
    # average = statistics.median(arr)
    # print(arr)
    # rot = 0
    # samples = 0
    # for i in rects:
    #     if (abs(i[2] - average) / average) > .1:
    #         continue
    #     rot += i[2]
    #     samples+=1
    
    # return rot/samples

def rotate_image(image, rects):
    # cv2.drawContours(image, np.int0(cv2.boxPoints(rects)), -1, (0,255,0), 3)
    
    rects = fix_rect_rotation(rects)
    rotation = average_rect_rotation(rects)
    
    for i, r in enumerate(rects):
        r[0] = rotate((image.shape[1]/2, image.shape[0]/2), r[0], math.radians(-rotation))
        r[2] = 0
        rects[i] = r
    
    image = ndimage.rotate(image, rotation, reshape=False)
    
    
    return image, rects

def find_lines(image):
    image = np.array(image)
    edges = cv2.Canny(image, 100, 200, apertureSize=3)
    
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    hierarchy = hierarchy[0]
    
    # image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    boxes = []
    
    for i, contour in enumerate(contours):
        rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        
        if (rect[1][0] * rect[1][1]) < 70000:
            continue
        # if(hierarchy[i][2] < 0 and hierarchy[i][3] < 0):
        #     continue
        
        cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
        
        # if (abs(cv2.contourArea(contour) - (rect[1][0] * rect[1][1])) / cv2.contourArea(contour)) > .15:
        #     continue
        boxes.append(rect)
        
    # crop.display(image)
    
    # draw_rects(image, boxes, color=(255,0,0))
    
    if len(boxes) == 0:
        print("No scorecard detected")
        return 1, None, None
    image, boxes = rotate_image(image, boxes)
    
    # if len(boxes) != 8:
    #     print("Incorrect Number of Boxes {}", len(boxes))
    #     return 1, None, None
    
    return image

def crop_to_bounds(img):
    img = np.array(img)
    
    #loading in referenaces (kernels)
    ref1 = np.array(Image.open("scr.jpg"))
    ref2 = np.array(Image.open("comp.jpg"))
    
    ref1loc = scan(img, ref1)
    ref2loc = scan(img, ref2)
    
    # print(ref1loc, ref2loc)
    
    plt.imshow(img)
    plt.show()
    pass

def center(imagedsds):

    imagedsds = find_lines(imagedsds)
    imagedsds = scan_for_references(imagedsds)
    return imagedsds

def split_boxes(img):
    split = {
        "event": [], 
        "round": [], 
        "id": [], 
        "name": [], 
        "scr": [], 
        "time": [], 
        "judge": [], 
        "comp": []
    }
    
    split['event'].append(img[195:263, 132:806])
    split['round'].append(img[195:263, 813:942])
    split['id'].append(img[335:403, 132:278])
    split['name'].append(img[335:403, 285:1072])
    
    split['scr'].append(img[514:620,132:259])
    split['scr'].append(img[653:759,132:259])
    split['scr'].append(img[793:899,132:259])
    split['scr'].append(img[932:1038,132:259])
    split['scr'].append(img[1071:1177,132:259])
    split['scr'].append(img[1256:1362,132:259])
    
    split['time'].append(img[514:620,265:805])
    split['time'].append(img[653:759,265:805])
    split['time'].append(img[793:899,265:805])
    split['time'].append(img[932:1038,265:805])
    split['time'].append(img[1071:1177,265:805])
    split['time'].append(img[1256:1362,265:805])
    
    split['judge'].append(img[514:620,811:939])
    split['judge'].append(img[653:759,811:939])
    split['judge'].append(img[793:899,811:939])
    split['judge'].append(img[932:1038,811:939])
    split['judge'].append(img[1071:1177,811:939])
    split['judge'].append(img[1256:1362,811:939])
    
    split['comp'].append(img[514:620,945:1072])
    split['comp'].append(img[653:759,945:1072])
    split['comp'].append(img[793:899,945:1072])
    split['comp'].append(img[932:1038,945:1072])
    split['comp'].append(img[1071:1177,945:1072])
    split['comp'].append(img[1256:1362,811:939])
    
    # for id, i in enumerate(split['comp']):
    #     plt.imsave(str(id)+".png", i)
    
    # plt.imshow(split['name'][0])
    # plt.imshow(img)
    # plt.show()
    
    return split

def crop(i):

    imgff = i
    imgff = center(imgff)
    sp = split_boxes(imgff)
    return imgff, sp
    


# plt.imshow(imgff)
# plt.show()


# plt.imshow(imagedsds)
# plt.show()
