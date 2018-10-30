import pickle, h5py, sys, argparse
import numpy as np
import networkx as nx
import pyemma as pe 

np.set_printoptions(precision=2)

class WEClusterer:
    def __init__(self):
        # Get arguments as usual
        self._parse_args()
        # Parse and set the arguments
        # Open files 
        self.assignFile = h5py.File(self.args.assign_path, 'r')
        self.tm = np.load(self.args.trans_mat_file)
        # Set assignments
        self.assignments = self.assignFile['assignments']
        # Cluster count
        self.cluster_count = self.args.cluster_count
        # Do we symmetrize
        self.symmetrize = self.args.symmetrize

    def _parse_args(self):
        parser = argparse.ArgumentParser()

        # Data input options
        parser.add_argument('-TM', '--trans_mat',
                            dest='trans_mat_file',
                            default="tm.npy",
                            help='Path to the numpy.loadable file that contains the'
                            'transition matrix',
                            type=str)
        parser.add_argument('-A', '--assignh5',
                            dest='assign_path',
                            default="assign.h5",
                            help='Path to the assignment h5 file', 
                            type=str)
        # Cluster count
        parser.add_argument('--pcca-count', required=True,
                          dest='cluster_count',
                          help='Cluster count for the PCCA+ algorithm',
                          type=int)

        # Do we symmetrize the matrix?
        parser.add_argument('--symmetrize-matrix',
                            dest='symmetrize', action='store_true', default=False,
                            help='Symmetrize matrix using (TM + TM.T)/2.0')

        self.args = parser.parse_args()

    def row_normalize(self):
        for irow, row in enumerate(self.tm):
            if row.sum() != 0:
                self.tm[irow] /= row.sum() 

    def preprocess_tm(self):
        zt = np.where(tm.sum(axis=1)==0)
        if len(zt[0]) != 0:
            print("there are bins where there are no transitions")
            print(zt)
            print("removing these bins from the transition matrix")
        ind = np.where(tm.sum(axis=1)!=0)[0]
        tm = tm[...,ind][ind,...]
        if self.symmetrize:
            print("symmetrizing transition matrix")
            tm = (tm + tm.T)/2.0
        row_normalize(tm)

    def print_pcca_results(self):
        print("MSM probs")
        print(self.p*100)
        print("MSM TM")
        print(self.ctm*100)

    def cluster(self):
        self.preprocess_tm()

        self.MSM = pe.msm.MSM(self.tm, reversible=True)
        self.pcca = self.MSM.pcca(self.cluster_count)
        self.p = self.pcca.coarse_grained_stationary_probability
        self.ctm = self.pcca.coarse_grained_transition_matrix
        self.print_pcca_results()

if __name__ == '__main__':
    c = WEClusterer()
    c.cluster()


sys.exit()
metastab_ass = pcca.metastable_assignment
mstabs = []
li = 0
for i in zt[0]:
    mstabs += list(metastab_ass[li:i]) 
    mstabs += [0]
    li = i
mstabs += list(metastab_ass[li:])
mstabs = np.array(mstabs)
f = open("metasble_assignments.pkl", "w")
pickle.dump(mstabs, f)
f.close()

a = h5py.File(assign_file, 'r')
bin_labels_str = a['bin_labels'][...]
bin_labels = []
for ibstr, bstr in enumerate(bin_labels_str):
    st, ed = bstr.find('['), bstr.find(']')
    bin_labels.append(eval(bstr[st:ed+1]))
bin_labels = np.array(bin_labels)[ind]
for i in range(bin_labels.shape[1]):
    bin_labels[:,i] = bin_labels[:,i] - bin_labels[:,i].min()
    bin_labels[:,i] = bin_labels[:,i]/bin_labels[:,i].max()
bin_labels *= 100
#bin_labels = np.array(bin_labels[1:])
#bin_labels_01 = np.array(map(lambda x: (x[0], x[1]), bin_labels))
#bin_labels_01 = bin_labels_01[1:]

name_file = open("names.txt", 'r')
names = name_file.readline().split()
name_file.close()
width = 6
for i in range(metastab_ass.max()+1):
    print("metastable state {} with probability {:.2f}%".format(i, p[i]*100))
    print("{} bins are assigned to this state".format(len(np.where(metastab_ass.T==i)[0])))
    for name in names:
        # python 2.7 specific unfortunately
        print '{0:^{width}}'.format(name, width=width, align="center"),
    # similarly 2.7 specific
    print
    avg_vals = bin_labels[metastab_ass.T==i].mean(axis=0)
    for val in avg_vals:
        # python 2.7 specific unfortunately
        print '{0:{width}.2f}'.format(val, width=width),
    # similarly 2.7 specific
    print

#print("metastab 0")
#print(bin_labels[metastab_ass.T==0].mean(axis=0))
#print("metastab 1")
#print(bin_labels[metastab_ass.T==1].mean(axis=0))
#print("metastab 2")
#print(bin_labels[metastab_ass.T==2].mean(axis=0))
#print("metastab 3")
#print(bin_labels[metastab_ass.T==3].mean(axis=0))

#print(cents)
#print(bin_assignments)
#print(metastab_ass)
#print(bin_labels)
#IPython.embed()

state_labels = {0: "loGBX", 1: "loKLF4", 2: "t1", 3:"t2"}
state_colors = {0: "#FF00FF", 1: "#000000", 2: "#FF0000", 3:"#0000FF"}
tm = pcca.transition_matrix
node_sizes = pcca.stationary_probability*1000
edge_sizes = tm

G = nx.DiGraph()
for i in range(tm.shape[0]):
    if node_sizes[i] > 0:
        G.add_node(i, weight=float(node_sizes[i]), color=state_colors[metastab_ass[i]], LabelGraphics={"text": " "}, #)
               graphics={"type": "circle", "fill": state_colors[metastab_ass[i]], "w": node_sizes[i], "h": node_sizes[i]})

for i in range(tm.shape[0]):
    for j in range(tm.shape[1]):
        if i != j:
            #if edge_sizes[i][j] > 1e-2:
            if edge_sizes[i][j] > 0:
                G.add_edge(i, j, weight=float(edge_sizes[i][j]), graphics={"type": "arc", "targetArrow": "none", "fill": state_colors[metastab_ass[i]]})

nx.write_gml(G, "pcca_full.gml")

tm = pcca.coarse_grained_transition_matrix
node_sizes = pcca.coarse_grained_stationary_probability*1000
edge_sizes = tm
print("coarse tm")
print(edge_sizes)
print("coarse probs")
print(pcca.coarse_grained_stationary_probability)

G = nx.DiGraph()
for i in range(tm.shape[0]):
    if node_sizes[i] > 0:
        G.add_node(i, weight=float(node_sizes[i]), color=state_colors[i], LabelGraphics={"text": " "}, #)
               graphics={"type": "circle", "fill": state_colors[i], "w": node_sizes[i], "h": node_sizes[i]})

for i in range(tm.shape[0]):
    for j in range(tm.shape[1]):
        if i != j:
            if edge_sizes[i][j] > 0:
                G.add_edge(i, j, weight=float(edge_sizes[i][j]), graphics={"type": "arc", "targetArrow": "none", "fill": state_colors[i]})

nx.write_gml(G, "pcca_coarse.gml")
