#!/bin/bash -l
#SBATCH -p regular
#SBATCH -t {TimeLimitHours}:00:00
#SBATCH -J {SimName}{SimNum}-adgpp
#SBATCH -o {SimName}{SimNum}-adgpp.%j.oe
#SBATCH -A {Repo}
#SBATCH --mail-type=All
#SBATCH --mail-user  {Email}
#SBATCH -N {NNodes}
#SBATCH --exclusive

module load mpi4py

srun -n {NCores} python {ExecDir}/scripts/finalize_catalog.py addgalspostprocess.cfg
