#source env.sh
#w_assign -W $1 --construct-dataset assignment.pull_all_data -r ../west.cfg
# usage: w_pdist [-h] [-r RCFILE] [--quiet | --verbose | --debug] [--version]
#                [--max-queue-length MAX_QUEUE_LENGTH] [-W WEST_H5FILE]
#                [--first-iter N_ITER] [--last-iter N_ITER] [-b BINEXPR]
#                [-o OUTPUT] [-C] [--loose]
#                [--construct-dataset CONSTRUCT_DATASET | --dsspecs DSSPEC [DSSPEC ...]]
#                [--serial | --parallel | --work-manager WORK_MANAGER]
#                [--n-workers N_WORKERS]
for i in $(seq 1 12); do
  for j in $(seq $i 12);do
    if [ $i != $j ];then
      echo "$i $j" 
      echo "$i $j" > data_to_pull.txt
      w_pdist -W $1 -o pdist_$i_$j.h5 -b 100 --construct-dataset assignment.pull_data
    fi
  done
done
