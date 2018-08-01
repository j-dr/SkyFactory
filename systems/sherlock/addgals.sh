#!/bin/bash
#SBATCH -p {Queue}
#SBATCH -t {TimeLimitHours}:00:00
#SBATCH -J {SimName}{SimNum}-adg
#SBATCH -o {SimName}{SimNum}-adg.%j.oe
#SBATCH --mail-type=All
#SBATCH --mail-user  {Email}
#SBATCH -N {NNodes}
#SBATCH --exclusive

srun -n {NTasks} -c {NCoresPerTask} {ExecDir}/pyaddgals/bin/addgals addgals.yaml
