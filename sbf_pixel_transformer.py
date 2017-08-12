import time, random
from samplebase import SampleBase
from rgbmatrix import graphics
import itertools

xmax = 161
ymax = 225

def make_transformer(panel_x, panel_y, panel_rot, panel_chain_pos):
    panel_x = panel_x
    panel_y = panel_y
    panel_rot = panel_rot
    panel_chain_pos = panel_chain_pos
    def transform(x, y):
        xt = x-panel_x
        yt = y-panel_y
        if panel_rot==0:
            #flip y
            yout = 31-yt
            xout = xt
        elif panel_rot==180:
            #flip x, not y
            xout = 63-xt
            yout = yt
        elif panel_rot==90:
            yout = 31-xt
            xout = 63-yt
        elif panel_rot==270:
            xout = xt
            yout = yt
        xout = xout+(64*(panel_chain_pos-1))
        return xout, yout
    return transform


def get_bounds(panel):
    #format xmin, xmax, ymin, ymax
    if panel[2]==0 or panel[2]==180:#no rotation
        return panel[0], panel[0]+64, panel[1], panel[1]+32
    elif panel[2]==90 or panel[2]==270:
        return panel[0], panel[0]+32, panel[1], panel[1]+64

def transform_pixel(x, y, panels):
    for panel in panels:
        xmin, xmax, ymin, ymax = get_bounds(panel)
        if xmin<=x<xmax and ymin<=y<ymax:
            return panel[4](x, y)


panels = [(32, 193, 0, 1),
            (32, 161, 180, 2),
            (32, 129, 0, 3),
            (32, 97, 180, 4),
            (32, 65, 0, 5),
            (97, 81, 0, 6),
            (97, 49, 180, 7),
            (32, 33, 180, 8),
            (0, 38, 90, 9),
            (32, 0, 0, 10)]
#print panels
pts = []
for p in panels:
    func = make_transformer(p[0], p[1], p[2], p[3])
    pt = list(p)
    pt.append(func)
    pt = tuple(pt)
    pts.append(pt)

ranges = [get_bounds(p) for p in pts]

#test speed
t0=time.time()
for i in xrange(10000):
    r = random.choice(ranges)
    x = random.randint(r[0], r[1]-1)
    y = random.randint(r[2], r[3]-1)
    transform_pixel(x, y, pts)
t1=time.time()

diff = t1-t0
print "Approx. {} sec/pixel".format(diff/float(10000))

class Sbf(SampleBase):
    def __init__(self, *args, **kwargs):
        self.panels = kwargs['panels']
	self.gen_pixel_list()
	super(Sbf, self).__init__(*args, **kwargs)
        #self.panels = kwargs['panels']
        #self.gen_pixel_list()
        #self.draw_start()
        #self.run()
	#pass

    def gen_pixel_list(self):
        panels = [p[0] for p in self.panels]
	#print panels
        self.pixels = []
        for i, p in enumerate(panels):
            xmin, xmax, ymin, ymax = get_bounds(p)
            base_color = self.panels[i][1]
            pixels = list(itertools.product(range(xmin, xmax), range(ymin, ymax)))
            pixels = [transform_pixel(pix[0],pix[1],panels) for pix in pixels]
            pixels = [(pix, base_color) for pix in pixels]
            self.pixels = self.pixels+pixels

    def randomize_color(self, col):
        shift = random.randint(-10, 10)
        r = col[0]+shift if col[0]+shift<255 else 255
        g = col[1]+shift if col[1]+shift<255 else 255
        b = col[2]+shift if col[2]+shift<255 else 255
        #return r,g,b
	return 255, 0, 0

    def draw_start(self):
        print "Drawing base"
        canvas = self.matrix.CreateFrameCanvas()
	#print self.pixels[0]
        for p in self.pixels:
            r,g,b = p[1]
            canvas.SetPixel(p[0][0], p[0][1], r, g, b)
        canvas = self.matrix.SwapOnVSync(canvas)

    def run(self):
        print "Starting run"
        #font = graphics.Font()
        #font.LoadFont("../../fonts/7x13.bdf")
        changed_pixels_indecies = []
	#self.draw_start()
	canvas = self.matrix.CreateFrameCanvas()
	for p in self.pixels:
	    r, g, b = p[1]
	    canvas.SetPixel(p[0][0],p[0][1],r,g,b)
        while True:
	    #canvas.SetPixel(0,0,255,255,255)
            i = random.randint(0, len(self.pixels)-1)
            while len(changed_pixels_indecies)>5:
                i0 = changed_pixels_indecies[0]
		changed_pixels_indecies = changed_pixels_indecies[1:]
                r, g, b = self.pixels[i0][1]
		#print self.pixels[i0][0], r, g, b, changed_pixels_indecies
                canvas.SetPixel(self.pixels[i0][0][0], self.pixels[i0][0][1], r, g, b)
		#canvas = self.matrix.SwapOnVSync(canvas)
            r, g, b = self.randomize_color(self.pixels[i][1])
            canvas.SetPixel(self.pixels[i][0][0], self.pixels[i][0][1], r, g, b)
            changed_pixels_indecies.append(i)
	    canvas = self.matrix.SwapOnVSync(canvas)

if __name__ == '__main__':
    panels = [(p, (0,200,0)) for p in pts]
    sbf = Sbf(panels=panels)
    if (not sbf.process()):
        sbf.print_help()
    #sbf.run()
