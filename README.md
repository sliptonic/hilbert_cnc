# hilbert_cnc
Generating gcode for hilbert curves with and without image sampling 

hilbertgcode.py is a simplified version that only does the curve.
hilbertimage.py can do everything gilbergcode.py can do as well as image sampling.



usage: hilbertimage.py [-h] [-p ITERATIONS] [-s SIZE] [-zmin ZMIN]
                       [-zmax ZMAX] [--laser] [-F FEED] [-i INFILE]
                       [-o OUTFILE]

Generate a hilbert curve

optional arguments:
  -h, --help            show this help message and exit
  -p ITERATIONS, --iterations ITERATIONS
                        hilbert curve is fractal, number of iterative levels
  -s SIZE, --size SIZE  size in millimeters
  -zmin ZMIN            The minimum z value which approximates black
  -zmax ZMAX            The maximum z value which approximates white
  --laser               Z values will be output as spindle power (S words)
  -F FEED, --FEED FEED  Feed rate in mm/min, default = 4000
  -i INFILE, --infile INFILE
                        image filename to process
  -o OUTFILE, --outfile OUTFILE
                        gcode filename to write
