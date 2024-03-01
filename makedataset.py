import glob
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cropping
import ocr
import wcalive

fnames = glob.glob("./raw/*")
fnames = list(sorted(fnames))

def generate_data_point(img):
    pass



imgs = []
for i in fnames:
    img_ = np.array(Image.open(i))
    img_ = ocr.add_white_border(img_, (200, 200))

    imgs.append(img_[0:3508//2, 0:2544//2])
    imgs.append(img_[3508//2:3508, 0:2544//2])
    imgs.append(img_[0:3508//2, 2544//2:2544])
    imgs.append(img_[3508//2:3508, 2544//2:2544])
    
labelsFile = open("dataset/labels.csv", 'w')
numFeatures = 0

for i in imgs:
    img, crops = cropping.crop(i)
    
    regId = ocr.read_id(crops['id'][0])
    event = ocr.read_event(crops['event'][0])
    round = ocr.read_id(crops['round'][0], round=True)
    
    labels = wcalive.get_results(regId, event, round)
    
    print(event, regId, round)
    
    for time in range(len(labels)):
        
        plt.imsave("dataset/imgs/{}.png".format(numFeatures), crops['time'][time])
        labelsFile.write(str(numFeatures) + ',' + str(labels[time]) + "\n")
        
        numFeatures+=1
        pass
    # print("id", regId)
    # print("event", event)
    # print("round", round)
    # print(labels)

    # plt.imshow(img)
    # plt.show()
    
    