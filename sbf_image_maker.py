from PIL import Image, ImageDraw
import time, random
import itertools
import pickle
import tqdm

im = Image.open("SBF_logo_final.png")

w, h = im.size

scale = 1.015

tx = -2
ty = 0#-100

temp_image = Image.new('RGBA', (w+150, h))
temp_image.paste(im, (0,0,w,h))
print temp_image.size
im = temp_image

data = (scale, 0, tx, 0, scale, ty)

im = im.transform(im.size,Image.AFFINE,data)
im.save("sbf_images/temp_logo.PPM","PPM")
print im.size

pixels = []

w, h = im.size

for x in xrange(0, w):
    for y in xrange(0, h):
        #flip y.  Also introduce any shift here
        xt = x
        yt = h-(y+1)
        r, g, b, a = im.getpixel((x,y))
        if any([r != 0, b != 0, g != 0, a != 0]):
            if not all([r==255,g==255,b==255]):
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

print ranges

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


def make_cube_image(cube_coords, base_image, out_name, panels):
    im = Image.open(base_image)
    draw = ImageDraw.Draw(im)
    #iterate over pixels in cubes, converting to the panel-space, and color those pixels white
    for p in cube_coords:
        if transform_pixel(p[0], p[1], panels)==None: #We shouldn't need this, look into it
            continue
        xt, yt = transform_pixel(p[0], p[1], panels)
        draw.point([(xt, yt)], (255, 255, 255))
    del draw
    im.save(out_name, "PPM")

def convert_cube_coords(cube_pose):
    """convert from a grid with lattice pointsd corresponding to cubes to one corresponsding to pixles
    inputs:
        cube_pose: integer 2-tuple
    outputs:
        cube_coords: list of integer 2-tuples of pixel locations in untransformed space"""
    xt = 6#12 #offsets for top-left of cubes
    yt = 0#7
    xstart = cube_pose[0]*13+xt
    xend = xstart+12
    yend = ymax-1-cube_pose[1]*13+yt
    ystart = yend-12
    cube_coords = []
    for x in range(xstart, xend):
        for y in range(ystart, yend):
            cube_coords.append((x, y))
    return cube_coords

# cubes = [(4,0),(5,0),
#     (4,1),(5,1),
#     (3,2),(4,2),
#     (2,3),(3,3),(4,3),
#     (2,4),(3,4),
#     (2,5),(3,5),
#     (2,6),(3,6),(4,6),
#     (2,7),(3,7),(4,7),
#     (2,8),(3,8),(4,8),(5,8),
#     (2,8),(3,8),(4,8),(5,8)]

cube_ascii = """    ##
    ##
   ##
  ###
  ##
  ##
  ###
  ###
  ####
   ### #
    ##
    ########
    ########
###########
   ##
  ##
  #"""

cube_ascii = cube_ascii.split("\n")
#cube_ascii = [c.strip() for c in cube_ascii]

cubes = []
for y, row in enumerate(cube_ascii):
    for x, c in enumerate(row):
        if c=='#':
            cubes.append((x,y))

print cubes

if __name__ == '__main__':
    out_pixels = []
    misses = 0
    for p in pixels:
        x1 = p[0]+12
        y1 = p[1]+7
        if transform_pixel(x1,y1,pts)==None:
            misses += 1
            continue
        xt, yt = transform_pixel(x1,y1,pts)
        out_pixels.append((xt, yt, p[2], p[3], p[4]))
    print len(pixels), misses
    make_image(out_pixels, 20*32, 32, "sbf_images/sbf_logo.PPM")
    for i, c in tqdm.tqdm(enumerate(cubes)):
        pixs = convert_cube_coords(c)
        make_cube_image(pixs, "sbf_images/sbf_logo.PPM", "sbf_images/{}.PPM".format(i), pts)
