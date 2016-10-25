#!/bin/bash
#SBATCH -p {Queue}
#SBATCH -A {Repo}
#SBATCH --qos {QOS}
#SBATCH -t {TimeLimitHours}:00:00
#SBATCH -J {SimName}{SimNum}-erm
#SBATCH -o {SimName}{SimNum}-erm.%j.oe
#SBATCH --mail-type=All
#SBATCH --mail-user  {Email}
#SBATCH -N {NNodes}
#SBATCH --exclusive

module load python/2.7-anaconda

COUNTER=0
while [ $COUNTER -lt {NModels} ]; do
    srun -n {NTasks} -c {NCoresPerTask} python {ExecDir}/mock_error_apply.py errormodel.$COUNTER.cfg
    let "COUNTER = $COUNTER + 1"
done
