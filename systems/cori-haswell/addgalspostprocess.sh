#!/bin/bash
#SBATCH -p {Queue}
#SBATCH -A {Repo}
#SBATCH --qos {QOS}
#SBATCH -t {TimeLimitHours}:00:00
#SBATCH -J {SimName}{SimNum}-adgpp
#SBATCH -o {SimName}{SimNum}-adgpp.%j.oe
#SBATCH --mail-type=All
#SBATCH --mail-user  {Email}
#SBATCH -N {NNodes}
#SBATCH -C haswell
#SBATCH -L SCRATCH
#SBATCH --exclusive

module load python/2.7-anaconda 

srun -n {NCores} python {ExecDir}/scripts/finalize_catalog.py addgalspostprocess.cfg
