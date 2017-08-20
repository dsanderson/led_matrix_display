from PIL import Image, ImageDraw
import time, random
import itertools
import pickle
import tqdm

im = Image.open("SBFF_logo.png")

w = im.width
h = im.height

pixels = []

for x in xrange(0, w):
    for y in xrange(0, h):
        #flip y.  Also introduce any shift here
        xt = x
        yt = y#h-(y+1)
        r, g, b, a = im.getpixel((x,y))
        if any([r != 0, b != 0, g != 0, a != 0]):
            pixels.append((xt, yt, r, g, b))

print len(pixels)

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
    xt = 0 #offsets for top-left of cubes
    yt = 0
    xstart = cube_pose[0]*6+xt
    xend = xstart+5
    ystart = cube_pose[1]*6+yt
    yend = ystart+5
    cube_coords = []
    for x in range(xstart, xend+1):
        for y in range(ystart, yend+1):
            cube_coords.append((x, ymax-1-y))
    return cube_coords

cubes = [(3,0),(4,0),(5,0),(6,0),(9,0),(10,0),
    (1,1),(2,1),(3,1),(4,1),(5,1),(6,1),(7,1),(9,1),(10,1),(11,1),
    (1,2),(2,2),(3,2),(4,2),(5,2),(6,2),(7,2),(10,2),(11,2),(12,2),
    (0,3),(1,3),(2,3),(3,3),(4,3),(5,3),(6,3),(7,3),(8,3),(9,3),(10,3),(11,3),(12,3),
    (4,4),(5,4),(6,4),(7,4),(8,4),(9,4),(10,4),(11,4),(12,4),
    (6,5),(7,5),(8,5),(9,5),(10,5),(11,5),(12,5),
    (8,6),(9,6),(10,6),(11,6),(12,6),
    (9,7),(10,7),(11,7),(12,7),
    (10,8),(11,8),(12,8),(13,8),(14,8),(15,8),(16,8),(17,8),(18,8),
    (12,9),(13,9),(14,9),(15,9),(16,9),(17,9)]

if __name__ == '__main__':
    out_pixels = []
    for p in pixels:
        x = p[0]
        y = ymax-1-p[1]
        if transform_pixel(x,y,pts)==None:
            continue
        xt, yt = transform_pixel(x,y,pts)
        out_pixels.append((xt, yt, p[2], p[3], p[4]))
    make_image(out_pixels, 20*32, 32, "sbff_images/sbff_logo.PPM")
    for i, c in tqdm.tqdm(enumerate(cubes)):
        pixs = convert_cube_coords(c)
        make_cube_image(pixs, "sbff_images/sbff_logo.PPM", "sbff_images/{}.PPM".format(i), pts)
