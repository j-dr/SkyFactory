#!/bin/bash
#SBATCH -p iric
#SBATCH --qos iric
#SBATCH -t {TimeLimitHours}:00:00
#SBATCH -J {SimName}{SimNum}-sm
#SBATCH -o {SimName}{SimNum}-sm.%j.oe
#SBATCH --mail-type=All
#SBATCH --mail-user  {Email}
#SBATCH -N {NNodes}
#SBATCH --exclusive

module load py-numpy

COUNTER=0
while [ $COUNTER -lt {NCatalogs} ]; do
    srun -n {NTasks} -c {NCoresPerTask} python {ExecDir}/select_samples.py selectsamples.$COUNTER.yaml &
    let "COUNTER = $COUNTER + 1"
done

wait

cd {OPath}
COUNTER=0
while [ $COUNTER -lt {NCatalogs} ]; do
    srun -n 1 -c {NCoresPerTask} python {ExecDir}/merge_buzzard.py flatcat.$COUNTER.yaml
    let "COUNTER = $COUNTER + 1"
done
cd -



