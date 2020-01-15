#http://blog.gordn.org/2012/06/python-calculating-average-color-of.html
from hilbertcurve.hilbertcurve import HilbertCurve
import argparse
import math

PREAMBLE = """
G17 G54 G40 G49 G80 G90
G21
G54
G0 Z10
G0 X0 Y0
"""

POSTAMBLE = """
M2
"""


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
    parser.add_argument('-F','--FEED', type=int, default=4000,
        help='Feed rate in mm/min, default = 4000')
    parser.add_argument('-o', '--outfile',
        help='gcode filename to write')
    parser.add_argument('-zmin', type=float, default=0,
        help='The drawing level')
    parser.add_argument('-zmax', type=float, default=10,
        help='the clearance level')

    args = parser.parse_args()


    N=2 # Number of dimensions.  For images, this is always 2
    MAX = 2**(args.iterations*N)-1
    scalefactor = args.size/(math.sqrt(MAX+1))


    hilbert_curve = HilbertCurve(args.iterations, N)
    with open(args.outfile, "w") as outfile:
        outfile.write(PREAMBLE)
        for ii in range(MAX):
            coords = hilbert_curve.coordinates_from_distance(ii)

            outfile.write(f'G1 X{coords[0]*scalefactor} Y{coords[1]*scalefactor} Z{args.zmin} F{args.FEED}\n')

        outfile.write(POSTAMBLE)
        outfile.write(f'G0 Z{args.zmax}')

if __name__ == '__main__':
    main()
