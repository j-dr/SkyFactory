#!/bin/bash
#SBATCH -p iric
#SBATCH --qos iric
#SBATCH -t {TimeLimitHours}:00:00
#SBATCH -J {SimName}{SimNum}-rt
#SBATCH -o {SimName}{SimNum}-rt.%j.oe
#SBATCH --mail-type=All
#SBATCH --mail-user {Email}
#SBATCH -N {NNodes}
#SBATCH --exclusive

cd {OPath}

srun -n {NCores} {ExecDir}/raytrace raytrace.cfg {Restart}
