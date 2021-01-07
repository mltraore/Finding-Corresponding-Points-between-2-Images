from scipy.ndimage import filters as flt
from matplotlib.pyplot import *
from numpy import*
from PIL import Image

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--image', help='The image directory', default='01.png')
parser.add_argument('--sigma', type=int, help='Sigma value', default=3)
parser.add_argument('--threshold',type=float,help='Threshold value',default=0.1)
parser.add_argument('--min_dist',type=int,help='Minimum distance',default=10)

# To use this please uncomment the below arguments

# args = parser.parse_args()
# img       =  args.image
# sigma     =  args.sigma
# threshold =  args.threshold
# min_dist  =  args.min_dist


class Harris:
    """
    Harris Corner Detector Class
    Usage:
         - uncomment above arguments
           python3 harris.py  \
                  --image      image_name \
                  --simga      sigma_value
                  --threshold  threshold value
                  --min_dist   Minimum distance value
    """

    def __init__(self, image, sigma, threshold, min_dist):
        self._image = image
        self._sigma = sigma
        self._threshold = threshold
        self._min_dist = min_dist

    def compute_harris_response(self):
        """Compute the Harris corner detector response function
                   for each pixel in a graylevel image.
        """
        # derivates
        imx = zeros(self._image.shape)
        flt.gaussian_filter(
            self._image, (self._sigma, self._sigma), (0, 1), imx)
        imy = zeros(self._image.shape)
        flt.gaussian_filter(
            self._image, (self._sigma, self._sigma), (1, 0), imy)
        # compute components of the Harris matrix
        Wxx = flt.gaussian_filter(imx * imx, self._sigma)
        Wxy = flt.gaussian_filter(imx * imy, self._sigma)
        Wyy = flt.gaussian_filter(imy * imy, self._sigma)
        # determinant and trace
        Wdet = Wxx * Wyy - Wxy**2
        Wtr = Wxx + Wyy
        return Wdet / Wtr

    def get_harris_points(self, harris):
        """
        Return corners from a Harris response image
        min_dist is the minimum number of pixels separating
        corners and image boundary.
        """

        # find top corner candidates above a threshold
        corner_threshold = harris.max() * self._threshold
        harris_t = (harris > corner_threshold) * 1
        # get coordinates of candidates
        coords = array(harris_t.nonzero()).T
        # ...and their values
        candidate_values = [harris[c[0], c[1]] for c in coords]
        # sort candidates
        index = argsort(candidate_values)
        # store allowed point locations in array
        allowed_locations = zeros(harris.shape)
        allowed_locations[self._min_dist:-self._min_dist,
                            self._min_dist:-self._min_dist] = 1
        # select the best points taking min_distance into account
        filtered_coords = []
        for i in index:
            if allowed_locations[coords[i, 0], coords[i, 1]] == 1:
                filtered_coords.append(coords[i])
                allowed_locations[(coords[i, 0] - self._min_dist):(coords[i, 0] + self._min_dist), (coords[i, 1] - self._min_dist):(coords[i, 1] + self._min_dist)] = 0

        return filtered_coords

    def plot_harris_points(self, filtered_coords):
        """ Plots corners found in image."""
        figure()
        gray()
        imshow(self._image)
        plot([p[1] for p in filtered_coords], [p[0]
                                               for p in filtered_coords], 'r.')
        axis('off')
        show()


if __name__ == "__main__":
    """ Demo   """
    im = np.array(Image.open(img).convert('L'))
    xs = Harris(im, sigma, threshold, min_dist)
    harris = xs.compute_harris_response()
    filtered_coords = xs.get_harris_points(harris)
    xs.plot_harris_points(filtered_coords)
