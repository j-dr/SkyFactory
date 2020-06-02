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
export HDF5_USE_FILE_LOCKING=FALSE

COUNTER=0
while [ $COUNTER -lt {NCatalogs} ]; do
    srun -n {NTasks} -c {NCoresPerTask} shifter python3 /pyaddgals/bin/skyfactory/merge_truth_obs_pz.py {JDir}/selectsamples.$COUNTER.yaml
#    srun -n 1 -c {CoresPerNode} shifter python /pyaddgals/bin/skyfactory/merge_buzzard.py {JDir}/selectsamples.$COUNTER.yaml
#    srun -n 1 -c {CoresPerNode} shifter python /pyaddgals/bin/skyfactory/make_master_h5_cat.py {JDir}/mastercat.$COUNTER.yaml
#    srun -n 1 -c {CoresPerNode} shifter python /pyaddgals/bin/skyfactory/link_sompz_to_mastercat.py {JDir}/mastercat.$COUNTER.yaml    
    let "COUNTER = $COUNTER + 1"
done

wait

cd -
