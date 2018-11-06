# Anything that uses bin mapper will need the system.py to be in the folder
if [ ! -e system.py ];then
  cp ../system.py .
fi
if [ ! -e west.h5 ];then
  ln -s ../west.h5 .
fi

# First check the probability distributions
python highdimplotter.py -W west.h5 --name-file full_names.txt -o pdists.png --smooth-data 0.25 

# Check steady state for each dimension
python evoPlotter.py -W west.h5 --name-file full_names.txt -o evolution.png

# Do a PCA to figure out the number of states
python PCAer.py -W west.h5 --name-file full_names.txt --first-iter 100 --last-iter 200

# now let's do PCCA+ and get some states
## assignment first, need to assign to original voronoi bins
w_assign -W west.h5 --states-from-file states.yaml || exit 1
mv assign.h5 assign_voronoi.h5
## then we need to calculate transition matrix
python transMatCalculator.py -W west.h5 -A assign_voronoi.h5 -o tm.npy || exit 1
## use PCCA+ to get the coarse grained system
COUNT=$1
python clusterer.py -TM tm.npy -A assign_voronoi.h5 --pcca-count $COUNT --name-file full_names.txt || exit 1

# Use the pcca to get GML files to plot networks
python networker.py -PCCA pcca.pkl --mstab-file metasble_assignments.pkl --state-labels state_labels.txt

# TODO: How to do halton seq stuff in this setup here?
# Let's reanalyze with halton seq
w_assign -W west.h5 --states-from-file states.yaml --bins-from-function assignment.assign_halton || exit 1
mv assign.h5 assign_halton.h5
python transMatCalculator.py -W west.h5 -A assign_halton.h5 -o tm_halton.npy || exit 1
python clusterer.py -TM tm_halton.npy -A assign_halton.h5 --mstab-file mstab_halton.pkl \
                    --pcca-count $COUNT --name-file full_names.txt --halton-centers halton_centers.npy || exit 1
