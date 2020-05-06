#!/bin/bash
#SBATCH -p {Queue}
#SBATCH -A {Repo}
#SBATCH --qos {QOS}
#SBATCH -t {TimeLimitHours}:00:00
#SBATCH -J {SimName}{SimNum}-sompz
#SBATCH -o {SimName}{SimNum}-sompz.%j.oe
#SBATCH --mail-type=All
#SBATCH --mail-user  {Email}
#SBATCH -N 1
#SBATCH -C haswell
#SBATCH -L SCRATCH
#SBATCH --exclusive
#SBATCH --image=docker:jderose/sompz:latest
#SBATCH --volume="/global/project/projectdirs/des/jderose/SkyFactory-config:/SkyFactory-config"

COUNTER=0
CatNames=({CatNames})
export HDF5_USE_FILE_LOCKING=FALSE
for cat in {Dummy};
do
    mkdir -p {OutDir}/$cat/0.25
    ln -s {OrigDir}/* {OutDir}/$cat/0.25/
    srun -n 1 -c {CoresPerNode} shifter python /sompz/test/full_run_on_data/sompz_assign_3.py sompz.$COUNTER.cfg
    srun -n 1 -c {CoresPerNode} shifter python /sompz/test/full_run_on_data/sompz_definebins_4.py sompz.$COUNTER.cfg
    let "COUNTER = $COUNTER + 1"
done
