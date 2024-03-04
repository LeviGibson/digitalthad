import glob
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cropping
import ocr
import wcalive
import cv2
import math

fnames = glob.glob("./raw/*.tiff")
fnames = list(sorted(fnames))

def generate_data_point(img):
    pass

def entry_to_time(entry):
    minutes = math.floor(entry/6000)
    seconds = (entry - (6000*minutes)) / 100
    text = ""
    if not minutes == 0:
        text += str(minutes) + ":"
        if seconds < 10:
            text += "0"
    text += str(seconds)
    
    if entry == -1:
        return "DNF"
    
    if len(text.split(".")[1]) == 1:
        text += "0"
        
    return text

#1201
#1178

#Cardinal Cube Day
# SCORECARD_HEIGHT = 1201

#Naticube
SCORECARD_HEIGHT = 1178

# for i in fnames:
#     img_ = np.array(Image.open(i))
#     img_ = ocr.add_white_border(img_, (200, 200))

#     imgs.append(img_[0:3508//2, 0:2544//2])
#     imgs.append(img_[3508//2:3508, 0:2544//2])
#     imgs.append(img_[0:3508//2, 2544//2:2544])
#     imgs.append(img_[3508//2:3508, 2544//2:2544])
    
labelsFile = open("dataset/labels.csv", 'w')
numFeatures = 0

for fname in fnames:
    imgs = []
    
    img_ = np.array(Image.open(fname))

    imgs.append(img_[0:3508//2, 0:2544//2])
    imgs.append(img_[3508//2:3508, 0:2544//2])
    imgs.append(img_[0:3508//2, 2544//2:2544])
    imgs.append(img_[3508//2:3508, 2544//2:2544])
    # imgs[-1] = ocr.add_white_border(imgs[-1], (200, 200))
    
    for i in imgs:
        scalar = 1178/SCORECARD_HEIGHT
        
        i = cv2.resize(i, (int(i.shape[1]*scalar), int(i.shape[0]*scalar)), interpolation = cv2.INTER_LINEAR)
        
        # plt.imshow(i)
        # plt.show()
        
        i = ocr.add_white_border(i, (200, 200))
        img, crops = cropping.crop(i)
        
        regId = ocr.read_id(crops['id'][0])
        event = ocr.read_event(crops['event'][0])
        round = ocr.read_id(crops['round'][0], round=True)
        
        if event == 'skip':
            continue
        if event == 'show':
            plt.imshow(i)
            plt.show()
        
        labels = wcalive.get_results(regId, event, round)
        
        if labels == None or regId == None or event == None:
            print("Data not found in WCA Live")
            plt.imsave("ref.png", crops['id'][0])
            regId = int(input("What is the number in ref.png?"))
            plt.imsave("ref.png", crops['event'][0])
            event = input("What is the event in ref.png (event id, 222, 333, minx piram, 333oh, 333bf, sq1, clock)?")
            plt.imsave("ref.png", crops['round'][0])
            round = int(input("What is the number in ref.png?"))
            
            if input("skip card? (y/n)").lower() == 'y': continue
            
            labels = wcalive.get_results(regId, event, round)
            if labels == None:
                print("Entry not found, skipping")
                continue
            
        print(numFeatures ,event, regId, round)
        
        for time in range(len(labels)):
            
            plt.imsave("dataset/imgs/{}.png".format(numFeatures), crops['time'][time])
            labelsFile.write(str(numFeatures) + ',' + str(labels[time]) + "," + entry_to_time(int(labels[time])) + "\n")
            
            numFeatures+=1
            pass

        # print("id", regId)
        # print("event", event)
        # print("round", round)
        # print(labels)

        # plt.imshow(img)
        # plt.show()
    
    