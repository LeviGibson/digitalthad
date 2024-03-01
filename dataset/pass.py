import numpy as np
from PIL import Image
import cv2
import os
import shutil
import math

infile = open("labels.csv", 'r')
outfile = open("passed.csv", 'w')

labels = []
for line in infile:
    labels.append(line)

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

id = 0
while id < len(labels):
    line = labels[id]
    line = line[0:-1].split(',')
    line = ((line[0]), int(line[1]))
    shutil.copyfile("./imgs/{}.png".format(id), "view.png")
    
    text = entry_to_time(line[1])
    
    print(text)
    
    ui = input("Correction:")
    if ui != '':
        if ui == "!":
            text = entry_to_time(line[1]-200) + "+2=" + entry_to_time(line[1])
        elif ui == "b":
            id -= 2
    
    outfile.write(line[0] + "," + str(text) + "\n")
    id+=1
    
outfile.close()
infile.close()

usedthings = []
outfile = open("buffer.csv", 'w')

for line in reversed(open("passed.csv").readlines()):
    line = line.rstrip().split(',')
    if int(line[0]) in usedthings:
        continue

    usedthings.append(int(line[0]))
    outfile.write(line[0] + "," + line[1] + "\n")

outfile.close()
outfile = open("labels2.csv", 'w')
for line in reversed(open("buffer.csv").readlines()):
    outfile.write(line.rstrip() + "\n")

outfile.close()
