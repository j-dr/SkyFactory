#!/bin/bash
#SBATCH -p iric
#SBATCH --qos iric
#SBATCH -t {TimeLimitHours}:00:00
#SBATCH -J {SimName}{SimNum}-dmap
#SBATCH -o {SimName}{SimNum}-dmap.%j.oe
#SBATCH --mail-type=All
#SBATCH --mail-user  {Email}
#SBATCH -N {NNodes}
#SBATCH --exclusive

while read cmd; do
    srun -n 1 $cmd &
done < densmap.cmds


