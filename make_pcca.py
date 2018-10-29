import IPython
import pickle, h5py, sys
import numpy as np
import networkx as nx
import pyemma as pe 

np.set_printoptions(precision=2)

tm_file = sys.argv[1]
assign_file = sys.argv[2]
pcca_cluster_count = sys.argv[3]

tm = np.load(tm_file)
zt = np.where(tm.sum(axis=1)==0)
ind = np.where(tm.sum(axis=1)!=0)[0]
tm = tm[...,ind][ind,...]
tm = (tm + tm.T)/2.0
#print("tm loaded")
#print(tm)
#print((tm < 0).any())
def row_normalize(mat):
    for irow, row in enumerate(mat):
        if row.sum() != 0:
            mat[irow] /= row.sum() 
row_normalize(tm)
#IPython.embed()
#print("row normalized tm")
#print(tm)
#print((tm < 0).any())
#mcsn = csn.CSN(tm, symmetrize=True)
#rtm = mcsn.transmat.toarray()
#print("symm tm")
#print(tm)
#print((tm < 0).any())
MSM = pe.msm.MSM(tm, reversible=True)
pcca = MSM.pcca(pcca_cluster_count)
p = pcca.coarse_grained_stationary_probability
ctm = pcca.coarse_grained_transition_matrix
#print(ctm.sum(axis=1))
print("MSM probs")
print(p*100)
print("MSM TM")
print(ctm*100)
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
