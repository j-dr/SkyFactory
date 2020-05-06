#!/bin/bash
#SBATCH -p {Queue}
#SBATCH -A {Repo}
##SBATCH --qos {QOS}
#SBATCH -t 2:00:00
#SBATCH -J {SimName}{SimNum}-adg
#SBATCH -o {SimName}{SimNum}-adg.%j.oe
#SBATCH --mail-type=All
#SBATCH --mail-user  {Email}
#SBATCH -N 1
#SBATCH -C haswell
#SBATCH -L SCRATCH
#SBATCH --exclusive
#SBATCH --image=docker:jderose/addgals-stack:latest
#SBATCH --volume="/global/project/projectdirs/des/jderose/SkyFactory-config:/SkyFactory-config;{BaseName}:/output"

COUNTER=0
while [ $COUNTER -lt {NCatalogs} ]; do
    srun -n 1 -c 32 shifter python3 /pyaddgals/bin/skyfactory/make_master_h5_cat.py make_master_cat.${COUNTER}.yaml
    let "COUNTER = $COUNTER + 1"    
done
