from scipy.ndimage import filters as flt
from matplotlib.pyplot import *
from numpy import*
from PIL import Image


class Descriptor:
    """
    Descriptor Class
    Finding corresponding points between images
    """
    def __init__(self, img1, img2, wid, threshold):
    	self._img1 = img1
    	self._img2 = img2 
    	self._wid   = wid
    	self._threshold = threshold
    	
    def get_descriptors(self, image, filtered_coords):
        """ 
        For each point return pixel values around the point
        using a neighbourhood of width 2*wid+1. (Assume points are
        extracted with min_distance > wid). 
        """
        desc = []
        for coords in filtered_coords:
            patch = image[coords[0]-self._wid:coords[0]+self._wid+1,
            coords[1]-self._wid:coords[1]+self._wid+1].flatten()
            desc.append(patch)
        return desc
    	
    def match(self, desc1, desc2):
        """ 
        For each corner point descriptor in the first image,
        select its match to second image using
        normalized cross correlation. 
        """
        n = len(desc1[0])
        # pair-wise distances
        d = -ones((len(desc1),len(desc2)))
        for i in range(len(desc1)):
            for j in range(len(desc2)):
                d1 = (desc1[i] - mean(desc1[i])) / std(desc1[i])
                d2 = (desc2[j] - mean(desc2[j])) / std(desc2[j])
                ncc_value = sum(d1 * d2) / (n-1)
                if ncc_value > self._threshold:
	                d[i,j] = ncc_value
				
        ndx = np.argsort(-d)
        matchscores = ndx[:,0]
	
        return matchscores
        
    def match_twosided(self, desc1,desc2):
	    """ Two-sided symmetric version of match()."""
	    matches_12 = self.match(desc1,desc2)
	    matches_21 = self.match(desc2,desc1)
	    ndx_12 = where(matches_12 >= 0)[0]
	    # remove matches that are not symmetric
	    for n in ndx_12:
	        if matches_21[matches_12[n]] != n:
	            matches_12[n] = -1
	            
	    return matches_12
        
   
    def appendimages(self):
	    """ Return a new image that appends the two images side-by-side. """
	    # select the image with the fewest rows and fill in enough empty rows
	    rows1 = self._img1.shape[0]
	    rows2 = self._img2.shape[0]
	    if rows1 < rows2:
		    self._img1 = np.concatenate((self._img1,zeros((rows2-rows1,self._img1.shape[1]))),axis=0)
	    elif rows1 > rows2:
		    self._img2 = np.concatenate((self._img2,zeros((rows1-rows2,self._img2.shape[1]))),axis=0)
	    # if none of these cases they are equal, no filling needed.
	    return np.concatenate((self._img1,self._img2), axis=1)
	    
	    
    def plot_matches(self, locs1, locs2, matchscores,graph,show_below=True):
	    """ Show a figure with lines joining the accepted matches
	    input: im1,im2 (images as arrays), locs1,locs2 (feature locations),
	    matchscores (as output from ’match()’),
	    show_below (if images should be shown below matches). """
	    im3 = self.appendimages()
	    if show_below:
		    im3 = vstack((im3,im3))
		
	    imshow(im3)
	
	    cols1 = self._img1.shape[1]
	    
	    if graph.lower() == "point":    
	        for i,m in enumerate(matchscores):
		        if m>0:	
			        plot(locs1[i][1],locs1[i][0],'b*')
			        plot(locs2[m][1]+cols1,locs2[m][0],'r.')	
			        axis('off')

	    elif graph.lower() == "line":
	     	for i,m in enumerate(matchscores):
		        if m>0:	
			        plot([locs1[i][1],locs2[m][1]+cols1],[locs1[i][0],locs2[m][0]],'c')			
			        axis('off')
	    else:
	        pass

