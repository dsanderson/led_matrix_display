from PIL import Image

im = Image.open("SBFF_logo.png")

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

with open("sbff_data.py", "w") as f:
	pts = ",".join(["({},{},{},{},{})".format(*p) for p in pixels])
	pts = "[{}]".format(pts)
	pts = "img = {}".format(pts)
	f.write(pts)
