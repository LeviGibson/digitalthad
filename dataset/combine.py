import glob
import shutil

folderNames = ["./Cardinal/", "./Naticube/"]
outfile = open("data.csv", 'w')

numFeatures = 0

for folder in folderNames:
    infile = open(folder + "labels.csv")
    for line in infile:
        line = line[0:-1].split(',')
        outfile.write("{},{},{}\n".format(numFeatures, line[1], line[2]))
        shutil.copyfile(folder+"imgs/{}.png".format(line[0]), "./imgs/{}.png".format(numFeatures))
        numFeatures+=1
        print(numFeatures)
