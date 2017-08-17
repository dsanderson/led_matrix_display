from samplebase import SampleBase
from rgbmatrix import graphics
import pickle
import random

class SbffLaunch(SampleBase):
    def __init__(self, *args, **kwargs):
        with open("sbff_pixels.pkl","rb") as f:
            self.pixels = pickle.load(f)
            random.seed(100)
            random.shuffle(self.pixels)
        super(SbffLaunch, self).__init__(*args, **kwargs)

    def run(self):
        #TODO: Add waiting for keypress
        
        print "Starting run"
        canvas = self.matrix.CreateFrameCanvas()
        for i in xrange(0, len(self.pixels)-10):
	    for j in xrange(i, i+10):
		p = self.pixels[j]
            	canvas.SetPixel(p[0],p[1],p[2],p[3],p[4])
            canvas = self.matrix.SwapOnVSync(canvas)
        while True:
            canvas = self.matrix.SwapOnVSync(canvas)
	    #pass #TODO: Add qr behavior here

if __name__ == '__main__':
    sbf = SbffLaunch()
    if (not sbf.process()):
        sbf.print_help()
