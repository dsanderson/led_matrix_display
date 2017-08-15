from samplebase import SampleBase
from rgbmatrix import graphics
import pickle
import random

class SbfLaunch(SampleBase):
    def __init__(self, *args, **kwargs):
        with open("sbf_pixels.pkl","rb") as f:
            self.pixels = pickle.load(f)
            random.seed(100)
            random.shuffle(self.pixels)
        super(Sbf, self).__init__(*args, **kwargs)

    def run(self):
        #TODO: Add waiting for keypress
        
        print "Starting run"
        canvas = self.matrix.CreateFrameCanvas()
        for p in self.pixels:
            canvas.SetPixel(p[0],p[1],p[2],p[3],p[4])
            canvas = self.matrix.SwapOnVSync(canvas)
        while True:
            pass #TODO: Add qr behavior here

if __name__ == '__main__':
    sbf = SbfLaunch()
    if (not sbf.process()):
        sbf.print_help()
