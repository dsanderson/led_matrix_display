from samplebase import SampleBase
from rgbmatrix import graphics
import pickle
import random
import keyboard
from PIL import image
import urllib2
import time

class SbfLaunch(SampleBase):
    def __init__(self, *args, **kwargs):
        super(SbfLaunch, self).__init__(*args, **kwargs)

    def run(self):
        self.image = Image.open("sbf_images/base.PPM").convert('RGB')
        print "Starting run"
        canvas = self.matrix.CreateFrameCanvas()
        canvas.SetImage(self.image,0,0)
        while True:
            try:
                response = urllib2.urlopen('http://dsa.tech/flask/sbf/sbf/get')
                cube = response.read()
                if int(cube)<0:
                    canvas.SetImage(self.image,0,0)
                else:
                    cube_image = Image.open("sbf_images/{}.PPM".format(int(cube)-1)).convert('RGB')
                    canvas.SetImage(cube_image,0,0)
            except:
                canvas.SetImage(self.image,0,0)
            canvas = self.matrix.SwapOnVSync(canvas)
            time.sleep(0.1)
	    #pass #TODO: Add qr behavior here

if __name__ == '__main__':
    print "waiting for page down"
    keyboard.wait("page down")
    sbf = SbfLaunch()
    if (not sbf.process()):
        sbf.print_help()
