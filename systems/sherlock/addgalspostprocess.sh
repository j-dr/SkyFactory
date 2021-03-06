#!/bin/bash
#SBATCH -p iric
#SBATCH --qos iric
#SBATCH -t {TimeLimitHours}:00:00
#SBATCH -J {SimName}{SimNum}-adgpp
#SBATCH -o {SimName}{SimNum}-adgpp.%j.oe
#SBATCH --mail-type=All
#SBATCH --mail-user  {Email}
#SBATCH -N {NNodes}
#SBATCH --exclusive

srun -n {NCores} python {ExecDir}/scripts/finalize_catalog.py addgalspostprocess.cfg

