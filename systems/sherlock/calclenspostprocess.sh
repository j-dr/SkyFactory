#!/bin/bash
#SBATCH -p iric
#SBATCH --qos iric
#SBATCH -t {TimeLimitHours}:00:00
#SBATCH -J {SimName}{SimNum}-rtpp
#SBATCH -o {SimName}{SimNum}-rtpp.%j.oe
#SBATCH --mail-type=All
#SBATCH --mail-user {Email}
#SBATCH -N {NNodes}
#SBATCH --exclusive

cd {OPath}

srun -n {NCores} python {ExecDir}/scripts/concat.py calclensconcat.yaml
