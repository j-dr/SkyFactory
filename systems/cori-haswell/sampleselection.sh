#!/bin/bash
#SBATCH -p {Queue}
#SBATCH -A {Repo}
#SBATCH --qos {QOS}
#SBATCH -t {TimeLimitHours}:00:00
#SBATCH -J {SimName}{SimNum}-adg
#SBATCH -o {SimName}{SimNum}-adg.%j.oe
#SBATCH --mail-type=All
#SBATCH --mail-user  {Email}
#SBATCH -N {NNodes}
#SBATCH -C haswell
#SBATCH -L SCRATCH
#SBATCH --exclusive
#SBATCH --image=docker:jderose/addgals-stack:latest
#SBATCH --volume="/global/project/projectdirs/des/jderose/SkyFactory-config:/SkyFactory-config;"

cd {OPath}

COUNTER=0
while [ $COUNTER -lt {NCatalogs} ]; do
    srun -n {NTasks} -c {NCoresPerTask} python /pyaddgals/bin/skyfactory/select_and_merge_samples.py selectsamples.$COUNTER.yaml
    let "COUNTER = $COUNTER + 1"
done

wait

cd -
