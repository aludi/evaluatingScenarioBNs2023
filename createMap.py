import cv2
import numpy as np
from skimage import io
import matplotlib.pyplot as plt
from PIL import Image


img = Image.open("groteMarkt4.png")
y = 75
x = int(y*1.5)
reduced_img = img.resize((x,y),resample=Image.BILINEAR)
result = reduced_img.resize(img.size,Image.NEAREST)
result.save('groteMarkt4Reduced.png')

