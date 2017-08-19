from samplebase import SampleBase
from rgbmatrix import graphics
import pickle
import random
import keyboard
from PIL import image

class SbffLaunch(SampleBase):
    def __init__(self, *args, **kwargs):
        super(SbffLaunch, self).__init__(*args, **kwargs)

    def run(self):
        self.image = Image.open("sbff_images/base.PPM").convert('RGB')
        print "Starting run"
        canvas = self.matrix.CreateFrameCanvas()
        canvas.SetImage(self.image,0,0)
        while True:
            canvas = self.matrix.SwapOnVSync(canvas)
	    #pass #TODO: Add qr behavior here

if __name__ == '__main__':
    print "waiting for page down"
    keyboard.wait("page down")
    sbff = SbffLaunch()
    if (not sbff.process()):
        sbff.print_help()
