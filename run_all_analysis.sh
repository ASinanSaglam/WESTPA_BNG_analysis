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

# TODO: How to do halton seq stuff in this setup here?
# TODO: How to deal with making networks?

## OLD STUFF ## 
## Get the pdist h5
#echo "1 2" > data_to_pull.txt
#w_pdist -W $WESTH5_FILE -o pdist_1_2.h5 -b 30 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
# Get -lnP plot with voronoi bins
#python weighted_ensemble_tools/free_energy_contour_plotter.py --pdist-input pdist_1_2.h5 --first-iter 1 --xlabel "Protein A" --ylabel "Protein B" --plot-mode contourf_l --output a_b_vor.png --pdist-axes "(0,1)" --cmap "magma_r" --postprocess plotting.func #--smooth-data 1 --smooth-curves 1 #--xrange "(0,30)" --yrange "(0,30)" --zmax 10 --zmin 0 --zbins 10 
#python weighted_ensemble_tools/free_energy_contour_plotter.py --pdist-input pdist_1_2.h5 --first-iter 1 --xlabel "Protein A" --ylabel "Protein B" --plot-mode contourf_l --output a_b_clust.png --pdist-axes "(0,1)" --cmap "magma_r" --postprocess plotting.func_ass #--smooth-data 1 --smooth-curves 1 #--xrange "(0,30)" --yrange "(0,30)" --zmax 10 --zmin 0 --zbins 10 
#python weighted_ensemble_tools/free_energy_contour_plotter.py --pdist-input pdist_7_8.h5 --first-iter 1 --xlabel "Protein A" --ylabel "Protein B" --plot-mode contourf_l --output a_b_basic.png --pdist-axes "(0,1)" --cmap "magma_r" --postprocess plotting.plot_basic #--smooth-data 1 --smooth-curves 1 #--xrange "(0,30)" --yrange "(0,30)" --zmax 10 --zmin 0 --zbins 10 

### 
# Assign to PCCA+ states
#w_assign -W $WESTH5_FILE --bins-from-function assignment.assign_pcca --states-from-file states_8dims.yaml --construct-dataset assignment.pull_all_data || exit 1
#mv assign.h5 assign_pcca.h5
# Make transition matrix from those coarse grained states manually
#python make_transMat.py $WESTH5_FILE assign_pcca.h5 pcca_tm.npy || exit 1
#w_direct all -W $WESTH5_FILE -a assign_pcca.h5 -db --first-iter 1 || exit 1
#w_reweight all -W $WESTH5_FILE -a assign_pcca.h5 -db --first-iter 1 || exit 1
#mv direct.h5 direct_pcca.h5
#mv reweight.h5 reweight_pcca.h5
#python pcca_label_graph.py assign_pcca.h5 reweight_pcca.h5 || exit 1
# Get -lnP plot with assignments
#python weighted_ensemble_tools/free_energy_contour_plotter.py --pdist-input pdist_1_2.h5 --first-iter 500 --xlabel "Protein A" --ylabel "Protein B" --xrange "(0,30)" --yrange "(0,30)" --plot-mode contourf_l --output a_b_paths.png --pdist-axes "(0,1)" --cmap "magma_r" --zmax 10 --zmin 0 --zbins 10 --postprocess plotting.plot_paths --smooth-data 1 --smooth-curves 1
#plothist average pdist_1_2.h5 0 -o 1d.png --first-iter 50 --postprocess-function plotting.func_1d --range "0,6.0"
#plothist average pdist_1_2.h5 0 -o 1d_prob.png --first-iter 50 --postprocess-function plotting.func_1d --range "0,0.2" --linear
#python analyze_bf.py exmisa_bf.cdat
#python weighted_ensemble_tools/free_energy_contour_plotter.py --pdist-input /home/boltzmann/PROJECTS/BNGL/exMISA_BF/pdist_bf.h5 --first-iter 1 --last-iter 999 --xlabel "Protein A" --ylabel "Protein B" --xrange "(0,30)" --yrange "(0,30)" --plot-mode contourf_l --output a_b_bf.png --pdist-axes "(0,1)" --cmap "magma_r" --zmax 10 --zmin 0 --zbins 10 --postprocess plotting.plot_basic --smooth-data 1 --smooth-curves 1
# Let's reanalyze with halton seq
#w_assign -W $WESTH5_FILE --states-from-file states_8dims.yaml --bins-from-function assignment.assign_halton || exit 1
#mv assign.h5 assign_halton.h5
#python make_transMat.py $WESTH5_FILE assign_halton.h5 halton_tm.npy || exit 1
#python make_pcca_halton.py halton_tm.npy assign_halton.h5 4 || exit 1
#python weighted_ensemble_tools/free_energy_contour_plotter.py --pdist-input pdist_1_2.h5 --first-iter 500 --xlabel "Protein A" --ylabel "Protein B" --xrange "(0,30)" --yrange "(0,30)" --plot-mode contourf_l --output a_b_vor_halt.png --pdist-axes "(0,1)" --cmap "magma_r" --zmax 10 --zmin 0 --zbins 10 --postprocess plotting.func_halt --smooth-data 1 --smooth-curves 1
#python weighted_ensemble_tools/free_energy_contour_plotter.py --pdist-input pdist_1_2.h5 --first-iter 500 --xlabel "Protein A" --ylabel "Protein B" --xrange "(0,30)" --yrange "(0,30)" --plot-mode contourf_l --output a_b_clust_halt.png --pdist-axes "(0,1)" --cmap "magma_r" --zmax 10 --zmin 0 --zbins 10 --postprocess plotting.func_ass_halt --smooth-data 1 --smooth-curves 1
