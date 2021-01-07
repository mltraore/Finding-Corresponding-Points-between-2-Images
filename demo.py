from scipy.ndimage import filters as flt
from matplotlib.pyplot import *
from numpy import*
from PIL import Image
from harris import Harris
from descriptor import Descriptor

import argparse

"""
Usage:
    python3 demo.py \
            --image1        image1_name    \
            --image2        image2_name    \
            --sigma         sigma value    \
            --threshold_h   threshold value for harris corner detector \
            --threshold_d   threshold vaşue for point descriptor       \
            --min_dist      minimum distance value between points      \
            --wid           wid value                                  \
            --graph         graph type [line or point]                 
         
    Not: Command line arguments are optional
    Examples:
        
    python3  demo.py \
            --image1         01.png  \
            --image2         02.png  \
            --threshold_h    0.1     \
            --threshold_d    0.5     \
            --min_dist       10      \
            --wid            5       \
            --graph          line                 
"""


parser = argparse.ArgumentParser()
parser.add_argument('--image1', help='First image name', default='01.png')
parser.add_argument('--image2', help='Second image name', default='02.png')
parser.add_argument('--sigma', type=int,  help='Sigma value',default=3)
parser.add_argument('--threshold_h', type=float, help='Harris points threshold value',default=0.1)
parser.add_argument('--threshold_d', type=float, help='Descriptor threshold value',default=0.3)
parser.add_argument('--min_dist', type=int, help='Minimum distance',default=10)
parser.add_argument('--wid', type=int, help='Wid value',default=5)
parser.add_argument('--graph', help='Graph choise[ line or point]', default="point")


args  = parser.parse_args()
img1  = args.image1
img2  = args.image2
sigma = args.sigma
threshold_h = args.threshold_h
threshold_d = args.threshold_d
min_dist    = args.min_dist
wid         = args.wid 
my_graph    = args.graph 


im1 = np.array(Image.open(img1).convert('L'))
im2 = np.array(Image.open(img2).convert('L'))

descriptor = Descriptor(im1, im2, wid, threshold_d)

harris1 = Harris(im1, sigma, threshold_h, min_dist)
harrisim1 = harris1.compute_harris_response()
filtered_coords1 = harris1.get_harris_points(harrisim1)
d1 = descriptor.get_descriptors(im1, filtered_coords1)  

harris2 = Harris(im2, sigma, threshold_h, min_dist)
harrisim2 = harris1.compute_harris_response()
filtered_coords2 = harris1.get_harris_points(harrisim2)
d2 = descriptor.get_descriptors(im2, filtered_coords2)

matches = descriptor.match_twosided(d1,d2)
figure()
gray()
descriptor.plot_matches(filtered_coords1,filtered_coords2,matches,graph=my_graph)
show()
