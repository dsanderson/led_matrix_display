from PIL import Image, ImageDraw
import time, random
import itertools
import pickle

im = Image.open("SBF_logo.png")

w = im.width
h = im.height

pixels = []

for x in xrange(0, w):
	for y in xrange(0, h):
		#flip y.  Also introduce any shift here
		xt = x
		yt = h-(y+1)
		r, g, b, a = im.getpixel((x,y))
		if any([r != 0, b != 0, g != 0, a != 0]):
			pixels.append((xt, yt, r, g, b))

print len(pixels)

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


panels = [(32, 193, 180, 1),
            (32, 161, 0, 2),
            (32, 129, 180, 3),
            (32, 97, 0, 4),
            (32, 65, 180, 7),
            (97, 76, 0, 5),
            (97, 44, 180, 6),#180
            (32, 33, 0, 9),
            (0, 38, 90, 8),
            (32, 0, 180, 10)]
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
#t0=time.time()
#for i in xrange(10000):
#    r = random.choice(ranges)
#    x = random.randint(r[0], r[1]-1)
#    y = random.randint(r[2], r[3]-1)
#    transform_pixel(x, y, pts)
#t1=time.time()

#diff = t1-t0
#print "Approx. {} sec/pixel".format(diff/float(10000))

def make_image(pixels, w, h, name):
    im = Image.new("RGB",(w,h))
    draw = ImageDraw.Draw(im)
    for p in pixels:
        draw.point([(p[0],p[1])], (p[2],p[3],p[4]))
    del draw
    im.save(name, "PPM")


if __name__ == '__main__':
    out_pixels = []
    for p in pixels:
		x1 = p[0]+12
		y1 = p[1]+7
	    if transform_pixel(x1,y1,pts)==None:
            continue
        xt, yt = transform_pixel(x1,y1,pts)
        out_pixels.append((xt, yt, p[2], p[3], p[4]))
    make_image(pixels, 20*32, 32, "sbf_logo.PPM")