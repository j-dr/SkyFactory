#!/bin/bash
#SBATCH -p {Queue}
#SBATCH -A {Repo}
#SBATCH --qos {QOS}
#SBATCH -t {TimeLimitHours}:00:00
#SBATCH -J {SimName}{SimNum}-dmap
#SBATCH -o {SimName}{SimNum}-dmap.%j.oe
#SBATCH --mail-type=All
#SBATCH --mail-user  {Email}
#SBATCH -N {NNodes}
#SBATCH --exclusive

module load mpi4py python/2.7-anaconda 

while read cmd; do
    srun -n 1 $cmd &
done < densmap.cmds
