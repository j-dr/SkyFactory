#!/bin/bash
#SBATCH -p regular
#SBATCH -t 12:00
#SBATCH -J {SimName}{SimNum}-dmap
#SBATCH -o {SimName}{SimNum}-dmap.%j.oe
#SBATCH -A {Repo}
#SBATCH --mail-type=All
#SBATCH --mail-user  {Email}
#SBATCH -N {NNodes}
#SBATCH --exclusive

while read cmd; do
    srun -n 1 $cmd &
done < densmap.cmds

