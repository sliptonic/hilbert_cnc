#http://blog.gordn.org/2012/06/python-calculating-average-color-of.html
from PIL import Image, ImageOps
from hilbertcurve.hilbertcurve import HilbertCurve
import argparse
import math

PREAMBLE = """
G17 G54 G40 G49 G80 G90
G21
G54
G0 Z0
G0 X0 Y0
M3 0.7
"""

POSTAMBLE = """
M2
"""


def get_average_color(x, y, n, img):
    """ Returns a grayscale value between 0 and 255 by converting the RGB of
    the pixels surrounding the target pixl within n units.
    """

    # calculate the sample box of pixels
    p = int(n/2)
    limX = img.size[0]
    limY = img.size[1]


    newxmin = 0 if x-p <= 0 else x-p
    newxmax = limX if x+p >= limX else x+p
    newymin = 0 if y-p <= 0 else y-p
    newymax = limY if y+p >= limY else y+p

    box = newxmin, newymin, newxmax, newymax

    # crop the sample box, resize it to 1x1 and get the first (only) pixel color
    color = img.crop(box).resize((1, 1)).getpixel((0, 0))

    # calculate grayscale
    L = color[0] * 299/1000 + color[1] * 587/1000 + color[2] * 114/1000
    return L


def main():
    """
    calculates a hilbert pseudocurve of p iterations.
    Scale the pseudocurve to match the desired image.
    Move along the curve and sample image and to get average color at each segment
    Output gcode corresponding the coordinates and scaled Z levels.

    If no image is given, a flat hilbert curve of the desired size is produced.
    """


    parser = argparse.ArgumentParser(description='Generate a hilbert curve')

    parser.add_argument('-p', '--iterations', type=int, default=5,
        help='hilbert curve is fractal, number of iterative levels')
    parser.add_argument('-s', '--size', type=int, default=100,
        help='size in millimeters')
    parser.add_argument('-zmin', type=float, default=0,
        help='The minimum z value which approximates black')
    parser.add_argument('-zmax', type=float, default=255,
        help='The maximum z value which approximates white')
    parser.add_argument('--laser', action='store_true',
        help='Z values will be output as spindle power (S words)')
    parser.add_argument('-F','--FEED', type=int, default=4000,
        help='Feed rate in mm/min, default = 4000')
    parser.add_argument('-i','--infile',
        help='image filename to process')
    parser.add_argument('-o', '--outfile',
        help='gcode filename to write')

    args = parser.parse_args()


    N=2 # Number of dimensions.  For images, this is always 2
    MAX = 2**(args.iterations*N)-1
    scalefactor = args.size/(math.sqrt(MAX+1))

    imagefile = None

    if args.infile is not None:
        imagefile = Image.open(args.infile)

        if imagefile.size[0] != imagefile.size[1]:
            print('the image is not square. It will be cropped')
            cropsize = min(imagefile.size)
            imagefile = imagefile.crop((0, 0, cropsize, cropsize))
        imagefactor = imagefile.size[0]/(math.sqrt(MAX+1))

    hilbert_curve = HilbertCurve(args.iterations, N)
    with open(args.outfile, "w") as outfile:
        outfile.write(PREAMBLE)
        for ii in range(MAX):
            coords = hilbert_curve.coordinates_from_distance(ii)

            if imagefile is not None:
                zval = get_average_color(x=int(coords[0]*imagefactor), y=int(coords[1]*imagefactor), n=5, img=imagefile)
            else:
                zval = 1
            scalez = (args.zmax-args.zmin)/255*zval-0+args.zmin

            if args.laser:
                #outfile.write(f'M3 S{scalez}\n')
                outfile.write(f'G1 X{coords[0]*scalefactor} Y{coords[1]*scalefactor} F{scalez}\n')
            else:
                outfile.write(f'G1 X{coords[0]*scalefactor} Y{coords[1]*scalefactor} Z{scalez} F{args.FEED}\n')

        outfile.write(POSTAMBLE)

if __name__ == '__main__':
    main()
