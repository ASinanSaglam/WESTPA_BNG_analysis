import h5py, sys
import numpy as np

west_file = sys.argv[1]
assign_file = sys.argv[2]
out_file = sys.argv[3]
a = h5py.File(assign_file, 'r')
w = h5py.File(west_file, 'r')
amnts = a['assignments']

tm_s = a['bin_labels'].shape[0]
tm = np.zeros((tm_s, tm_s))

def get_parent(iiter):
    return w['iterations/iter_%08d'%iiter]['seg_index']['parent_id']

def get_weight(iiter):
    return w['iterations/iter_%08d'%iiter]['seg_index']['weight']

def get_ass(iiter):
    return a['assignments'][iiter-1,:,:]

def get_walk_counts(iiter):
    return w['summary']['n_particles'][iiter-1]

ctr = 0
for iiter, iter_arr in enumerate(amnts):
    print("working on iter %i"%(iiter+1))
    ctr += 1
    #if iiter > 100:
    if iiter > 0:
        n_walks = get_walk_counts(iiter+1)
        parents = get_parent(iiter+1)
        ass = get_ass(iiter)
        weights = get_weight(iiter+1)
        print(iter_arr.shape)
        print(parents.shape, ass.shape, weights.shape, n_walks)
        for iwalk in range(n_walks):
            walk = iter_arr[iwalk]
            parent = parents[iwalk]
            weight = weights[iwalk]
            prev_ass = ass[parent] 
            tm[walk[0]][walk[1]] += weight
            tm[prev_ass[1]][walk[0]] += weight

print("counter, trans mat")
print(ctr, tm)
tm /= ctr
np.save(out_file, tm)
