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
    ds = cdist(np.array([p]),centers)
    return np.array(ds[0], dtype=p.dtype)

class System(WESTSystem):
    def initialize(self):
        self.pcoord_ndim = 12
        self.pcoord_len = 2 
        self.pcoord_dtype = np.float32
        self.nbins = 1

        centers = np.zeros((self.nbins,self.pcoord_ndim),dtype=self.pcoord_dtype)
        # Using the values from the inital point
        i = np.loadtxt('bngl_conf/init.gdat')
        centers[0] = i[4:]

        self.bin_mapper = VoronoiBinMapper(dfunc, centers)
        self.bin_target_counts = np.empty((self.bin_mapper.nbins,), np.int)
        self.bin_target_counts[...] = 20
