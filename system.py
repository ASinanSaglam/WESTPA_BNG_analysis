from __future__ import division, print_function; __metaclass__ = type
import numpy as np
import west
from west import WESTSystem
from westpa.binning import VoronoiBinMapper, RectilinearBinMapper
from scipy.spatial.distance import cdist

import logging
log = logging.getLogger(__name__)
log.debug('loading module %r' % __name__)

def dfunc(p, centers):
    #print("Dfunc called")
    #print(p, centers)
    #print(p.shape, centers.shape)
    ds = cdist(np.array([p]),centers)
    return np.array(ds[0], dtype=p.dtype)

class System(WESTSystem):
    def initialize(self):
        self.pcoord_ndim = 8
        self.pcoord_len = 2
        self.pcoord_dtype = np.float32
        nbins = 1
        self.nbins = nbins

        centers = np.zeros((self.nbins,self.pcoord_ndim),dtype=self.pcoord_dtype)
        centers[:,:] = 1

        self.bin_mapper = VoronoiBinMapper(dfunc, centers)
        self.bin_target_counts = np.empty((self.bin_mapper.nbins,), np.int)
        self.bin_target_counts[...] = 50
