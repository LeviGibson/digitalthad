import easyocr
import matplotlib.pyplot as plt
import random
import jellyfish
import os
import pytesseract

reader = easyocr.Reader(["en"])

def read_int_printed_header(obj):
    r = random.randint(0, 100000000000)
    fname = "./tmp/IMG_{}.png".format(r)
    
    plt.imsave(fname, obj)
    output = reader.readtext(fname)
    
    #IF IT DON'T WORK, TRY IT AGAIN WITH A DIFFERENT OCR ENGINE
    #my code is magnificent
    #honestly though, this is just for single-diget IDS and round numbers.
    if output == []:
        val = pytesseract.image_to_string(fname, config='-c tessedit_char_whitelist=0123456789 --psm 10')
        # print(val)
        # plt.imshow(obj)
        # plt.show()
        
        return int(val)
    
    maxval = -1000
    maxthing = None
    for i in output:
        if i[-1] > maxval:
            maxval = i[-1]
            maxthing = i[-2]
            
    os.remove(fname)
    return int(maxthing)

def read_noint_printed_header(obj):
    r = random.randint(0, 100000000000)
    fname = "./tmp/IMG_{}.png".format(r)
    
    plt.imsave(fname, obj)
    output = reader.readtext(fname)
    
    assert output != []
    
    maxval = -1000
    maxthing = None
    for i in output:
        if i[-1] > maxval:
            maxval = i[-1]
            maxthing = i[-2]
            
    os.remove(fname)
    return maxthing

def read_id(obj):
    return int(read_int_printed_header(obj))

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
    text = read_noint_printed_header(obj)
    
    maxVal = -10000
    maxObj = None
    for i in range(len(eventIds)):
        val = jellyfish.jaro_similarity(text, eventNames[i])
        if val > maxVal:
            maxVal = val
            maxObj = eventIds[i]
    
    return maxObj
