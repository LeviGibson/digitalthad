from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
import cropping

im = Image.open("new.tiff")
cropped = cropping.crop(im)


