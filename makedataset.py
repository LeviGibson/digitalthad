import glob
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cropping
import ocr
import makedataset
import wcalive

fnames = glob.glob("./raw/*")

def generate_data_point(img):
    pass

imgs = []
for i in fnames:
    img_ = np.array(Image.open(i))
    
    imgs.append(img_[0:3508//2, 0:2544//2])
    imgs.append(img_[3508//2:3508, 0:2544//2])
    imgs.append(img_[0:3508//2, 2544//2:2544])
    imgs.append(img_[3508//2:3508, 2544//2:2544])
    

for i in imgs:
    img, crops = cropping.crop(i)
    
    for id, j in enumerate(crops['id']):
        plt.imsave(str(id) + ".png", j)
        
    regId = ocr.read_id(crops['id'][0])
    event = ocr.read_event(crops['event'][0])
    round = ocr.read_id(crops['round'][0])
    
    labels = wcalive.get_results(regId, event, round)
    
    print("id", regId)
    print("event", event)
    print("round", round)
    print(labels)

    plt.imshow(img)
    plt.show()
    