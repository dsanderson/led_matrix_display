#!/usr/bin/env python
import time
import sys
import keyboard
import urllib2
import traceback

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

image = Image.open("sbff_images/sbff_logo.PPM")

keyboard.wait('page down')

# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 20
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'

matrix = RGBMatrix(options = options)

matrix.SetImage(image.convert('RGB'))

#cube = 0
while True:
    #cube+=1
    try:
        response = urllib2.urlopen('http://dsa.tech/flask/sbf/sbff/get')
        cube = response.read()
        #cube = cube if cube<80 else -1
        if int(cube)<=0:
            matrix.SetImage(image.convert('RGB'))
        else:
            cube_image = Image.open("sbff_images/{}.PPM".format(int(cube)-1))
            matrix.SetImage(cube_image.convert('RGB'))
    except Exception, e:
        traceback.print_exc()
        matrix.SetImage(image.convert('RGB'))
    time.sleep(0.25)
