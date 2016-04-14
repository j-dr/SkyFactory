#!/bin/bash
#SBATCH -p regular
#SBATCH -t {TimeLimitHours}:00:00
#SBATCH -J {SimName}{SimNum}-adg-Lb{BoxL}
#SBATCH -o {SimName}{SimNum}-adg-Lb{BoxL}.%j.oe
#SBATCH -A {Repo}
#SBATCH --mail-type=All
#SBATCH --mail-user  {Email}
#SBATCH -N {NNodes}
#SBATCH --exclusive

module load idl
idl setup_addgals.idl

sh submit_jobs.sh | cake add_multiple l-addgals.db

srun -n {NCores} cake run l-addgals.db --mpi 
