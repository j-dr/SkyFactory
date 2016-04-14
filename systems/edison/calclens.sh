#!/bin/bash -l
#SBATCH -p regular
#SBATCH -t {TimeLimitHours}:00:00
#SBATCH -J {SimName}{SimNum}-rt
#SBATCH -o {SimName}{SimNum}-rt.%j.oe
#SBATCH -A {Repo}
#SBATCH --mail-type=All
#SBATCH --mail-user {Email}
#SBATCH -N {NNodes}
#SBATCH --exclusive

{GalCatListCMD}

srun -n {NCores} {ExecDir}/raytrace raytrace.cfg {Restart}
