import time, random
import itertools
import pickle
import sbf_data

xmax = 161
ymax = 225

img = sbf_data.img

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

if __name__ == '__main__':
    pixels = []
    for p in img:
	x1 = p[0]+12
	y1 = p[1]+7
        if transform_pixel(x1,y1,pts)==None:
            continue
        xt, yt = transform_pixel(x1,y1,pts)
        pixels.append((xt, yt, p[2], p[3], p[4]))

with open("sbf_pixels.pkl", "wb") as f:
    pickle.dump(pixels, f)
