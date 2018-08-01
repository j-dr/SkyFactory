#!/bin/bash
#SBATCH -p iric,hns,normal
#SBATCH -t {TimeLimitHours}:00:00
#SBATCH -J {SimName}{SimNum}-sm
#SBATCH -o {SimName}{SimNum}-sm.%j.oe
#SBATCH --mail-type=All
#SBATCH --mail-user  {Email}
#SBATCH -N {NNodes}
#SBATCH --exclusive

cd {OPath}

COUNTER=0
while [ $COUNTER -lt {NCatalogs} ]; do
    srun -n {NTasks} -c {NCoresPerTask} python3 {ExecDir}/select_and_merge_samples.py selectsamples.$COUNTER.yaml &
    let "COUNTER = $COUNTER + 1"
done

wait

cd -
