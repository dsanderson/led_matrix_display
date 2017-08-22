import time, random
import itertools
import pickle
import sbff_data

xmax = 238
ymax = 128

img = sbff_data.img

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
            xout = yt
            yout = xt
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


panels = [(0, 64, 90, 10),
            (32, 64, 270, 9),
            (64, 64, 90, 8),
            (96, 64, 270, 7),
            (128, 64, 90, 6),
            (160, 64, 270, 5),
            (110, 32, 0, 4),
            (78, 0, 270, 3),
            (110, 0, 180, 2),
            (174, 0, 180, 1)]
#print panels
pts = []
for p in panels:
    func = make_transformer(p[0], p[1], p[2], p[3])
    pt = list(p)
    pt.append(func)
    pt = tuple(pt)
    pts.append(pt)

ranges = [get_bounds(p) for p in pts]
#for r in ranges:
#    print r

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

if __name__ == '__main__':
    pixels = []
    for p in img:
	x = p[0]
        y = ymax-1-p[1]
	if transform_pixel(x,y,pts)==None:
	    continue
	xt, yt = transform_pixel(x,y,pts)
	pixels.append((xt, yt, p[2], p[3], p[4]))

print len(pixels)

with open("sbff_pixels.pkl", "wb") as f:
    pickle.dump(pixels, f)
