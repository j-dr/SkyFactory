#!/bin/bash
#SBATCH -p iric
#SBATCH --qos iric
#SBATCH -t {TimeLimitHours}:00:00
#SBATCH -J {SimName}{SimNum}-pz
#SBATCH -o {SimName}{SimNum}-pz.%j.oe
#SBATCH --mail-type=All
#SBATCH --mail-user  {Email}
#SBATCH -N {NNodes}
#SBATCH --exclusive

module load py-numpy

srun -n {NTasks} -c {NCoresPerTask} python {ExecDir}/run_photoz.py photoz.cfg
