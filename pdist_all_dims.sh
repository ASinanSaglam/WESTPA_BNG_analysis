#source env.sh
#w_assign -W $1 --construct-dataset assignment.pull_all_data -r ../west.cfg
# usage: w_pdist [-h] [-r RCFILE] [--quiet | --verbose | --debug] [--version]
#                [--max-queue-length MAX_QUEUE_LENGTH] [-W WEST_H5FILE]
#                [--first-iter N_ITER] [--last-iter N_ITER] [-b BINEXPR]
#                [-o OUTPUT] [-C] [--loose]
#                [--construct-dataset CONSTRUCT_DATASET | --dsspecs DSSPEC [DSSPEC ...]]
#                [--serial | --parallel | --work-manager WORK_MANAGER]
#                [--n-workers N_WORKERS]
echo "1 2" > data_to_pull.txt
w_pdist -W $1 -o pdist_1_2.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "1 3" > data_to_pull.txt
w_pdist -W $1 -o pdist_1_3.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "1 4" > data_to_pull.txt
w_pdist -W $1 -o pdist_1_4.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "1 5" > data_to_pull.txt
w_pdist -W $1 -o pdist_1_5.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "1 6" > data_to_pull.txt
w_pdist -W $1 -o pdist_1_6.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "1 7" > data_to_pull.txt
w_pdist -W $1 -o pdist_1_7.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "1 8" > data_to_pull.txt
w_pdist -W $1 -o pdist_1_8.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "1 9" > data_to_pull.txt
w_pdist -W $1 -o pdist_1_9.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "1 10" > data_to_pull.txt
w_pdist -W $1 -o pdist_1_10.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "1 11" > data_to_pull.txt
w_pdist -W $1 -o pdist_1_11.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "1 12" > data_to_pull.txt
w_pdist -W $1 -o pdist_1_12.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "2 3" > data_to_pull.txt
w_pdist -W $1 -o pdist_2_3.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "2 4" > data_to_pull.txt
w_pdist -W $1 -o pdist_2_4.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "2 5" > data_to_pull.txt
w_pdist -W $1 -o pdist_2_5.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "2 6" > data_to_pull.txt
w_pdist -W $1 -o pdist_2_6.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "2 7" > data_to_pull.txt
w_pdist -W $1 -o pdist_2_7.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "2 8" > data_to_pull.txt
w_pdist -W $1 -o pdist_2_8.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "2 9" > data_to_pull.txt
w_pdist -W $1 -o pdist_2_9.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "2 10" > data_to_pull.txt
w_pdist -W $1 -o pdist_2_10.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "2 11" > data_to_pull.txt
w_pdist -W $1 -o pdist_2_11.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "2 12" > data_to_pull.txt
w_pdist -W $1 -o pdist_2_12.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "3 4" > data_to_pull.txt
w_pdist -W $1 -o pdist_3_4.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "3 5" > data_to_pull.txt
w_pdist -W $1 -o pdist_3_5.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "3 6" > data_to_pull.txt
w_pdist -W $1 -o pdist_3_6.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "3 7" > data_to_pull.txt
w_pdist -W $1 -o pdist_3_7.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "3 8" > data_to_pull.txt
w_pdist -W $1 -o pdist_3_8.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "3 9" > data_to_pull.txt
w_pdist -W $1 -o pdist_3_9.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "3 10" > data_to_pull.txt
w_pdist -W $1 -o pdist_3_10.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "3 11" > data_to_pull.txt
w_pdist -W $1 -o pdist_3_11.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "3 12" > data_to_pull.txt
w_pdist -W $1 -o pdist_3_12.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "4 5" > data_to_pull.txt
w_pdist -W $1 -o pdist_4_5.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "4 6" > data_to_pull.txt
w_pdist -W $1 -o pdist_4_6.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "4 7" > data_to_pull.txt
w_pdist -W $1 -o pdist_4_7.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "4 8" > data_to_pull.txt
w_pdist -W $1 -o pdist_4_8.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "4 9" > data_to_pull.txt
w_pdist -W $1 -o pdist_4_9.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "4 10" > data_to_pull.txt
w_pdist -W $1 -o pdist_4_10.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "4 11" > data_to_pull.txt
w_pdist -W $1 -o pdist_4_11.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "4 12" > data_to_pull.txt
w_pdist -W $1 -o pdist_4_12.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "5 6" > data_to_pull.txt
w_pdist -W $1 -o pdist_5_6.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "5 7" > data_to_pull.txt
w_pdist -W $1 -o pdist_5_7.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "5 8" > data_to_pull.txt
w_pdist -W $1 -o pdist_5_8.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "5 9" > data_to_pull.txt
w_pdist -W $1 -o pdist_5_9.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "5 10" > data_to_pull.txt
w_pdist -W $1 -o pdist_5_10.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "5 11" > data_to_pull.txt
w_pdist -W $1 -o pdist_5_11.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "5 12" > data_to_pull.txt
w_pdist -W $1 -o pdist_5_12.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "6 7" > data_to_pull.txt
w_pdist -W $1 -o pdist_6_7.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "6 8" > data_to_pull.txt
w_pdist -W $1 -o pdist_6_8.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "6 9" > data_to_pull.txt
w_pdist -W $1 -o pdist_6_9.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "6 10" > data_to_pull.txt
w_pdist -W $1 -o pdist_6_10.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "6 11" > data_to_pull.txt
w_pdist -W $1 -o pdist_6_11.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "6 12" > data_to_pull.txt
w_pdist -W $1 -o pdist_6_12.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "7 8" > data_to_pull.txt
w_pdist -W $1 -o pdist_7_8.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "7 9" > data_to_pull.txt
w_pdist -W $1 -o pdist_7_9.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "7 10" > data_to_pull.txt
w_pdist -W $1 -o pdist_7_10.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "7 11" > data_to_pull.txt
w_pdist -W $1 -o pdist_7_11.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "7 12" > data_to_pull.txt
w_pdist -W $1 -o pdist_7_12.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "8 9" > data_to_pull.txt
w_pdist -W $1 -o pdist_8_9.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "8 10" > data_to_pull.txt
w_pdist -W $1 -o pdist_8_10.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "8 11" > data_to_pull.txt
w_pdist -W $1 -o pdist_8_11.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "8 12" > data_to_pull.txt
w_pdist -W $1 -o pdist_8_12.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "9 10" > data_to_pull.txt
w_pdist -W $1 -o pdist_9_10.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "9 11" > data_to_pull.txt
w_pdist -W $1 -o pdist_9_11.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "9 12" > data_to_pull.txt
w_pdist -W $1 -o pdist_9_12.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "10 11" > data_to_pull.txt
w_pdist -W $1 -o pdist_10_11.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "10 12" > data_to_pull.txt
w_pdist -W $1 -o pdist_10_12.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight
echo "11 12" > data_to_pull.txt
w_pdist -W $1 -o pdist_11_12.h5 -b 100 --construct-dataset assignment.pull_data #--construct-wdataset assignment.pull_weight

# Alex plotting tool
#python weighted_ensemble_tools/free_energy_contour_plotter.py --pdist-input pdist.h5 --first-iter $2 --last-iter $3 --xlabel "Binding RMSD ($\AA$)" --ylabel "Complex RMSD ($\AA$)" --xrange "(0,30)" --yrange "(0,60)" --plot-mode contourf_l --output ${4} --pdist-axes "(1,0)" --cmap "magma_r" --zmax 20 --zmin 0 --zbins 10 --postprocess plotting.func
