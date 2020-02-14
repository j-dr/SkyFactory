#!/bin/bash
#SBATCH -p {Queue}
#SBATCH -A {Repo}
#SBATCH --qos {QOS}
#SBATCH -t {TimeLimitHours}:00:00
#SBATCH -J {SimName}{SimNum}-rm
#SBATCH -o {SimName}{SimNum}-rm.%j.oe
#SBATCH --mail-type=All
#SBATCH --mail-user  {Email}
#SBATCH -N {NNodesRedmagic}
#SBATCH -C haswell
#SBATCH -L SCRATCH
#SBATCH --exclusive
#SBATCH --image={RedmapperShifter}
#SBATCH --volume="/global/project/projectdirs/des/jderose/SkyFactory-config:/SkyFactory-config;{OutputBase}:/output"

COUNTER=0
while [ $COUNTER -lt {NModels} ]; do
    cd {OPath}
    srun -n 1 -c {NCoresPerTask} shifter /bin/bash -c ". /opt/redmapper/startup.sh && redmagic_run.py -c {JobBase}/redmapper.${{COUNTER}}.cfg -n {NRandoms}"
    let "COUNTER = $COUNTER + 1"
done
