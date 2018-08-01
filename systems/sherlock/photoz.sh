#!/bin/bash
#SBATCH -p iric,hns,normal
#SBATCH -t {TimeLimitHours}:00:00
#SBATCH -J {SimName}{SimNum}-pz
#SBATCH -o {SimName}{SimNum}-pz.%j.oe
#SBATCH --mail-type=All
#SBATCH --mail-user  {Email}
#SBATCH -N {NNodes}
#SBATCH --exclusive

COUNTER=0
while [ $COUNTER -lt {NCatalogs} ]; do
    srun -n {NTasks} -c {NCoresPerTask} python3 {ExecDir}/run_photoz.py photoz.$COUNTER.cfg
    let "COUNTER = $COUNTER + 1"
done

cd ../sampleselection

COUNTER=0
while [ $COUNTER -lt {NCatalogs} ]; do
    srun -n 1 -c {NCoresPerTask} python3 {ExecDir}/../sampleselection/merge_buzzard.py selectsamples.$COUNTER.yaml &
    let "COUNTER = $COUNTER + 1"
done

wait

cd -
