import numpy as np
import pickle, sys
from westpa.binning import NopMapper, RectilinearBinMapper

index_dtype = np.uint16

class wrapped_clusterer(NopMapper):
    def __init__(self, clusterer):
        super(NopMapper,self).__init__()
        self.predictor = clusterer
        self.labels = [0,1,2,3]
        self.nbins = 4
        
    def assign(self, coords, mask=None, output=None):
        #print("In .assign")
        #print("coordinates")
        #print(coords, coords.shape)

        assigned = np.array(self.predictor.predict(coords), dtype=index_dtype)
        try:
            output[...] = assigned[...]
            #print(output, output.shape)
        except:
            pass
        #print("assigned")
        #print(assigned, assigned.shape)

        return assigned 

def pull_data(n_iter, iter_group):
    '''
    This function reshapes the progress coordinate and 
    auxiliary data for each iteration and retuns it to
    the tool.
    '''
    data_to_pull = np.loadtxt("data_to_pull.txt") - 1
    d1, d2 = data_to_pull 
    pcoord  = iter_group['pcoord'][:,:,[d1,d2]]
    
    data = pcoord

    return data

def pull_all_data(n_iter, iter_group):
    '''
    This function reshapes the progress coordinate and 
    auxiliary data for each iteration and retuns it to
    the tool.
    '''
    pcoord  = iter_group['pcoord'][:,:,:]

    data = pcoord

    return data

def avg(hist, midpoints, binbounds):
  
    # First we are going to import the pyplot library
    # to get access to the matplotlib object so we can 
    # further modify it.
    import matplotlib.pyplot as plt

    # Now we are going to change the title, add axis labels
    plt.xlabel('Protein A concentration')
    plt.ylabel('Protein B concentration') 
    plt.xlim((0,30))
    plt.ylim((0,30))

def assign_cluster():
    print("making the wrapped clusterer")
    WClusterer = wrapped_clusterer(clusterer)
    return WClusterer

def load_mapper(file_name, iter_no):
    import h5py, pickle, IPython
    h = h5py.File(file_name, 'r')
    #hashval = 
    topol_grp = h['bin_topologies']

    index = topol_grp['index']
    pickles = topol_grp['pickles']
    n_entries = len(index)

    chunksize = 256
    istart = iter_no - 1
    #for istart in range(0, n_entries, chunksize):
    chunk = index[istart:min(istart+chunksize, n_entries)]
        #for i in range(len(chunk)):
    i = 0
            #if chunk[i]['hash'] == hashval:
    pkldat = bytes(pickles[istart+i, 0:chunk[i]['pickle_len']].data)
    mapper = pickle.loads(pkldat)
    #IPython.embed()
    return mapper


def assign_voronoi():
    print("Pulling the latest bin mapper")
    #mapper = load_mapper("west.h5.1529", 500)
    mapper = load_mapper('../west.h5', 100)
    return mapper

def assign_pcca():
    print("making the wrapped clusterer")
    mapper = load_mapper('../west.h5', 100)
    WClusterer = wrapped_mapper(mapper)
    WClusterer.load_pcca_labels('/home/monoid/PROJECTS/PLURI_12GENE/001/analysis/metasble_assignments.pkl')
    return WClusterer

def assign_halton():
    import matplotlib.pyplot as plt
    import ghalton as gh
    print("getting halton centers")
    mapper = load_mapper('../west.h5', 100)
    seq = gh.Halton(mapper.centers.shape[1])
    s = np.array(seq.get(mapper.centers.shape[0]))
    for i in range(mapper.centers.shape[1]):
        s[:,i] = s[:,i] * (mapper.centers[:,i].max())
    # plot test
    plt.plot(s[:,0], s[:,1], lw=0, marker="o", c="r", label="hcenters")
    plt.plot(mapper.centers[:,0], mapper.centers[:,1], lw=0, marker="+", c="k", label="map centers")
    plt.legend(frameon=False)
    plt.savefig("map_test.png")
    plt.close()
    print(s, mapper.centers)
    print(s[:,0].min(), s[:,1].max())
    print(mapper.centers[:,0].min(), mapper.centers[:,1].max())
    np.save("halton_centers.npy", s)
    # done plotting
    mapper.centers = s
    return mapper 

class wrapped_mapper(NopMapper):
    def __init__(self, mapper):
        super(NopMapper,self).__init__()
        self.underlying_mapper = mapper
        self.labels = mapper.labels
        self.nbins = mapper.nbins

    def load_pcca_labels(self, label_file):
        f = open(label_file, 'r')
        self.pcca_labels = np.array([0] + list(pickle.load(f)))
        f.close()
        
    def assign(self, coords, mask=None, output=None):
        #print("In .assign")
        #print("coordinates")
        #print(coords, coords.shape)

        assigned = self.underlying_mapper.assign(coords)
        #print("shape of coords to remap")
        #print(assigned.shape)
        remapped = np.array(map(lambda x: self.pcca_labels[x], assigned))
        try:
            output[...] = remapped[...]
            #print(output, output.shape)
        except:
            pass
        #print("assigned")
        #print(assigned, assigned.shape)

        return remapped 

def pull_weight(n_iter, iter_group):
    '''
    Custom weight puller for a custom version of w_pdist. 
    This will probably eventually make it into the main repo
    '''
    #import sys, h5py
    #import numpy as np
    #
    ## Let's pull in the parent we want
    #parent = np.loadtxt('parent_to_track.txt')
    #parent_file = h5py.File('root_parents.h5', 'r')
    #parents = parent_file['iter_%08d/parents'%n_iter]
    #weights_to_get = (parents == parent)
    ## Get the weights
    #weights = iter_group['seg_index']['weight'][...]
    ## everything else is 0
    #data = np.zeros(weights.shape)
    #data[weights_to_get] = weights[weights_to_get]
    ## normalize 
    #data = data/sum(data)
    return iter_group['seg_index']['weight'][...]
